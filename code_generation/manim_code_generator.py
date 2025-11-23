"""
Manim Code Generator Module

Converts structured scene descriptions into executable Manim Python code.
Uses LLM to generate clean, idiomatic Manim code from CodeGenerationContext.
"""

import os
import json
import sys
from typing import Dict, List, Optional, Any
from dataclasses import asdict

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.scene_parser import CodeGenerationContext, SceneParser
from data_processing.scene_structure import SceneStructure, ObjectType, AnimationType
from models.llm import LLM


class ManimCodeGenerator:
    """Generates Manim Python code from structured scene descriptions."""
    
    # Mapping from ObjectType to Manim classes
    OBJECT_TYPE_MAPPING = {
        ObjectType.TEXT: "Text",
        ObjectType.MATHTEXT: "MathTex",
        ObjectType.FORMULA: "MathTex",
        ObjectType.CIRCLE: "Circle",
        ObjectType.SQUARE: "Square", 
        ObjectType.RECTANGLE: "Rectangle",
        ObjectType.LINE: "Line",
        ObjectType.ARROW: "Arrow",
        ObjectType.POLYGON: "Polygon",
        ObjectType.AXES: "Axes",
        ObjectType.GRAPH: "FunctionGraph",
        ObjectType.IMAGE: "ImageMobject",
        ObjectType.GROUP: "VGroup"
    }
    
    # Mapping from AnimationType to Manim animation methods
    ANIMATION_TYPE_MAPPING = {
        AnimationType.CREATE: "Create",
        AnimationType.WRITE: "Write",
        AnimationType.DRAW_BORDER_THEN_FILL: "DrawBorderThenFill",
        AnimationType.FADE_IN: "FadeIn",
        AnimationType.FADE_OUT: "FadeOut",
        AnimationType.TRANSFORM: "Transform",
        AnimationType.REPLACE_TRANSFORM: "ReplacementTransform",
        AnimationType.MOVE_TO: "move_to",  # This is a method, not animation class
        AnimationType.SHIFT: "shift",      # This is a method, not animation class
        AnimationType.ROTATE: "rotate",    # This is a method, not animation class
        AnimationType.SCALE: "scale",      # This is a method, not animation class
        AnimationType.SHOW_CREATION: "ShowCreation",
        AnimationType.UNCREATE: "Uncreate",
        AnimationType.WIGGLE: "Wiggle",
        AnimationType.INDICATE: "Indicate",
        AnimationType.FLASH: "Flash",
        AnimationType.CIRCUMSCRIBE: "Circumscribe"
    }
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the ManimCodeGenerator.
        
        Args:
            api_key: Gemini API key. If None, will try to get from GOOGLE_API_KEY env var.
            model_name: Gemini model to use for code generation
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.llm = LLM(
            provider="google_genai",
            model_name=model_name,
            api_key=self.api_key,
            temperature=0.3  # Lower temperature for more consistent code generation
        )
        
        self.system_prompt = """You are an expert Manim code generator. Given structured scene data, generate complete, runnable Python code using the Manim library.

CRITICAL REQUIREMENTS:
1. Always create a Scene class that inherits from Scene
2. Implement the construct() method
3. Use proper Manim classes and methods
4. Include all necessary imports
5. Handle timing correctly (delays, durations)
6. Use proper coordinate system (Manim uses [-7,7] for x, [-4,4] for y typically)

OBJECT TYPE MAPPINGS:
- "text" → Text("content")
- "mathtext" or "formula" → MathTex(r"content") 
- "circle" → Circle()
- "square" → Square()
- "rectangle" → Rectangle()
- "line" → Line(start, end)
- "arrow" → Arrow(start, end)

ANIMATION TYPE MAPPINGS:
- "write" → Write(object)
- "create" → Create(object)
- "fade_in" → FadeIn(object)
- "fade_out" → FadeOut(object)
- "transform" → Transform(from_obj, to_obj)
- "move_to" → object.animate.move_to(position)
- "shift" → object.animate.shift(offset)
- "rotate" → object.animate.rotate(angle)
- "scale" → object.animate.scale(factor)

CODE STRUCTURE:
```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create objects
        obj1 = MathTex(r"formula")
        obj1.move_to([x, y, z])
        obj1.set_color(COLOR)
        
        # Animate with proper timing
        self.wait(delay)
        self.play(Animation(obj), run_time=duration)
        self.wait()
```

IMPORTANT: 
- Return ONLY valid Python code, no explanations
- Use proper Manim syntax and conventions
- Handle all timing (delays between animations)
- Use self.wait() for delays and final wait
- Use run_time parameter for animation durations"""

    def generate_code(self, context: CodeGenerationContext) -> str:
        """
        Generate Manim Python code from a CodeGenerationContext.
        
        Args:
            context: Parsed scene context containing objects and animations
            
        Returns:
            Complete Python code string ready to execute with Manim
        """
        try:
            # Prepare structured data for the LLM
            scene_data = self._prepare_scene_data(context)
            
            # Create the prompt
            user_prompt = f"""Generate complete Manim code for this scene:

Scene Title: {context.scene_title}
Description: {context.scene_description}
Duration: {context.total_duration}s
Background: {context.background_color}

Objects:
{json.dumps(scene_data['objects'], indent=2)}

Animations (in chronological order):
{json.dumps(scene_data['animations'], indent=2)}

Animation Timeline:
{json.dumps(scene_data['timeline'], indent=2)}

Generate complete, runnable Python code using Manim."""
            
            # Generate code using LLM
            chat = self.llm.create_chat()
            messages = [
                ("system", self.system_prompt),
                ("user", user_prompt)
            ]
            
            response = chat.invoke(messages)
            
            # Extract code from response
            raw_code = response.content if hasattr(response, 'content') else str(response)
            
            # Clean up the code
            cleaned_code = self._clean_code(raw_code)
            
            return cleaned_code
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate Manim code: {str(e)}") from e
    
    def generate_code_template(self, context: CodeGenerationContext) -> str:
        """
        Generate a basic code template without using LLM (fallback method).
        
        Args:
            context: Parsed scene context
            
        Returns:
            Basic Manim code template
        """
        imports = "\n".join(context.get_imports_needed if hasattr(context, 'get_imports_needed') else ["from manim import *"])
        
        code_lines = [
            imports,
            "",
            f"class GeneratedScene(Scene):",
            f'    """',
            f'    {context.scene_title}',
            f'    {context.scene_description}',
            f'    """',
            f"    def construct(self):",
            f"        # Scene duration: {context.total_duration}s",
            f"        # Background color: {context.background_color}",
            "",
            "        # Create objects"
        ]
        
        # Add object creation
        all_objects = (context.text_objects + context.shape_objects + 
                      context.math_objects + context.line_objects + context.graph_objects)
        
        for obj in all_objects:
            manim_class = self.OBJECT_TYPE_MAPPING.get(obj.type, "Text")
            
            if obj.type in [ObjectType.MATHTEXT, ObjectType.FORMULA]:
                content = f'r"{obj.text_content}"' if obj.text_content else '""'
            elif obj.type == ObjectType.TEXT:
                content = f'"{obj.text_content}"' if obj.text_content else '""'
            else:
                content = ""
            
            if content:
                code_lines.append(f"        {obj.id} = {manim_class}({content})")
            else:
                code_lines.append(f"        {obj.id} = {manim_class}()")
            
            # Add positioning
            pos = obj.position
            code_lines.append(f"        {obj.id}.move_to([{pos.x}, {pos.y}, {pos.z}])")
            
            # Add color
            if obj.color and obj.color.name:
                code_lines.append(f"        {obj.id}.set_color({obj.color.name})")
        
        code_lines.extend([
            "",
            "        # Animations"
        ])
        
        # Add animations in timeline order
        for start_time, anim in context.animation_timeline:
            if start_time > 0:
                code_lines.append(f"        self.wait({start_time})  # delay")
            
            anim_method = self.ANIMATION_TYPE_MAPPING.get(anim.type, "Create")
            target_obj = anim.target_objects[0] if anim.target_objects else "obj"
            
            if anim.type in [AnimationType.MOVE_TO, AnimationType.SHIFT, AnimationType.ROTATE, AnimationType.SCALE]:
                # These use .animate
                code_lines.append(f"        self.play({target_obj}.animate.{anim_method}(...), run_time={anim.duration})")
            else:
                # These are animation classes
                code_lines.append(f"        self.play({anim_method}({target_obj}), run_time={anim.duration})")
        
        code_lines.append("        self.wait()  # final wait")
        
        return "\n".join(code_lines)
    
    def _prepare_scene_data(self, context: CodeGenerationContext) -> Dict[str, Any]:
        """Prepare scene data for LLM consumption."""
        # Collect all objects
        all_objects = (context.text_objects + context.shape_objects + 
                      context.math_objects + context.line_objects + context.graph_objects)
        
        objects_data = []
        for obj in all_objects:
            objects_data.append({
                "id": obj.id,
                "type": obj.type.value,
                "manim_class": self.OBJECT_TYPE_MAPPING.get(obj.type, "Text"),
                "text_content": obj.text_content,
                "position": [obj.position.x, obj.position.y, obj.position.z],
                "color": obj.color.name if obj.color and obj.color.name else None,
                "size": obj.size,
                "opacity": obj.opacity
            })
        
        # Collect all animations
        all_animations = (context.creation_animations + context.transformation_animations + 
                         context.movement_animations + context.style_animations)
        
        animations_data = []
        for anim in all_animations:
            animations_data.append({
                "id": anim.id,
                "type": anim.type.value,
                "manim_method": self.ANIMATION_TYPE_MAPPING.get(anim.type, "Create"),
                "target_objects": anim.target_objects,
                "duration": anim.duration,
                "delay": anim.delay,
                "target_position": [anim.target_position.x, anim.target_position.y, anim.target_position.z] if anim.target_position else None,
                "from_object": anim.from_object,
                "to_object": anim.to_object
            })
        
        # Timeline data
        timeline_data = []
        for start_time, anim in context.animation_timeline:
            timeline_data.append({
                "start_time": start_time,
                "animation_id": anim.id,
                "animation_type": anim.type.value,
                "targets": anim.target_objects,
                "duration": anim.duration
            })
        
        return {
            "objects": objects_data,
            "animations": animations_data,
            "timeline": timeline_data
        }
    
    def _clean_code(self, raw_code: str) -> str:
        """Clean up generated code by removing markdown and extra formatting."""
        code = raw_code.strip()
        
        # Remove markdown code blocks
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        
        if code.endswith("```"):
            code = code[:-3]
        
        code = code.strip()
        
        # Ensure proper imports if missing
        if "from manim import" not in code and "import manim" not in code:
            code = "from manim import *\n\n" + code
        
        return code


