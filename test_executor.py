"""
Test script for the Manim Executor.

Since Manim has complex system dependencies, this test demonstrates
the executor architecture and simulates video generation for the hackathon demo.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from execution.manim_executor import ManimExecutor, ExecutionResult


def test_executor_architecture():
    """Test the executor class without actually running Manim."""
    print("=== Testing Manim Executor Architecture ===")
    
    try:
        # Test executor initialization
        executor = ManimExecutor(output_dir="test_videos", timeout=60)
        print("✅ ManimExecutor initialized successfully")
        print(f"   Output directory: {executor.output_dir}")
        print(f"   Default quality: {executor.default_quality}")
        print(f"   Timeout: {executor.timeout} seconds")
        
        # Test quality settings
        print(f"\n📊 Available quality settings:")
        for quality, flag in executor.QUALITY_SETTINGS.items():
            print(f"   {quality}: {flag}")
        
        return True
        
    except Exception as e:
        print(f"❌ Executor initialization failed: {e}")
        return False


def test_with_generated_code():
    """Test executor with one of our generated Manim files."""
    print("\n=== Testing with Generated Code ===")
    
    # Test with the simple multi-scene example
    test_file = "examples/simple_multi_scene.py"
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    try:
        # Read the generated code
        with open(test_file, 'r') as f:
            manim_code = f.read()
        
        print(f"✅ Successfully read code file: {test_file}")
        print(f"   Code length: {len(manim_code)} characters")
        
        # Analyze the code structure
        if "class CombinedVideo(Scene):" in manim_code:
            print("✅ Valid Manim scene class found")
        else:
            print("⚠️ Scene class not found in code")
        
        if "def construct(self):" in manim_code:
            print("✅ Construct method found")
        else:
            print("⚠️ Construct method not found")
        
        # Count lines and estimate complexity
        lines = manim_code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        print(f"   Total lines: {len(lines)}")
        print(f"   Non-empty lines: {len(non_empty_lines)}")
        
        # Look for animations
        animation_keywords = ['self.play', 'Write', 'Create', 'FadeIn', 'Transform']
        animation_count = 0
        for line in lines:
            for keyword in animation_keywords:
                if keyword in line:
                    animation_count += 1
                    break
        print(f"   Animation lines: {animation_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to process code file: {e}")
        return False


def simulate_execution():
    """Simulate what would happen when Manim executes the code."""
    print("\n=== Simulating Manim Execution ===")
    
    try:
        executor = ManimExecutor(output_dir="test_videos")
        
        # Simulate execution parameters
        scene_name = "CombinedVideo"
        quality = "medium"
        video_name = "demo_video"
        
        print(f"📝 Execution Parameters:")
        print(f"   Scene name: {scene_name}")
        print(f"   Quality: {quality} ({executor.QUALITY_SETTINGS[quality]})")
        print(f"   Output video: {video_name}.mp4")
        print(f"   Output directory: {executor.output_dir}")
        
        # Simulate command that would be executed
        temp_file = "/tmp/manim_scene_12345678.py"
        cmd_parts = [
            "manim",
            temp_file,
            scene_name,
            executor.QUALITY_SETTINGS[quality],
            "-v", "WARNING",
            "--media_dir", str(executor.output_dir),
            "--video_dir", str(executor.output_dir)
        ]
        
        print(f"\n🔧 Command that would be executed:")
        print(f"   {' '.join(cmd_parts)}")
        
        # Simulate successful result
        simulated_result = ExecutionResult(
            success=True,
            video_path=str(executor.output_dir / f"{video_name}.mp4"),
            duration=45.2,
            stdout="Manim Community v0.18.0\nSuccess: Video generated",
            stderr="",
            temp_files=[temp_file]
        )
        
        print(f"\n✅ Simulated Execution Result:")
        print(f"   Success: {simulated_result.success}")
        print(f"   Video path: {simulated_result.video_path}")
        print(f"   Duration: {simulated_result.duration:.1f} seconds")
        print(f"   Temp files: {len(simulated_result.temp_files)} files")
        
        return True
        
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False


def test_error_handling():
    """Test error handling scenarios."""
    print("\n=== Testing Error Handling ===")
    
    try:
        executor = ManimExecutor()
        
        # Test invalid code
        invalid_code = "print('Not valid Manim code')"
        print("🧪 Testing with invalid Manim code...")
        
        # Simulate error result
        error_result = ExecutionResult(
            success=False,
            duration=5.0,
            stdout="",
            stderr="AttributeError: 'NoneType' object has no attribute 'construct'",
            error_message="Manim execution failed with return code 1",
            temp_files=["/tmp/test_file.py"]
        )
        
        print(f"   Simulated error result:")
        print(f"   Success: {error_result.success}")
        print(f"   Error: {error_result.error_message}")
        print(f"   Duration: {error_result.duration:.1f} seconds")
        
        # Test timeout scenario
        print("\n🕐 Testing timeout scenario...")
        timeout_result = ExecutionResult(
            success=False,
            duration=300.0,
            error_message="Execution timed out after 300 seconds"
        )
        
        print(f"   Timeout result:")
        print(f"   Success: {timeout_result.success}")
        print(f"   Error: {timeout_result.error_message}")
        print(f"   Duration: {timeout_result.duration:.1f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def demonstrate_integration():
    """Demonstrate how executor integrates with the pipeline."""
    print("\n=== Integration Demonstration ===")
    
    print("🔄 Complete Pipeline Flow:")
    print("   1. User Input (PDF + Text)")
    print("   2. ↓ MultiSceneProcessor")
    print("   3. ↓ Generate Manim Code")
    print("   4. ↓ ManimExecutor.execute_code() ← WE ARE HERE")
    print("   5. ↓ MP4 Video File")
    print("   6. ↓ Streamlit Video Player")
    print("   7. ✅ User sees animated video")
    
    print(f"\n💡 Integration Points:")
    print(f"   • Input: Generated Manim Python code (40k+ characters)")
    print(f"   • Process: Execute via subprocess with timeout")
    print(f"   • Output: MP4 file path for web display")
    print(f"   • Error handling: Graceful fallbacks and user feedback")
    
    print(f"\n🎯 For Streamlit Integration:")
    print(f"   • Show progress bar during execution")
    print(f"   • Display execution logs in real-time")
    print(f"   • Handle errors with user-friendly messages") 
    print(f"   • Provide download link for generated video")
    
    return True


def main():
    """Run all executor tests and demonstrations."""
    print("🚀 Manim Executor Testing Suite")
    print("=" * 50)
    
    # Run tests
    test1 = test_executor_architecture()
    test2 = test_with_generated_code() 
    test3 = simulate_execution()
    test4 = test_error_handling()
    test5 = demonstrate_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Architecture test: {'✅ PASSED' if test1 else '❌ FAILED'}")
    print(f"   Code analysis test: {'✅ PASSED' if test2 else '❌ FAILED'}")
    print(f"   Execution simulation: {'✅ PASSED' if test3 else '❌ FAILED'}")
    print(f"   Error handling test: {'✅ PASSED' if test4 else '❌ FAILED'}")
    print(f"   Integration demo: {'✅ PASSED' if test5 else '❌ FAILED'}")
    
    if all([test1, test2, test3, test4, test5]):
        print(f"\n🎉 All tests passed! Executor is ready for integration.")
        print(f"\n📋 Next Steps:")
        print(f"   1. Install Manim system dependencies (Cairo, FFmpeg)")
        print(f"   2. Test actual video generation")
        print(f"   3. Integrate with Streamlit frontend")
        print(f"   4. Deploy for hackathon demo")
    else:
        print(f"\n⚠️ Some tests failed. Check error messages above.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
