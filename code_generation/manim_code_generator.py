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
        AnimationType.SHOW_CREATION: "Create",  # Updated to use Create (modern Manim API)
        AnimationType.UNCREATE: "Uncreate",
        AnimationType.WIGGLE: "Wiggle",
        AnimationType.INDICATE: "Indicate",
        AnimationType.FLASH: "Flash",
        AnimationType.CIRCUMSCRIBE: "Circumscribe"
    }
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-pro"):
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
            temperature=0.1  # Lower temperature for more consistent code generation
        )
        
        self.system_prompt = """You are an expert Manim code generator. Given structured scene data, generate complete, runnable Python code using the Manim Community Edition library.

CRITICAL REQUIREMENTS:
1. Always create a Scene class that inherits from Scene
2. Implement the construct() method
3. Use proper Manim classes and methods
4. Include all necessary imports
5. Handle timing correctly (delays, durations)
6. Use proper coordinate system (Manim uses [-7,7] for x, [-4,4] for y typically)
7. PREVENT TEXT OVERFLOW - Always use .set_max_width() for text objects
8. PREVENT OVERLAPPING - Space objects vertically with at least 0.8 units between them
9. USE APPROPRIATE FONT SIZES - Never exceed 36 for body text, 48 for titles

OBJECT TYPE MAPPINGS:
- "text" → Text("content")
- "mathtext" or "formula" → MathTex(r"content") 
- "circle" → Circle()
- "square" → Square()
- "rectangle" → Rectangle()
- "line" → Line(start, end)
- "arrow" → Arrow(start, end)

ANIMATION TYPE MAPPINGS (Modern Manim API):
- "write" → Write(object)
- "create" → Create(object)  # Use Create, NOT ShowCreation
- "show_creation" → Create(object)  # Use Create, NOT ShowCreation
- "fade_in" → FadeIn(object)
- "fade_out" → FadeOut(object)
- "transform" → Transform(from_obj, to_obj)
- "move_to" → object.animate.move_to(position)
- "shift" → object.animate.shift(offset)
- "rotate" → object.animate.rotate(angle)
- "scale" → object.animate.scale(factor)

MODERN MANIM API USAGE:
- Use font_size parameter in constructors: Text("content", font_size=24)
- NEVER use set_font_size() method (deprecated)
- For conditional checks, use != or == with numbers, NOT 'is not' or 'is'
- Example: if font_size != None: NOT if font_size is not None:

TEXT SIZING AND POSITIONING (CRITICAL):
- Frame dimensions: width=14 units (x: -7 to 7), height=8 units (y: -4 to 4)
- Safe text area: x: [-6, 6], y: [-3.5, 3.5] to avoid edge overflow
- Font sizes: 18 (small body), 24 (body), 32 (subtitle), 40 (title) - NEVER larger than 40
- For long text: ALWAYS use .set_max_width(11) to prevent horizontal overflow
- For multi-line text: use line_spacing=0.8 parameter
- Vertical spacing: minimum 0.8 units between text objects to prevent overlap
- Position titles at y=3.0 or y=3.5 (top area)
- Position body text between y=-2.5 and y=2.5 (center area)
- Position footnotes at y=-3.0 or y=-3.5 (bottom area)

TEXT WIDTH CONSTRAINTS (MANDATORY):
- Short text (< 20 chars): .set_max_width(12)
- Medium text (20-40 chars): .set_max_width(11)
- Long text (> 40 chars): .set_max_width(10)
- Very long text (> 60 chars): .set_max_width(9) and font_size=20 or smaller
- ALWAYS apply .set_max_width() immediately after creating text objects

POSITIONING GUIDELINES:
- Top area: y = 3.0 to 3.5 (for titles)
- Upper middle: y = 1.5 to 2.5 (for subtitles)
- Center: y = -0.5 to 0.5 (for main content)
- Lower middle: y = -1.5 to -2.5 (for secondary content)
- Bottom area: y = -3.0 to -3.5 (for footnotes)
- Horizontal: keep x between -6 and 6 for safety
- Vertical spacing: at least 0.8 units between objects

MANIM CONSTANTS AND SIZING:
- NEVER use DEFAULT_FONT_SIZE (deprecated) - use explicit values
- NEVER use FRAME_WIDTH or FRAME_HEIGHT (deprecated) - use explicit values
- Standard font sizes: 18 (small), 24 (medium), 32 (large), 40 (title) - MAX 40
- For frame dimensions: width is 14, height is 8

FORBIDDEN PATTERNS:
- DEFAULT_FONT_SIZE, FRAME_WIDTH, FRAME_HEIGHT constants
- Font sizes larger than 40
- Text without .set_max_width() constraint
- Objects positioned outside [-6, 6] x [-3.5, 3.5] safe area
- Vertical spacing less than 0.8 units between text objects
- Nested identical conditionals: if x > y: if x > y: (NEVER do this!)
- Double conditional checks with same condition
- Using 'is not None' with numeric contexts

REQUIRED PATTERNS:
- Use explicit font sizes: Text("content", font_size=24)
- ALWAYS use width constraints: text_obj.set_max_width(11)
- Space objects vertically: position objects at least 0.8 units apart
- Single conditional waits: if start_time > current_time: self.wait(start_time - current_time)
- Clean, non-redundant conditionals

TIMING REQUIREMENTS:
- NEVER use self.wait() with zero or negative durations
- Always use conditional waits: if start_time > current_time: self.wait(start_time - current_time)
- Track current_time variable to manage animation timeline
- Use proper timing calculations that prevent negative wait times
- NEVER repeat the same conditional check twice

CODE STRUCTURE:
```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create text objects with proper sizing and width constraints
        title = Text("Title", font_size=40)
        title.set_max_width(11)  # CRITICAL: Prevent overflow
        title.move_to([0, 3.0, 0])  # Top area
        title.set_color(WHITE)
        
        body_text = Text("Long body text that might overflow", font_size=24)
        body_text.set_max_width(10)  # CRITICAL: Prevent overflow
        body_text.move_to([0, 0, 0])  # Center area
        body_text.set_color(WHITE)
        
        # Ensure vertical spacing: at least 0.8 units between objects
        # Animation Timeline with proper timing
        current_time = 0.0
        
        # Only wait if there's time to wait (CRITICAL!)
        if 2.0 > current_time:
            self.wait(2.0 - current_time)
        self.play(Write(title), run_time=1.5)
        current_time = 3.5
        
        # Final wait (if needed)
        if 5.0 > current_time:
            self.wait(5.0 - current_time)
```

IMPORTANT: 
- Return ONLY valid Python code, no explanations
- Use proper Manim Community Edition syntax and conventions
- ALWAYS use conditional waits to prevent zero/negative durations
- ALWAYS use .set_max_width() on text objects to prevent overflow
- ALWAYS space objects at least 0.8 units apart vertically
- NEVER use font sizes larger than 40
- Use self.wait() for delays and final wait
- Use run_time parameter for animation durations
- NEVER use deprecated constants like DEFAULT_FONT_SIZE or FRAME_WIDTH"""

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
        
        # Fix import statement formatting
        code = self._fix_import_statements(code)
        
        # Fix modern Manim API issues (deprecated methods, syntax warnings)
        code = self._fix_modern_manim_api(code)
        
        # Normalize indentation
        code = self._normalize_indentation(code)
        
        # Validate and fix basic syntax issues
        code = self._validate_and_fix_syntax(code)
        
        return code
    
    def _normalize_indentation(self, code: str) -> str:
        """Normalize Python indentation to use 4 spaces consistently."""
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            if not line.strip():  # Empty line
                normalized_lines.append("")
                continue
                
            # Count leading whitespace
            stripped = line.lstrip()
            if not stripped:  # Line with only whitespace
                normalized_lines.append("")
                continue
                
            # Calculate indentation level (assuming 4 spaces per level)
            original_indent = len(line) - len(stripped)
            
            # Convert tabs to spaces and normalize irregular spacing
            if '\t' in line:
                # Replace tabs with 4 spaces
                line = line.expandtabs(4)
                stripped = line.lstrip()
                original_indent = len(line) - len(stripped)
            
            # Normalize to multiples of 4
            indent_level = (original_indent + 2) // 4  # Round to nearest level
            new_indent = '    ' * indent_level  # 4 spaces per level
            
            normalized_lines.append(new_indent + stripped)
        
        return '\n'.join(normalized_lines)
    
    def _fix_import_statements(self, code: str) -> str:
        """Fix common import statement formatting issues."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix concatenated imports like "from manim import *import numpy as np"
            if "from manim import *import" in line:
                # Split on the first occurrence of "import" after the "*"
                star_pos = line.find("*")
                after_star = line[star_pos+1:]
                if "import" in after_star:
                    # Split the part after "*"
                    before_star = line[:star_pos+1]  # "from manim import *"
                    import_part = after_star[after_star.find("import"):]  # "import numpy as np"
                    
                    fixed_lines.append(before_star)
                    fixed_lines.append(import_part)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_modern_manim_api(self, code: str) -> str:
        """Fix deprecated Manim API usage for modern versions."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix deprecated set_font_size() calls
            if '.set_font_size(' in line:
                # Replace with font_size in constructor or skip if already constructed
                import re
                # Look for pattern like: obj.set_font_size(1.2 * DEFAULT_FONT_SIZE)
                match = re.search(r'(\w+)\.set_font_size\(([^)]+)\)', line)
                if match:
                    obj_name = match.group(1)
                    font_size_expr = match.group(2)
                    # Convert to font_size attribute setting
                    indent = len(line) - len(line.lstrip())
                    spacing = ' ' * indent
                    fixed_line = f"{spacing}{obj_name}.font_size = {font_size_expr}"
                    fixed_lines.append(fixed_line)
                    continue
            
            # Fix DEFAULT_FONT_SIZE references
            if 'DEFAULT_FONT_SIZE' in line:
                import re
                # Replace multiplications with DEFAULT_FONT_SIZE
                line = re.sub(r'(\d*\.?\d*)\s*\*\s*DEFAULT_FONT_SIZE', r'\1 * 24', line)
                # Replace standalone DEFAULT_FONT_SIZE
                line = line.replace('DEFAULT_FONT_SIZE', '24')
            
            # Fix FRAME_WIDTH references
            if 'FRAME_WIDTH' in line:
                import re
                line = line.replace('FRAME_WIDTH - 1', '13')
                line = line.replace('FRAME_WIDTH - 2', '12')
                line = line.replace('FRAME_WIDTH', '14')
            
            # Fix FRAME_HEIGHT references
            if 'FRAME_HEIGHT' in line:
                line = line.replace('FRAME_HEIGHT', '8')
            
            # Fix 'is not' with float literals
            if 'is not None' in line and any(f in line for f in ['.0', '.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9']):
                # Replace 'is not None' with '!= None' when used with numeric context
                import re
                # Pattern like: if 1.2 is not None:
                line = re.sub(r'(\d+\.?\d*)\s+is\s+not\s+None', r'\1 != None', line)
            
            # Fix ShowCreation references
            if 'ShowCreation(' in line:
                line = line.replace('ShowCreation(', 'Create(')
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _validate_and_fix_syntax(self, code: str) -> str:
        """Basic syntax validation and common error fixes."""
        # First fix timing calculation issues
        code = self._fix_timing_calculations(code)
        
        # Fix redundant conditionals
        code = self._fix_redundant_conditionals(code)
        
        # Fix text overflow and sizing issues
        code = self._fix_text_overflow_and_sizing(code)
        
        # Apply modern API fixes again (in case timing fixes introduced issues)
        code = self._fix_modern_manim_api(code)
        
        try:
            # Try to compile the code to check for syntax errors
            compile(code, '<string>', 'exec')
            return code
        except SyntaxError as e:
            print(f"Syntax error detected: {e}")
            
            # Try some common fixes
            lines = code.split('\n')
            
            # Fix common indentation errors around class/function definitions
            fixed_lines = []
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    # Ensure proper indentation for function/class definitions
                    if not line.startswith('def ') and not line.startswith('class '):
                        # It's indented incorrectly - fix it
                        stripped = line.strip()
                        if i > 0 and lines[i-1].strip().endswith(':'):
                            # It should be indented
                            fixed_lines.append('    ' + stripped)
                        else:
                            # It should not be indented
                            fixed_lines.append(stripped)
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            
            return '\n'.join(fixed_lines)
        except Exception:
            # If we can't fix it, return as is
            return code
    
    def _fix_timing_calculations(self, code: str) -> str:
        """Fix timing calculation issues in generated code."""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Look for problematic self.wait(time - current_time) patterns
            if 'self.wait(' in line and ' - current_time' in line:
                # Extract the timing calculation
                import re
                match = re.search(r'self\.wait\(([0-9.]+)\s*-\s*current_time\)', line)
                if match:
                    start_time = match.group(1)
                    indent = len(line) - len(line.lstrip())
                    spacing = ' ' * indent
                    
                    # Replace with conditional wait
                    fixed_line = f"{spacing}if {start_time} > current_time:"
                    fixed_lines.append(fixed_line)
                    fixed_lines.append(f"{spacing}    self.wait({start_time} - current_time)")
                    continue
            
            # Look for final wait patterns
            if 'self.wait(' in line and ' - current_time)' in line and 'if ' not in line:
                import re
                match = re.search(r'self\.wait\(([0-9.]+)\s*-\s*current_time\)', line)
                if match:
                    end_time = match.group(1)
                    indent = len(line) - len(line.lstrip())
                    spacing = ' ' * indent
                    
                    # Replace with conditional wait
                    fixed_line = f"{spacing}if {end_time} > current_time:"
                    fixed_lines.append(fixed_line)
                    fixed_lines.append(f"{spacing}    self.wait({end_time} - current_time)")
                    continue
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_redundant_conditionals(self, code: str) -> str:
        """Fix redundant conditional statements that appear in generated code."""
        lines = code.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for redundant identical conditionals
            if line.strip().startswith('if ') and i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Check if the next line has the same condition
                if (line.strip() == next_line.strip() and 
                    line.strip().startswith('if ') and 
                    next_line.strip().startswith('if ')):
                    # Skip the redundant line
                    fixed_lines.append(line)
                    i += 2  # Skip the duplicate
                    continue
                
                # Check for nested identical conditions
                if (line.strip().endswith(':') and 
                    i + 1 < len(lines) and 
                    next_line.strip() == line.strip()):
                    # This is a duplicate condition, skip the second one
                    fixed_lines.append(line)
                    i += 2  # Skip the duplicate
                    continue
            
            # Check for pattern: if condition: if condition:
            if 'if ' in line and line.count('if ') > 1:
                import re
                # Extract the condition to check for duplicates
                match = re.search(r'if\s+(.+?):\s*if\s+(.+?):', line)
                if match:
                    cond1 = match.group(1).strip()
                    cond2 = match.group(2).strip()
                    if cond1 == cond2:
                        # Remove the duplicate condition
                        line = re.sub(r'if\s+(.+?):\s*if\s+\1:', r'if \1:', line)
            
            fixed_lines.append(line)
            i += 1
        
        return '\n'.join(fixed_lines)
    
    def _fix_text_overflow_and_sizing(self, code: str) -> str:
        """Fix text overflow, oversized fonts, and overlapping issues."""
        import re
        lines = code.split('\n')
        fixed_lines = []
        text_objects = {}  # Track text objects: {name: {'has_max_width': bool, 'y_pos': float}}
        text_y_positions = []  # Track all y positions to prevent overlap
        
        # First pass: Fix font sizes and detect text objects
        i = 0
        while i < len(lines):
            line = lines[i]
            indent = len(line) - len(line.lstrip())
            spacing = ' ' * indent
            
            # Fix oversized font sizes in constructors
            if 'font_size=' in line:
                font_size_match = re.search(r'font_size\s*=\s*(\d+)', line)
                if font_size_match:
                    font_size = int(font_size_match.group(1))
                    if font_size > 40:
                        line = re.sub(r'font_size\s*=\s*\d+', 'font_size=40', line)
            
            # Fix font sizes in assignments
            font_size_assign_match = re.search(r'(\w+)\.font_size\s*=\s*(\d+)', line)
            if font_size_assign_match:
                font_size = int(font_size_assign_match.group(2))
                if font_size > 40:
                    line = re.sub(r'font_size\s*=\s*\d+', 'font_size=40', line)
            
            # Detect text object creation
            text_match = re.search(r'(\w+)\s*=\s*(Text|MathTex)\(', line)
            if text_match:
                obj_name = text_match.group(1)
                
                # Extract text content and font size
                text_content_match = re.search(r'(?:Text|MathTex)\([r]?["\']([^"\']+)["\']', line)
                text_length = len(text_content_match.group(1)) if text_content_match else 0
                
                font_size_match = re.search(r'font_size\s*=\s*(\d+)', line)
                font_size = int(font_size_match.group(1)) if font_size_match else 24
                
                # Initialize tracking
                text_objects[obj_name] = {
                    'has_max_width': False,
                    'text_length': text_length,
                    'font_size': font_size
                }
                
                fixed_lines.append(line)
                i += 1
                
                # Check next 10 lines for existing .set_max_width()
                has_max_width = False
                for j in range(i, min(i + 10, len(lines))):
                    if f'{obj_name}.set_max_width' in lines[j]:
                        has_max_width = True
                        text_objects[obj_name]['has_max_width'] = True
                        break
                
                # Add .set_max_width() if missing
                if not has_max_width and text_length > 0:
                    # Determine max_width based on text length and font size
                    if text_length > 60 or font_size > 32:
                        max_width = 9
                    elif text_length > 40 or font_size > 28:
                        max_width = 10
                    elif text_length > 20:
                        max_width = 11
                    else:
                        max_width = 12
                    
                    fixed_lines.append(f"{spacing}{obj_name}.set_max_width({max_width})")
                    text_objects[obj_name]['has_max_width'] = True
                
                continue
            
            fixed_lines.append(line)
            i += 1
        
        # Second pass: Fix positioning to prevent overlap and ensure safe bounds
        final_lines = []
        i = 0
        
        while i < len(fixed_lines):
            line = fixed_lines[i]
            
            # Check for move_to and adjust positions
            move_to_match = re.search(r'(\w+)\.move_to\(\[([-\d.]+),\s*([-\d.]+)', line)
            if move_to_match:
                obj_name = move_to_match.group(1)
                x_pos = float(move_to_match.group(2))
                y_pos = float(move_to_match.group(3))
                
                # Clamp x to safe area [-6, 6]
                if x_pos > 6:
                    x_pos = 6
                elif x_pos < -6:
                    x_pos = -6
                
                # Clamp y to safe area [-3.5, 3.5]
                if y_pos > 3.5:
                    y_pos = 3.5
                elif y_pos < -3.5:
                    y_pos = -3.5
                
                # Adjust y position to prevent overlap with other text objects
                if obj_name in text_objects:
                    min_spacing = 0.8
                    adjusted_y = y_pos
                    
                    # Check against existing positions
                    for existing_y in text_y_positions:
                        if abs(y_pos - existing_y) < min_spacing:
                            # Too close, adjust downward (prefer lower positions)
                            if y_pos > existing_y:
                                adjusted_y = existing_y + min_spacing
                            else:
                                adjusted_y = existing_y - min_spacing
                            # Re-clamp after adjustment
                            if adjusted_y > 3.5:
                                adjusted_y = 3.5
                            elif adjusted_y < -3.5:
                                adjusted_y = -3.5
                            break
                    
                    # Update line with adjusted position
                    line = re.sub(
                        r'(\w+)\.move_to\(\[([-\d.]+),\s*([-\d.]+)',
                        f'{obj_name}.move_to([{x_pos:.2f}, {adjusted_y:.2f}',
                        line
                    )
                    
                    text_y_positions.append(adjusted_y)
                    text_objects[obj_name]['y_pos'] = adjusted_y
            
            final_lines.append(line)
            i += 1
        
        return '\n'.join(final_lines)


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