def generate_manim_code(scene_structure: SceneStructure, api_key: Optional[str] = None) -> str:
    """
    Convenience function to generate Manim code from a SceneStructure.
    
    Args:
        scene_structure: SceneStructure object to convert
        api_key: Optional Gemini API key
        
    Returns:
        Generated Manim Python code
    """
    # Parse the scene structure
    parser = SceneParser()
    context = parser.parse(scene_structure)
    
    # Generate code
    generator = ManimCodeGenerator(api_key=api_key)
    code = generator.generate_code(context)
    
    return code


# Example usage and testing
if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    
    from data_processing.input_processor import InputProcessor
    
    # Test with the input processor pipeline
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        exit(1)
    
    # Create a scene from text input
    processor = InputProcessor(api_key=api_key)
    scene_structure = processor.process_text_input("Show the binomial theorem: (a+b)^2 = a^2 + 2ab + b^2")
    
    # Generate Manim code
    generator = ManimCodeGenerator(api_key=api_key)
    parser = SceneParser()
    context = parser.parse(scene_structure)
    
    print("=== Generated Manim Code ===")
    try:
        code = generator.generate_code(context)
        print(code)
    except Exception as e:
        print(f"LLM generation failed: {e}")
        print("\n=== Fallback Template Code ===")
        code = generator.generate_code_template(context)
        print(code)
