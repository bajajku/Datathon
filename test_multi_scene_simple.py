"""
Simple test for multi-scene processing to debug issues.
"""

import os
import sys
from pathlib import Path

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from data_processing.multi_scene_processor import process_large_document


def test_simple_multi_scene():
    """Test multi-scene processing with simple content."""
    print("=== Simple Multi-Scene Test ===")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not set")
        return False
    
    # Very simple content that should work
    simple_content = """
    Chapter 1: Addition
    Addition is combining numbers. 2 + 3 = 5.
    
    Chapter 2: Subtraction  
    Subtraction is taking away. 5 - 3 = 2.
    
    Chapter 3: Multiplication
    Multiplication is repeated addition. 3 × 4 = 12.
    """
    
    try:
        print("Processing simple document...")
        
        multi_scene, code = process_large_document(
            text_input=simple_content,
            document_title="Basic Math",
            api_key=api_key
        )
        
        print(f"✓ Success! Created {len(multi_scene.scenes)} scenes")
        print(f"  Total duration: {multi_scene.total_duration:.1f}s")
        
        for i, scene in enumerate(multi_scene.scenes):
            print(f"  Scene {i+1}: {scene.settings.title}")
        
        print(f"  Generated code: {len(code)} characters")
        
        with open("simple_multi_scene.py", "w") as f:
            f.write(code)
        print("✓ Saved to simple_multi_scene.py")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_simple_multi_scene()
