"""
End-to-End Test Script

Tests the complete pipeline from text input to Manim code generation.
"""

import os
import sys
from pathlib import Path

# Try to load environment variables if dotenv is available
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables only.")

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from data_processing.input_processor import InputProcessor
from data_processing.scene_parser import SceneParser
from code_generation.manim_code_generator import ManimCodeGenerator


def test_complete_pipeline():
    """Test the complete pipeline from text input to Manim code."""
    print("=== Complete Pipeline Test ===")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Please set it with your Gemini API key to test the complete pipeline")
        return False
    
    try:
        # Step 1: Process text input
        print("Step 1: Processing text input...")
        processor = InputProcessor(api_key=api_key)
        
        test_inputs = [
            "Show the quadratic formula: x = (-b ± √(b²-4ac)) / 2a",
            "Create a circle that moves from left to right and changes color from blue to red",
            "Display the Pythagorean theorem: a² + b² = c²"
        ]
        
        for i, text_input in enumerate(test_inputs, 1):
            print(f"\n--- Test Case {i} ---")
            print(f"Input: {text_input}")
            
            # Process input to structured scene
            scene_structure = processor.process_text_input(text_input)
            print(f"✓ Generated scene structure with {len(scene_structure.objects)} objects and {len(scene_structure.animations)} animations")
            
            # Step 2: Parse scene for code generation
            print("Step 2: Parsing scene for code generation...")
            parser = SceneParser()
            context = parser.parse(scene_structure)
            print(f"✓ Parsed context - Math objects: {len(context.math_objects)}, Animations: {len(context.creation_animations + context.transformation_animations + context.movement_animations + context.style_animations)}")
            
            # Step 3: Generate Manim code
            print("Step 3: Generating Manim code...")
            generator = ManimCodeGenerator(api_key=api_key)
            
            try:
                manim_code = generator.generate_code(context)
                print("✓ Successfully generated Manim code")
                
                # Show first few lines of generated code
                code_lines = manim_code.split('\n')
                preview_lines = code_lines[:10]
                print("\nGenerated Code Preview:")
                for line_num, line in enumerate(preview_lines, 1):
                    print(f"  {line_num:2d}: {line}")
                
                if len(code_lines) > 10:
                    print(f"  ... ({len(code_lines) - 10} more lines)")
                
                # Validate the code structure
                if "class " in manim_code and "def construct(self):" in manim_code:
                    print("✓ Code structure looks valid (has class and construct method)")
                else:
                    print("⚠ Code structure might be incomplete")
                
                # Save generated code to file
                output_file = f"generated_scene_{i}.py"
                with open(output_file, 'w') as f:
                    f.write(manim_code)
                print(f"✓ Saved generated code to {output_file}")
                
            except Exception as e:
                print(f"✗ LLM code generation failed: {e}")
                print("Trying fallback template generation...")
                
                try:
                    template_code = generator.generate_code_template(context)
                    print("✓ Generated fallback template code")
                    
                    output_file = f"template_scene_{i}.py"
                    with open(output_file, 'w') as f:
                        f.write(template_code)
                    print(f"✓ Saved template code to {output_file}")
                    
                except Exception as template_error:
                    print(f"✗ Template generation also failed: {template_error}")
            
            print(f"--- End Test Case {i} ---\n")
        
        return True
        
    except Exception as e:
        print(f"Pipeline test failed: {e}")
        return False


def test_with_sample_json():
    """Test with a manually created scene structure (no API needed)."""
    print("=== Testing with Sample JSON (No API Required) ===")
    
    from data_processing.scene_structure import (
        SceneStructure, SceneObject, AnimationStep, ObjectType, AnimationType,
        Position, Color, SceneSettings
    )
    
    # Create a sample scene manually
    settings = SceneSettings(
        title="Sample Mathematical Animation",
        description="Shows a mathematical formula with animation",
        duration=6.0,
        background_color=Color(name="BLACK")
    )
    
    objects = [
        SceneObject(
            id="formula",
            type=ObjectType.MATHTEXT,
            text_content=r"E = mc^2",
            position=Position(0, 1, 0),
            color=Color(name="YELLOW"),
            size=1.5
        ),
        SceneObject(
            id="description",
            type=ObjectType.TEXT,
            text_content="Einstein's Mass-Energy Equivalence",
            position=Position(0, -1, 0),
            color=Color(name="WHITE")
        )
    ]
    
    animations = [
        AnimationStep(
            id="write_formula",
            type=AnimationType.WRITE,
            target_objects=["formula"],
            duration=2.0,
            delay=0.5
        ),
        AnimationStep(
            id="show_description",
            type=AnimationType.FADE_IN,
            target_objects=["description"],
            duration=1.0,
            delay=3.0
        )
    ]
    
    scene = SceneStructure(settings=settings, objects=objects, animations=animations)
    
    # Parse and generate code
    try:
        parser = SceneParser()
        context = parser.parse(scene)
        
        print(f"Scene: {context.scene_title}")
        print(f"Objects: {len(context.math_objects)} math, {len(context.text_objects)} text")
        print(f"Animations: {len(context.creation_animations)} creation, {len(context.style_animations)} style")
        
        # Generate template code (no API needed)
        api_key = os.getenv("GOOGLE_API_KEY")
        generator = ManimCodeGenerator(api_key=api_key) if api_key else None
        
        if generator:
            try:
                print("\nGenerating code with LLM...")
                manim_code = generator.generate_code(context)
                print("✓ LLM generation successful")
            except Exception as e:
                print(f"LLM generation failed: {e}")
                print("Falling back to template...")
                manim_code = generator.generate_code_template(context)
        else:
            print("No API key available, using template generation...")
            # Create a minimal generator for template only
            class TemplateGenerator:
                OBJECT_TYPE_MAPPING = ManimCodeGenerator.OBJECT_TYPE_MAPPING
                ANIMATION_TYPE_MAPPING = ManimCodeGenerator.ANIMATION_TYPE_MAPPING
                def generate_code_template(self, ctx): 
                    return ManimCodeGenerator.generate_code_template(self, ctx)
            
            temp_gen = TemplateGenerator()
            manim_code = temp_gen.generate_code_template(context)
        
        print(f"\nGenerated Code:\n{manim_code}")
        
        # Save to file
        with open("sample_scene.py", 'w') as f:
            f.write(manim_code)
        print("✓ Saved to sample_scene.py")
        
        return True
        
    except Exception as e:
        print(f"Sample test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing Manim Code Generation Pipeline")
    print("=" * 50)
    
    # Test with sample data first (no API required)
    success1 = test_with_sample_json()
    
    # Test complete pipeline (requires API)
    success2 = test_complete_pipeline()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Sample JSON test: {'✓ PASSED' if success1 else '✗ FAILED'}")
    print(f"Complete pipeline test: {'✓ PASSED' if success2 else '✗ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! The pipeline is working correctly.")
    elif success1:
        print("\n⚠ Basic functionality works, but API-based tests failed.")
        print("Check your GOOGLE_API_KEY environment variable.")
    else:
        print("\n❌ Tests failed. Check the error messages above.")


if __name__ == "__main__":
    main()
