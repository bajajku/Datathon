"""
Multi-Scene Processor Module

Handles large documents by splitting them into multiple scenes and combining
them into a single cohesive video. Supports processing PDFs with text input.
"""

import os
import sys
import json
import re
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from io import BytesIO

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.llm import LLM
from .input_processor import InputProcessor
from .scene_parser import SceneParser, CodeGenerationContext
from .scene_structure import SceneStructure, SceneSettings, Color


@dataclass
class DocumentChunk:
    """Represents a chunk of document content."""
    id: str
    title: str
    content: str
    page_numbers: Optional[List[int]] = None
    chunk_type: str = "general"  # general, formula, diagram, summary, etc.
    priority: int = 0  # For ordering scenes


@dataclass
class MultiSceneStructure:
    """Contains multiple scenes that form a complete video."""
    title: str
    description: str
    total_duration: float
    scenes: List[SceneStructure]
    scene_order: List[str]  # List of scene IDs in order
    transitions: Dict[str, str] = None  # Optional transition types between scenes


class DocumentChunker:
    """Intelligently splits large documents into logical chunks."""
    
    def __init__(self, api_key: Optional[str] = None, max_chunk_size: int = 2000):
        """
        Initialize the document chunker.
        
        Args:
            api_key: Gemini API key for intelligent chunking
            max_chunk_size: Maximum characters per chunk
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.max_chunk_size = max_chunk_size
        
        if self.api_key:
            self.llm = LLM(
                provider="google_genai",
                model_name="gemini-2.5-flash",
                api_key=self.api_key,
                temperature=0.3
            )
        else:
            self.llm = None
    
    def chunk_document(self, content: str, document_title: str = "") -> List[DocumentChunk]:
        """
        Split document content into logical chunks.
        
        Args:
            content: Full document content
            document_title: Title of the document
            
        Returns:
            List of DocumentChunk objects
        """
        # First try intelligent chunking with LLM
        if self.llm and len(content) > self.max_chunk_size:
            try:
                return self._intelligent_chunking(content, document_title)
            except Exception as e:
                print(f"Intelligent chunking failed: {e}, falling back to simple chunking")
        
        # Fallback to simple chunking
        return self._simple_chunking(content, document_title)
    
    def _intelligent_chunking(self, content: str, document_title: str) -> List[DocumentChunk]:
        """Use LLM to intelligently split content into logical sections."""
        
        system_prompt = """You are a document chunking expert. Split the given content into logical sections for video animation.

Each section should:
1. Be focused on a single topic/concept
2. Be suitable for a 30-60 second animation
3. Have a clear title and purpose
4. Be self-contained but flow logically

Return a JSON array with this structure:
[
  {
    "id": "section_1",
    "title": "Introduction to Topic",
    "content": "The actual content for this section...",
    "chunk_type": "introduction|formula|concept|example|summary",
    "priority": 1
  }
]

Guidelines:
- Keep each chunk under 1500 characters
- Prioritize mathematical formulas, key concepts, and examples
- Number sections logically (1, 2, 3...)
- Use descriptive titles
"""

        user_prompt = f"""Split this document into logical animation sections:

Document Title: {document_title}
Content Length: {len(content)} characters

Content:
{content}

