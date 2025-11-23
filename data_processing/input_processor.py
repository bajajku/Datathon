"""
Input Processor Module

Processes unstructured inputs (text, PDF) using Gemini API to create
structured prompts suitable for Manim scene generation.
"""

import os
from typing import Optional
from io import BytesIO
import sys
import json

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.llm import LLM
from .scene_structure import SceneStructure, ObjectType, AnimationType

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_AVAILABLE = True
        PDF_LIBRARY = 'pdfplumber'
    except ImportError:
        PDF_AVAILABLE = False
        PDF_LIBRARY = None
else:
    PDF_LIBRARY = 'PyPDF2'


class InputProcessor:
    """Processes various input types and converts them to structured prompts."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-pro"):
        """
        Initialize the InputProcessor.
        
        Args:
            api_key: Gemini API key. If None, will try to get from GOOGLE_API_KEY env var.
            model_name: Gemini model to use (default: gemini-pro)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.llm = LLM(
            provider="google_genai",
            model_name=model_name,
            api_key=self.api_key,
            temperature=0.7
        )
        
        self.system_prompt = """You are a content analyzer specialized in extracting visual and animation elements from text content for Manim animation generation.

Your task is to analyze the provided content and output a structured JSON description that follows this exact schema:

{
  "settings": {
    "title": "Scene title",
    "description": "Brief description", 
    "duration": 10.0,
    "background_color": {"name": "BLACK"},
    "camera_position": [0, 0, 0],
    "quality": "medium_quality",
    "resolution": "720p"
  },
  "objects": [
    {
      "id": "unique_id",
      "type": "text|circle|square|rectangle|line|arrow|mathtext|formula|etc",
      "properties": {},
      "position": [x, y, z],
      "color": {"name": "BLUE"},
      "text_content": "text if applicable",
      "size": 1.0,
      "opacity": 1.0,
      "layer": 0
    }
  ],
  "animations": [
    {
      "id": "anim_id",
      "type": "create|write|fade_in|move_to|transform|etc",
      "target_objects": ["object_id1"],
      "duration": 1.0,
      "delay": 0.0,
      "properties": {},
      "easing": "smooth"
    }
  ]
}

Available object types: text, circle, square, rectangle, line, arrow, polygon, axes, graph, mathtext, formula, image, group
Available animation types: create, write, draw_border_then_fill, fade_in, fade_out, transform, replace_transform, move_to, shift, rotate, scale, show_creation, uncreate, wiggle, indicate, flash, circumscribe

IMPORTANT: Return ONLY valid JSON following this exact structure. No explanations, no additional text, just the JSON object."""

    def process_text_input(self, text: str) -> SceneStructure:
        """
        Process plain text input and create a structured scene description.
        
        Args:
            text: Raw text input from user
            
        Returns:
            SceneStructure object suitable for Manim code generation
        """
        if not text or not text.strip():
            raise ValueError("Text input cannot be empty")
        
        return self._create_structured_prompt(text)
    
    def process_pdf_input(self, pdf_path: str) -> SceneStructure:
        """
        Extract text from PDF and process it to create a structured scene description.
        
        Args:
            pdf_path: Path to PDF file or file-like object
            
        Returns:
            SceneStructure object suitable for Manim code generation
        """
        if not PDF_AVAILABLE:
            raise ImportError(
                "PDF processing requires either PyPDF2 or pdfplumber. "
                "Install one with: pip install PyPDF2 or pip install pdfplumber"
            )
        
        # Extract text from PDF
        extracted_text = self._extract_text_from_pdf(pdf_path)
        
        if not extracted_text or not extracted_text.strip():
            raise ValueError("No text could be extracted from the PDF file")
        
        return self._create_structured_prompt(extracted_text)
    
    def process_pdf_bytes(self, pdf_bytes: BytesIO) -> SceneStructure:
        """
        Process PDF from bytes (useful for file uploads).
        
        Args:
            pdf_bytes: BytesIO object containing PDF data
            
        Returns:
            SceneStructure object suitable for Manim code generation
        """
        if not PDF_AVAILABLE:
            raise ImportError(
                "PDF processing requires either PyPDF2 or pdfplumber. "
                "Install one with: pip install PyPDF2 or pip install pdfplumber"
            )
        
        extracted_text = self._extract_text_from_pdf_bytes(pdf_bytes)
        
        if not extracted_text or not extracted_text.strip():
            raise ValueError("No text could be extracted from the PDF file")
        
        return self._create_structured_prompt(extracted_text)
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        if PDF_LIBRARY == 'PyPDF2':
            return self._extract_with_pypdf2(pdf_path)
        elif PDF_LIBRARY == 'pdfplumber':
            return self._extract_with_pdfplumber(pdf_path)
        else:
            raise ImportError("No PDF library available")
    
    def _extract_text_from_pdf_bytes(self, pdf_bytes: BytesIO) -> str:
        """Extract text from PDF bytes."""
        if PDF_LIBRARY == 'PyPDF2':
            return self._extract_with_pypdf2_bytes(pdf_bytes)
        elif PDF_LIBRARY == 'pdfplumber':
            return self._extract_with_pdfplumber_bytes(pdf_bytes)
        else:
            raise ImportError("No PDF library available")
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2."""
        text_parts = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
        return "\n".join(text_parts)
    
    def _extract_with_pypdf2_bytes(self, pdf_bytes: BytesIO) -> str:
        """Extract text from bytes using PyPDF2."""
        text_parts = []
        pdf_bytes.seek(0)  # Reset to beginning
        pdf_reader = PyPDF2.PdfReader(pdf_bytes)
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())
        return "\n".join(text_parts)
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber."""
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        return "\n".join(text_parts)
    
    def _extract_with_pdfplumber_bytes(self, pdf_bytes: BytesIO) -> str:
        """Extract text from bytes using pdfplumber."""
        import pdfplumber
        text_parts = []
        pdf_bytes.seek(0)  # Reset to beginning
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        return "\n".join(text_parts)
    
    def _create_structured_prompt(self, raw_content: str) -> SceneStructure:
        """
        Use Gemini API to structure the raw content into a SceneStructure object.
        
        Args:
            raw_content: Raw text content to be structured
            
        Returns:
            SceneStructure object containing the parsed scene description
        """
        try:
            chat = self.llm.create_chat()
            
            # Create messages for the chat
            messages = [
                ("system", self.system_prompt),
                ("user", f"Analyze the following content and create a structured scene description:\n\n{raw_content}")
            ]
            
            # Invoke the LLM
            response = chat.invoke(messages)
            
            # Extract the content from the response
            # LangChain typically returns AIMessage objects with .content attribute
            if hasattr(response, 'content'):
                structured_prompt = response.content
            elif hasattr(response, 'text'):
                structured_prompt = response.text
            elif isinstance(response, str):
                structured_prompt = response
            else:
                # Fallback: convert to string
                structured_prompt = str(response)
            
            if not structured_prompt:
                raise ValueError("Received empty response from Gemini API")
            
            # Clean up the response - sometimes LLMs add markdown code blocks
            json_str = structured_prompt.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()
            
            # Parse JSON and create SceneStructure
            try:
                scene_data = json.loads(json_str)
                scene_structure = SceneStructure.from_dict(scene_data)
                return scene_structure
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON response from Gemini API: {str(e)}\nResponse: {json_str[:500]}...") from e
            except Exception as e:
                raise ValueError(f"Failed to create SceneStructure from response: {str(e)}") from e
            
        except Exception as e:
            raise RuntimeError(f"Failed to create structured prompt using Gemini API: {str(e)}") from e


def process_input(input_type: str, input_data: str, api_key: Optional[str] = None) -> SceneStructure:
    """
    Convenience function to process input based on type.
    
    Args:
        input_type: Type of input ('text' or 'pdf')
        input_data: The input data (text string or PDF file path)
        api_key: Optional Gemini API key
        
    Returns:
        SceneStructure object containing the parsed scene description
    """
    processor = InputProcessor(api_key=api_key)
    
    if input_type.lower() == 'text':
        return processor.process_text_input(input_data)
    elif input_type.lower() == 'pdf':
        return processor.process_pdf_input(input_data)
    else:
        raise ValueError(f"Unsupported input type: {input_type}. Use 'text' or 'pdf'")


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    GOOGLE_API_KEY = dotenv.get_key(".env", "GOOGLE_API_KEY")
    processor = InputProcessor(api_key=GOOGLE_API_KEY)
    result = processor.process_text_input("(a+b)^2 = a^2 + 2ab + b^2")
    print("Generated Scene Structure:")
    print(result.to_json())