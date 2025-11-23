"""
Manim Executor Module

Executes generated Manim Python code to produce MP4 video files.
Handles subprocess execution, error management, and file operations.
"""

import os
import sys
import subprocess
import tempfile
import uuid
import time
from pathlib import Path
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class ExecutionResult:
    """Result of Manim code execution."""
    success: bool
    video_path: Optional[str] = None
    duration: float = 0.0
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    temp_files: List[str] = None


class ManimExecutor:
    """Executes Manim code and generates MP4 videos."""
    
    # Quality settings for Manim
    QUALITY_SETTINGS = {
        'low': '-ql',      # Low quality (854x480, 15FPS)
        'medium': '-qm',   # Medium quality (1280x720, 30FPS)  
        'high': '-qh',     # High quality (1920x1080, 60FPS)
        'production': '-qp', # Production quality (2560x1440, 60FPS)
        'ultra': '-qk'     # Ultra quality (3840x2160, 60FPS)
    }
    
    def __init__(self, 
                 output_dir: str = "videos",
                 temp_dir: Optional[str] = None,
                 default_quality: str = "medium",
                 timeout: int = 300,
                 simulation_mode: bool = False):
        """
        Initialize the Manim executor.
        
        Args:
            output_dir: Directory to store generated videos
            temp_dir: Directory for temporary files (None = system temp)
            default_quality: Default video quality ('low', 'medium', 'high', 'ultra')
            timeout: Maximum execution time in seconds
            simulation_mode: If True, simulate execution without running Manim
        """
        self.output_dir = Path(output_dir)
        self.temp_dir = temp_dir
        self.default_quality = default_quality
        self.timeout = timeout
        self.simulation_mode = simulation_mode
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verify Manim is installed (unless in simulation mode)
        if not simulation_mode:
            self._verify_manim_installation()
        else:
            print("🎭 Running in simulation mode - Manim installation not required")
    
    def execute_code(self, 
                    manim_code: str, 
                    scene_name: str = "CombinedVideo",
                    quality: Optional[str] = None,
                    video_name: Optional[str] = None) -> ExecutionResult:
        """
        Execute Manim code and generate video.
        
        Args:
            manim_code: The complete Manim Python code
            scene_name: Name of the Scene class to render
            quality: Video quality ('low', 'medium', 'high', 'ultra')
            video_name: Custom name for the output video
            
        Returns:
            ExecutionResult with success status and video path
        """
        quality = quality or self.default_quality
        quality_flag = self.QUALITY_SETTINGS.get(quality, '-qm')
        
        start_time = time.time()
        temp_files = []
        
        try:
            # Create temporary Python file
            temp_file = self._create_temp_file(manim_code)
            temp_files.append(temp_file)
            
            # Generate unique output filename
            if not video_name:
                video_name = f"video_{uuid.uuid4().hex[:8]}"
            
            output_path = self.output_dir / f"{video_name}.mp4"
            
            # Handle simulation mode
            if self.simulation_mode:
                return self._simulate_execution(video_name, temp_files, start_time)
            
            # Build manim command (newer versions use 'manim render')
            cmd = [
                "manim", "render",
                temp_file,
                scene_name,
                quality_flag,
                "-v", "warning",  # Reduce verbosity (lowercase)
                "--media_dir", str(self.output_dir),
                "--output_file", f"{video_name}.mp4"
            ]
            
            print(f"Executing Manim command: {' '.join(cmd)}")
            
            # Execute Manim
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=os.getcwd()
            )
            
            duration = time.time() - start_time
            
            # Check if execution was successful
            if result.returncode == 0:
                # Find the generated video file
                video_path = self._find_generated_video(scene_name, quality, video_name)
                
                if video_path and video_path.exists():
                    # Move to our desired location if needed
                    final_path = self._move_video_to_output(video_path, video_name)
                    
                    return ExecutionResult(
                        success=True,
                        video_path=str(final_path),
                        duration=duration,
                        stdout=result.stdout,
                        stderr=result.stderr,
                        temp_files=temp_files
                    )
                else:
                    # List all mp4 files for debugging
                    all_mp4s = list(self.output_dir.rglob("*.mp4"))
                    debug_info = f"Expected scene: {scene_name}, Expected video: {video_name}.mp4\nFound MP4 files:\n"
                    for mp4 in all_mp4s[:10]:  # Limit to first 10
                        debug_info += f"  - {mp4.relative_to(self.output_dir)}\n"
                    
                    return ExecutionResult(
                        success=False,
                        duration=duration,
                        stdout=result.stdout,
                        stderr=result.stderr,
                        error_message=f"Video file was not generated or not found.\n{debug_info}",
                        temp_files=temp_files
                    )
            else:
                return ExecutionResult(
                    success=False,
                    duration=duration,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    error_message=f"Manim execution failed with return code {result.returncode}",
                    temp_files=temp_files
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                duration=time.time() - start_time,
                error_message=f"Execution timed out after {self.timeout} seconds",
                temp_files=temp_files
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                duration=time.time() - start_time,
                error_message=f"Execution failed: {str(e)}",
                temp_files=temp_files
            )
    
    def execute_code_file(self, 
                         code_file_path: str,
                         scene_name: str = "CombinedVideo",
                         quality: Optional[str] = None,
                         video_name: Optional[str] = None) -> ExecutionResult:
        """
        Execute Manim code from an existing file.
        
        Args:
            code_file_path: Path to the Python file containing Manim code
            scene_name: Name of the Scene class to render
            quality: Video quality
            video_name: Custom name for output video
            
        Returns:
            ExecutionResult with success status and video path
        """
        try:
            with open(code_file_path, 'r') as f:
                manim_code = f.read()
            
            return self.execute_code(manim_code, scene_name, quality, video_name)
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                error_message=f"Failed to read code file: {str(e)}"
            )
    
    def cleanup_temp_files(self, temp_files: List[str]):
        """Clean up temporary files."""
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temp file {temp_file}: {e}")
    
    def _create_temp_file(self, manim_code: str) -> str:
        """Create temporary Python file with Manim code."""
        if self.temp_dir:
            temp_dir = self.temp_dir
        else:
            temp_dir = tempfile.gettempdir()
        
        # Create unique filename
        temp_filename = f"manim_scene_{uuid.uuid4().hex[:8]}.py"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        with open(temp_path, 'w') as f:
            f.write(manim_code)
        
        return temp_path
    
    def _find_generated_video(self, scene_name: str, quality: str, video_name: str = None) -> Optional[Path]:
        """Find the generated video file in Manim's output directory."""
        # Manim typically outputs to media_dir/videos/temp_file_name/quality/scene_name.mp4
        
        # Quality mapping for directory names
        quality_dirs = {
            'low': ['480p15', '854x480_15'],
            'medium': ['720p30', '1280x720_30'],
            'high': ['1080p60', '1920x1080_60'],
            'production': ['1440p60', '2560x1440_60'],
            'ultra': ['4k60', '3840x2160_60', '2160p60']
        }
        
        # Search patterns in order of likelihood
        search_locations = [
            # Direct in media_dir/videos/
            self.output_dir / "videos",
            # In media subdirectory
            self.output_dir / "media" / "videos",
            # Current working directory
            Path.cwd() / "media" / "videos",
        ]
        
        for base_dir in search_locations:
            if not base_dir.exists():
                continue
            
            # Look for files matching various patterns
            patterns = [
                f"**/{scene_name}.mp4",
                f"**/videos/**/{scene_name}.mp4",
            ]
            
            # Also try quality-specific directories
            quality_names = quality_dirs.get(quality, [quality])
            for qual_name in quality_names:
                patterns.extend([
                    f"**/{qual_name}/{scene_name}.mp4",
                    f"**/{qual_name}/**/{scene_name}.mp4",
                ])
            
            for pattern in patterns:
                matches = list(base_dir.glob(pattern))
                if matches:
                    # Return the most recently created file
                    return max(matches, key=lambda p: p.stat().st_mtime)
        
        # Last resort: search the entire media_dir recursively for any matching files
        all_mp4s = list(self.output_dir.rglob("*.mp4"))
        
        # Try to find by video_name first (if specified with --output_file)
        if video_name:
            video_matches = [f for f in all_mp4s if video_name in f.name]
            if video_matches:
                return max(video_matches, key=lambda p: p.stat().st_mtime)
        
        # Then try scene name
        scene_matches = [f for f in all_mp4s if scene_name in f.name]
        if scene_matches:
            return max(scene_matches, key=lambda p: p.stat().st_mtime)
        
        # Finally, return the most recently created MP4 if any exist
        if all_mp4s:
            return max(all_mp4s, key=lambda p: p.stat().st_mtime)
        
        return None
    
    def _simulate_execution(self, video_name: str, temp_files: List[str], start_time: float) -> ExecutionResult:
        """Simulate Manim execution for testing purposes."""
        import time
        
        # Simulate processing time
        time.sleep(2)
        
        # Create a dummy video file for testing
        dummy_video_path = self.output_dir / f"{video_name}.mp4"
        dummy_video_path.write_text("# Simulated MP4 video file")
        
        duration = time.time() - start_time
        
        return ExecutionResult(
            success=True,
            video_path=str(dummy_video_path),
            duration=duration,
            stdout="[SIMULATION] Manim Community v0.18.0\n[SIMULATION] Success: Video generated",
            stderr="",
            temp_files=temp_files
        )
    
    def _move_video_to_output(self, video_path: Path, video_name: str) -> Path:
        """Move generated video to the desired output location."""
        target_path = self.output_dir / f"{video_name}.mp4"
        
        # If it's already in the right place with the right name, return it
        if video_path.name == f"{video_name}.mp4" and video_path.parent == self.output_dir:
            return video_path
        
        # Otherwise, copy it to the target location
        try:
            import shutil
            shutil.copy2(video_path, target_path)
            return target_path
        except Exception as e:
            print(f"Warning: Could not move video to {target_path}: {e}")
            return video_path
    
    def _verify_manim_installation(self):
        """Verify that Manim is installed and accessible."""
        try:
            result = subprocess.run(
                ["manim", "--version"], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                raise RuntimeError("Manim command failed")
                
            print(f"Manim version: {result.stdout.strip()}")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Manim command timed out")
        except FileNotFoundError:
            raise RuntimeError(
                "Manim is not installed or not in PATH. "
                "Install with: pip install manim"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to verify Manim installation: {str(e)}")


def execute_manim_code(manim_code: str, 
                      scene_name: str = "CombinedVideo",
                      output_dir: str = "videos",
                      quality: str = "medium",
                      video_name: Optional[str] = None) -> ExecutionResult:
    """
    Convenience function to execute Manim code.
    
    Args:
        manim_code: The Manim Python code to execute
        scene_name: Name of the Scene class to render
        output_dir: Directory to store the video
        quality: Video quality ('low', 'medium', 'high', 'ultra')
        video_name: Custom name for the video
        
    Returns:
        ExecutionResult with success status and video path
    """
    executor = ManimExecutor(output_dir=output_dir)
    return executor.execute_code(manim_code, scene_name, quality, video_name)


# Example usage and testing
if __name__ == "__main__":
    # Test with a simple Manim scene
    test_code = """
from manim import *

class TestScene(Scene):
    def construct(self):
        # Create a simple text
        text = Text("Hello, Manim!")
        text.set_color(BLUE)
        
        # Animate the text
        self.play(Write(text))
        self.wait(2)
        
        # Transform to formula
        formula = MathTex(r"E = mc^2")
        formula.set_color(RED)
        
        self.play(Transform(text, formula))
        self.wait(2)
"""
    
    print("Testing Manim Executor...")
    
    executor = ManimExecutor(output_dir="test_videos")
    result = executor.execute_code(test_code, "TestScene", quality="low", video_name="test_execution")
    
    if result.success:
        print(f"✅ Success! Video generated at: {result.video_path}")
        print(f"⏱️ Execution time: {result.duration:.2f} seconds")
    else:
        print(f"❌ Failed: {result.error_message}")
        if result.stderr:
            print(f"Error output: {result.stderr}")
    
    # Clean up temp files
    if result.temp_files:
        executor.cleanup_temp_files(result.temp_files)