Return the sections as a JSON array."""

        try:
            chat = self.llm.create_chat()
            messages = [
                ("system", system_prompt),
                ("user", user_prompt)
            ]
            
            response = chat.invoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Clean and parse JSON response
            json_str = self._clean_json_response(response_text)
            chunks_data = json.loads(json_str)
            
            # Convert to DocumentChunk objects
            chunks = []
            for i, chunk_data in enumerate(chunks_data):
                chunk = DocumentChunk(
                    id=chunk_data.get("id", f"section_{i+1}"),
                    title=chunk_data.get("title", f"Section {i+1}"),
                    content=chunk_data.get("content", ""),
                    chunk_type=chunk_data.get("chunk_type", "general"),
                    priority=chunk_data.get("priority", i+1)
                )
                chunks.append(chunk)
            
            # Sort by priority
            chunks.sort(key=lambda x: x.priority)
            
            return chunks
            
        except Exception as e:
            raise RuntimeError(f"Failed to perform intelligent chunking: {str(e)}")
    
    def _simple_chunking(self, content: str, document_title: str) -> List[DocumentChunk]:
        """Simple fallback chunking by size and natural breaks."""
        
        chunks = []
        
        # Split by common section markers
        section_patterns = [
            r'\n\n+',  # Paragraph breaks
            r'\n(?=\d+\.)',  # Numbered lists
            r'\n(?=[A-Z][a-z]+:)',  # Section headers with colons
            r'(?<=\.)\s+(?=[A-Z])',  # Sentence boundaries
        ]
        
        # Try to split by paragraphs first
        paragraphs = re.split(r'\n\n+', content)
        
        current_chunk = ""
        chunk_count = 1
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed max size, create a chunk
            if len(current_chunk) + len(paragraph) > self.max_chunk_size and current_chunk:
                chunk = DocumentChunk(
                    id=f"section_{chunk_count}",
                    title=f"{document_title} - Part {chunk_count}" if document_title else f"Section {chunk_count}",
                    content=current_chunk.strip(),
                    chunk_type="general",
                    priority=chunk_count
                )
                chunks.append(chunk)
                current_chunk = paragraph
                chunk_count += 1
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        # Add the last chunk
        if current_chunk.strip():
            chunk = DocumentChunk(
                id=f"section_{chunk_count}",
                title=f"{document_title} - Part {chunk_count}" if document_title else f"Section {chunk_count}",
                content=current_chunk.strip(),
                chunk_type="general",
                priority=chunk_count
            )
            chunks.append(chunk)
        
        return chunks
    
    def _clean_json_response(self, response: str) -> str:
        """Clean LLM response to extract valid JSON."""
        # Remove markdown code blocks
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        
        if response.endswith("```"):
            response = response[:-3]
        
        return response.strip()


class MultiSceneProcessor:
    """Processes large documents into multiple coordinated scenes."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the multi-scene processor.
        
        Args:
            api_key: Gemini API key for processing
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.chunker = DocumentChunker(api_key=self.api_key)
        self.processor = InputProcessor(api_key=self.api_key)
        self.parser = SceneParser()
    
    def process_combined_input(self, 
                             pdf_path: Optional[str] = None,
                             pdf_bytes: Optional[BytesIO] = None, 
                             text_input: str = "",
                             document_title: str = "") -> MultiSceneStructure:
        """
        Process combined PDF and text input into multiple scenes.
        
        Args:
            pdf_path: Path to PDF file
            pdf_bytes: PDF file as BytesIO object
            text_input: Additional text input
            document_title: Title for the document
            
        Returns:
            MultiSceneStructure containing all generated scenes
        """
        # Step 1: Extract and combine content
        combined_content = ""
        
        if pdf_path or pdf_bytes:
            if pdf_path:
                pdf_text = self.processor._extract_text_from_pdf(pdf_path)
            else:
                pdf_text = self.processor._extract_text_from_pdf_bytes(pdf_bytes)
            combined_content += pdf_text
        
        if text_input:
            if combined_content:
                combined_content += f"\n\n--- Additional Instructions ---\n{text_input}"
            else:
                combined_content = text_input
        
        if not combined_content.strip():
            raise ValueError("No content provided (PDF and text input are both empty)")
        
        # Step 2: Split into logical chunks
        print(f"Splitting document into chunks (total length: {len(combined_content)} chars)")
        chunks = self.chunker.chunk_document(combined_content, document_title)
        print(f"Created {len(chunks)} chunks")
        
        # Step 3: Process each chunk into a scene
        scenes = []
        scene_order = []
        total_duration = 0
        
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}: {chunk.title}")
            
            try:
                # Create enhanced content with context
                enhanced_content = f"Title: {chunk.title}\n\nContent: {chunk.content}"
                if i > 0:
                    enhanced_content = f"This is part {i+1} of a {len(chunks)}-part series. " + enhanced_content
                
                # Add instruction to create a simpler scene for multi-scene video
                enhanced_content += "\n\nNote: Create a focused, concise scene suitable for a multi-part video. Keep it simple and clear."
                
                scene = self.processor.process_text_input(enhanced_content)
                
                # Update scene metadata
                scene.settings.title = chunk.title
                scene.settings.description = f"Part {i+1} of {len(chunks)}: {chunk.title}"
                
                # Adjust timing for multi-scene flow
                base_duration = scene.settings.duration
                scene.settings.duration = max(base_duration, 3.0)  # Minimum 3 seconds per scene
                
                scenes.append(scene)
                scene_order.append(chunk.id)
                total_duration += scene.settings.duration
                
                print(f"✓ Generated scene: {scene.settings.title} ({scene.settings.duration}s)")
                
            except Exception as e:
                print(f"✗ Failed to process chunk {chunk.title}: {e}")
                # Continue with other chunks
                continue
        
        if not scenes:
            raise RuntimeError("Failed to generate any scenes from the provided content")
        
        # Step 4: Create multi-scene structure
        multi_scene = MultiSceneStructure(
            title=document_title or "Generated Video",
            description=f"Multi-scene video with {len(scenes)} parts",
            total_duration=total_duration,
            scenes=scenes,
            scene_order=scene_order
        )
        
        return multi_scene
    
    def generate_combined_code(self, multi_scene: MultiSceneStructure) -> str:
        """
        Generate Manim code that combines multiple scenes into one video.
        
        Args:
            multi_scene: MultiSceneStructure containing all scenes
            
        Returns:
            Combined Manim Python code
        """
        from code_generation.manim_code_generator import ManimCodeGenerator
        
        generator = ManimCodeGenerator(api_key=self.api_key)
        
        # Generate code for each individual scene
        scene_contexts = []
        for scene in multi_scene.scenes:
            context = self.parser.parse(scene)
            scene_contexts.append(context)
        
        # Create combined scene code
        combined_code = self._create_combined_scene_code(multi_scene, scene_contexts, generator)
        
        return combined_code
    
    def _create_combined_scene_code(self, 
                                   multi_scene: MultiSceneStructure, 
                                   contexts: List[CodeGenerationContext],
                                   generator: Any) -> str:
        """Create Manim code that combines multiple scenes."""
        
        # Generate individual scene methods
        scene_methods = []
        imports_needed = set(["from manim import *"])
        
        for i, (scene, context) in enumerate(zip(multi_scene.scenes, contexts)):
            method_name = f"scene_{i+1}"
            
            # Generate code for this scene
            individual_code = generator.generate_code(context)
            
            # Extract the construct method content
            method_content = self._extract_construct_content(individual_code)
            
            # Create scene method
            scene_method = f'''    def {method_name}(self):
        """Scene {i+1}: {context.scene_title}"""
        # Clear previous scene
        self.clear()
        
        # Scene content
{self._indent_code(method_content, 2)}
        
        # Scene transition
        self.wait(0.5)'''
            
            scene_methods.append(scene_method)
            
            # Collect imports
            if context.math_objects:
                imports_needed.add("import numpy as np")
        
        # Create the combined class
        combined_code = f'''{"".join(sorted(imports_needed))}

class CombinedVideo(Scene):
    """
    {multi_scene.title}
    {multi_scene.description}
    
    Total Duration: {multi_scene.total_duration:.1f} seconds
    Number of Scenes: {len(multi_scene.scenes)}
    """
    
    def construct(self):
        """Main video construction with multiple scenes."""
        # Title card
        title = Text("{multi_scene.title}", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Play all scenes in sequence
{self._create_scene_sequence(len(multi_scene.scenes))}
        
        # End card
        end_text = Text("End", font_size=36)
        self.play(FadeIn(end_text))
        self.wait(1)

{chr(10).join(scene_methods)}'''
        
        return combined_code
    
    def _extract_construct_content(self, manim_code: str) -> str:
        """Extract content from construct method of generated code."""
        lines = manim_code.split('\n')
        
        in_construct = False
        construct_lines = []
        indent_level = 0
        
        for line in lines:
            if 'def construct(self):' in line:
                in_construct = True
                continue
            
            if in_construct:
                # Check if we've left the construct method (next method or class)
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    break
                
                # Skip comments about scene duration and class docstrings
                if ('"""' in line or 
                    line.strip().startswith('#') and 
                    ('scene duration' in line.lower() or 'background color' in line.lower())):
                    continue
                
                construct_lines.append(line)
        
        # Remove leading/trailing empty lines
        while construct_lines and not construct_lines[0].strip():
            construct_lines.pop(0)
        while construct_lines and not construct_lines[-1].strip():
            construct_lines.pop()
        
        return '\n'.join(construct_lines)
    
    def _indent_code(self, code: str, additional_levels: int) -> str:
        """Add additional indentation to code block."""
        lines = code.split('\n')
        indent = '    ' * additional_levels
        
        indented_lines = []
        for line in lines:
            if line.strip():  # Only indent non-empty lines
                indented_lines.append(indent + line)
            else:
                indented_lines.append(line)
        
        return '\n'.join(indented_lines)
    
    def _create_scene_sequence(self, num_scenes: int) -> str:
        """Create the scene sequence calls."""
        sequence_lines = []
        for i in range(1, num_scenes + 1):
            sequence_lines.append(f"        self.scene_{i}()")
        
        return '\n'.join(sequence_lines)


def process_large_document(pdf_path: Optional[str] = None,
                          pdf_bytes: Optional[BytesIO] = None,
                          text_input: str = "",
                          document_title: str = "",
                          api_key: Optional[str] = None) -> Tuple[MultiSceneStructure, str]:
    """
    Convenience function to process a large document into a multi-scene video.
    
    Args:
        pdf_path: Path to PDF file
        pdf_bytes: PDF file as BytesIO
        text_input: Additional text instructions
        document_title: Title for the document
        api_key: Gemini API key
        
    Returns:
        Tuple of (MultiSceneStructure, generated_manim_code)
    """
    processor = MultiSceneProcessor(api_key=api_key)
    
    # Process into multiple scenes
    multi_scene = processor.process_combined_input(
        pdf_path=pdf_path,
        pdf_bytes=pdf_bytes,
        text_input=text_input,
        document_title=document_title
    )
    
    # Generate combined code
    combined_code = processor.generate_combined_code(multi_scene)
    
    return multi_scene, combined_code


# Example usage and testing
if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    
    # Test with sample content
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        exit(1)
    
    # Test document chunking
    sample_content = """
    Introduction to Calculus
    
    Calculus is the mathematical study of continuous change. It has two major branches:
    differential calculus and integral calculus.
    
    Chapter 1: Limits
    
    A limit describes the behavior of a function as its input approaches a particular value.
    The formal definition uses epsilon-delta notation.
    
    Example: lim(x→0) sin(x)/x = 1
    
    Chapter 2: Derivatives
    
    The derivative measures the rate at which a function changes.
    If f(x) = x², then f'(x) = 2x.
    
    The derivative has many applications in physics, economics, and engineering.
    
    Chapter 3: Integration
    
    Integration is the reverse process of differentiation.
    The fundamental theorem of calculus connects derivatives and integrals.
    
    ∫ x² dx = x³/3 + C
    """
    
    try:
        multi_scene, code = process_large_document(
            text_input=sample_content,
            document_title="Calculus Introduction",
            api_key=api_key
        )
        
        print(f"Generated multi-scene structure:")
        print(f"Title: {multi_scene.title}")
        print(f"Total duration: {multi_scene.total_duration:.1f}s")
        print(f"Number of scenes: {len(multi_scene.scenes)}")
        
        for i, scene in enumerate(multi_scene.scenes):
            print(f"  Scene {i+1}: {scene.settings.title} ({scene.settings.duration:.1f}s)")
        
        print(f"\nGenerated code length: {len(code)} characters")
        
        # Save the generated code
        with open("multi_scene_video.py", "w") as f:
            f.write(code)
        print("✓ Saved combined code to multi_scene_video.py")
        
    except Exception as e:
        print(f"Test failed: {e}")
