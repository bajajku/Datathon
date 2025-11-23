"""
Gradio Frontend for Manim Video Generation Pipeline

A simple web interface that allows users to:
1. Upload PDF files or input text directly
2. Generate multi-scene Manim videos
3. Watch generated videos directly in the browser
4. Download generated code and view video statistics
"""

import os
import sys
import tempfile
import traceback
import subprocess
import glob
from pathlib import Path
from io import BytesIO
from typing import Optional, Tuple

import gradio as gr

# Add parent directory to path to import modules
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

from data_processing.multi_scene_processor import process_large_document, MultiSceneStructure


class ManimPipelineFrontend:
    """Gradio frontend for the Manim video generation pipeline."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
    
    def process_input(
        self,
        pdf_file: Optional[gr.File],
        text_input: str,
        document_title: str,
        additional_instructions: str,
        api_key: str,
        auto_generate_video: bool = True,
        quality: str = "480p15"
    ) -> Tuple[str, str, str, Optional[str]]:
        """
        Process the user input and generate Manim code, optionally with video generation.
        
        Returns:
            Tuple of (status_message, video_stats, generated_code, video_file_path)
        """
        try:
            # Use provided API key or fallback to environment variable
            used_api_key = api_key.strip() if api_key.strip() else self.api_key
            
            if not used_api_key:
                return (
                    "❌ Error: No API key provided. Please set GOOGLE_API_KEY environment variable or provide one in the interface.",
                    "",
                    "",
                    None
                )
            
            # Validate input
            if not pdf_file and not text_input.strip():
                return (
                    "❌ Error: Please provide either a PDF file or text input.",
                    "",
                    "",
                    None
                )
            
            # Set default title if not provided
            if not document_title.strip():
                document_title = "Generated Video" if text_input else "PDF Video"
            
            # Combine text input and additional instructions
            combined_text = text_input.strip()
            if additional_instructions.strip():
                combined_text += f"\n\n--- Additional Instructions ---\n{additional_instructions.strip()}"
            
            # Process the document
            print(f"🚀 Starting video generation...")
            print(f"📄 Title: {document_title}")
            print(f"📝 Text input: {len(combined_text)} characters")
            print(f"📁 PDF file: {'Yes' if pdf_file else 'No'}")
            
            # Handle PDF file
            pdf_bytes = None
            if pdf_file:
                with open(pdf_file.name, 'rb') as f:
                    pdf_bytes = BytesIO(f.read())
                print(f"📄 PDF loaded: {len(pdf_bytes.getvalue())} bytes")
            
            # Process the document
            multi_scene, generated_code = process_large_document(
                pdf_path=pdf_file.name if pdf_file else None,
                pdf_bytes=pdf_bytes,
                text_input=combined_text,
                document_title=document_title,
                api_key=used_api_key
            )
            
            # Generate success message with statistics
            status_msg = f"✅ Video generation completed successfully!\n\n"
            status_msg += f"🎬 Title: {multi_scene.title}\n"
            status_msg += f"📺 Total Scenes: {len(multi_scene.scenes)}\n"
            status_msg += f"⏱️ Total Duration: {multi_scene.total_duration:.1f} seconds ({multi_scene.total_duration/60:.1f} minutes)\n"
            status_msg += f"📝 Generated Code: {len(generated_code):,} characters\n\n"
            status_msg += f"🎯 Next Steps:\n"
            status_msg += f"1. Download the generated code below\n"
            status_msg += f"2. Run: manim your_file.py CombinedVideo -pql\n"
            status_msg += f"3. Your video will be generated!"
            
            # Generate detailed statistics
            stats = f"📊 Detailed Video Statistics:\n"
            stats += f"{'='*50}\n\n"
            
            # Scene breakdown
            stats += f"🎥 Scene Breakdown:\n"
            for i, scene in enumerate(multi_scene.scenes, 1):
                stats += f"  Scene {i:2d}: {scene.settings.title}\n"
                stats += f"    ⏱️ Duration: {scene.settings.duration:4.1f}s\n"
                stats += f"    🎯 Objects: {len(scene.objects):2d}\n"
                stats += f"    🎬 Animations: {len(scene.animations):2d}\n"
                stats += f"\n"
            
            # Calculate additional statistics
            avg_duration = multi_scene.total_duration / len(multi_scene.scenes)
            total_objects = sum(len(scene.objects) for scene in multi_scene.scenes)
            total_animations = sum(len(scene.animations) for scene in multi_scene.scenes)
            
            stats += f"📈 Analysis:\n"
            stats += f"  📊 Average scene duration: {avg_duration:.1f} seconds\n"
            stats += f"  🎯 Total objects created: {total_objects}\n"
            stats += f"  🎬 Total animations: {total_animations}\n"
            stats += f"  📱 Scenes per minute: {len(multi_scene.scenes) / (multi_scene.total_duration / 60):.1f}\n"
            stats += f"  ⚡ Objects per scene (avg): {total_objects / len(multi_scene.scenes):.1f}\n"
            
            # Generate video if requested
            video_file_path = None
            
            if auto_generate_video:
                try:
                    # Save the generated code to a temporary file
                    safe_title = "".join(c for c in document_title if c.isalnum() or c in (' ', '-', '_')).strip()
                    safe_title = safe_title.replace(' ', '_').lower()
                    temp_filename = f"{safe_title}_generated.py"
                    temp_filepath = project_root / temp_filename
                    
                    with open(temp_filepath, 'w') as f:
                        f.write(generated_code)
                    
                    print(f"🎬 Generating video with quality {quality}...")
                    
                    # Determine quality flag
                    quality_flag = "-pql"  # Default to low quality
                    if quality == "720p30":
                        quality_flag = "-pqm"  # medium quality
                    elif quality == "1080p60":
                        quality_flag = "-pqh"  # high quality
                    
                    # Run manim command
                    cmd = [
                        "manim", 
                        str(temp_filepath), 
                        "CombinedVideo", 
                        quality_flag,
                        "--disable_caching"
                    ]
                    
                    print(f"Running command: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root))
                    
                    if result.returncode == 0:
                        # Find the generated video file
                        video_dir = project_root / f"media/videos/{temp_filename[:-3]}/{quality}"
                        video_path = video_dir / "CombinedVideo.mp4"
                        
                        if video_path.exists():
                            video_file_path = str(video_path)
                            print(f"✅ Video generated successfully: {video_file_path}")
                            
                            # Update status message
                            status_msg = status_msg.replace("📝 Generated Code:", "🎥 Video Generated!")
                            status_msg += f"\n🎬 Video saved to: {video_path.name}"
                        else:
                            # Try to find any CombinedVideo.mp4 in the media folder
                            video_files = list(project_root.glob("media/videos/**/CombinedVideo.mp4"))
                            if video_files:
                                video_file_path = str(video_files[-1])  # Use the most recent one
                                print(f"✅ Found generated video: {video_file_path}")
                                status_msg += f"\n🎬 Video found: {Path(video_file_path).name}"
                    else:
                        print(f"⚠️ Video generation failed: {result.stderr}")
                        status_msg += f"\n⚠️ Video generation failed. Code generated successfully."
                        
                    # Clean up temp file
                    if temp_filepath.exists():
                        temp_filepath.unlink()
                        
                except Exception as video_error:
                    print(f"⚠️ Video generation error: {video_error}")
                    status_msg += f"\n⚠️ Video generation error: {str(video_error)}"
            
            return status_msg, stats, generated_code, video_file_path
            
        except Exception as e:
            error_msg = f"❌ Error during processing: {str(e)}\n\n"
            error_msg += f"Full traceback:\n{traceback.format_exc()}"
            return error_msg, "", "", None
    
    def create_interface(self):
        """Create the Gradio interface."""
        
        # Custom CSS for better styling
        custom_css = """
        .status-box {
            background-color: #f0f8ff;
            border: 1px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        .stats-box {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
        }
        """
        
        with gr.Blocks(
            theme=gr.themes.Soft(),
            css=custom_css,
            title="Manim Video Generator"
        ) as interface:
            
            gr.HTML("""
            <h1 style="text-align: center; color: #4CAF50;">
                🎬 Manim Video Generation Pipeline
            </h1>
            <p style="text-align: center; font-size: 18px; color: #666;">
                Transform documents and text into engaging educational videos
            </p>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML("<h3>📥 Input</h3>")
                    
                    # File upload
                    pdf_file = gr.File(
                        label="📄 Upload PDF Document (Optional)",
                        file_types=[".pdf"],
                        file_count="single"
                    )
                    
                    # Text input
                    text_input = gr.Textbox(
                        label="📝 Text Input (Optional - use instead of or in addition to PDF)",
                        placeholder="Enter your content here...\n\nExample:\n- Course material\n- Educational content\n- Any text you want to animate",
                        lines=8,
                        max_lines=20
                    )
                    
                    # Document title
                    document_title = gr.Textbox(
                        label="🎬 Video Title",
                        placeholder="e.g., 'Machine Learning Course', 'Physics Fundamentals'",
                        value=""
                    )
                    
                    # Additional instructions
                    additional_instructions = gr.Textbox(
                        label="📋 Additional Instructions (Optional)",
                        placeholder="e.g., 'Use colorful animations', 'Focus on mathematical formulas', 'Make it beginner-friendly'",
                        lines=4
                    )
                    
                    # API key input
                    api_key_input = gr.Textbox(
                        label="🔑 Google Gemini API Key (Optional - will use environment variable if not provided)",
                        placeholder="Enter your API key here...",
                        type="password"
                    )
                    
                    # Video generation options
                    with gr.Accordion("🎬 Video Generation Options", open=True):
                        auto_generate = gr.Checkbox(
                            label="🎥 Auto-generate video after processing",
                            value=True
                        )
                        quality_choice = gr.Dropdown(
                            label="📺 Video Quality",
                            choices=["480p15", "720p30", "1080p60"],
                            value="480p15",
                            info="Higher quality takes longer to generate"
                        )
                    
                    # Generate button
                    generate_btn = gr.Button(
                        "🚀 Generate Video",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.HTML("<h3>📤 Output</h3>")
                    
                    # Status output
                    status_output = gr.Textbox(
                        label="📊 Status",
                        lines=10,
                        max_lines=20,
                        interactive=False,
                        elem_classes=["status-box"]
                    )
                    
                    # Detailed statistics
                    stats_output = gr.Textbox(
                        label="📈 Video Statistics",
                        lines=15,
                        max_lines=30,
                        interactive=False,
                        elem_classes=["stats-box"]
                    )
            
            # Video display (full width)
            with gr.Row():
                video_output = gr.Video(
                    label="🎬 Generated Video Preview",
                    height=400,
                    show_label=True
                )
            
            # Generated code output (full width)
            with gr.Row():
                generated_code_output = gr.Code(
                    label="📄 Generated Manim Code (Download this file and run with Manim)",
                    language="python",
                    lines=15,
                    max_lines=30,
                    interactive=False
                )
            
            # Instructions
            with gr.Accordion("📖 Instructions", open=False):
                gr.HTML("""
                <div style="padding: 20px;">
                <h4>How to use this interface:</h4>
                <ol>
                    <li><strong>Input Options:</strong>
                        <ul>
                            <li>Upload a PDF document, OR</li>
                            <li>Enter text directly, OR</li>
                            <li>Use both for combined processing</li>
                        </ul>
                    </li>
                    <li><strong>Set Parameters:</strong>
                        <ul>
                            <li>Provide a descriptive video title</li>
                            <li>Add any additional instructions for styling/content</li>
                            <li>Provide your Gemini API key (or set GOOGLE_API_KEY environment variable)</li>
                        </ul>
                    </li>
                    <li><strong>Generate:</strong>
                        <ul>
                            <li>Click "Generate Video Code" and wait for processing</li>
                            <li>The system will analyze your content and create multiple coordinated scenes</li>
                        </ul>
                    </li>
                    <li><strong>Use the Output:</strong>
                        <ul>
                            <li>Copy the generated code to a .py file</li>
                            <li>Run: <code>manim your_file.py CombinedVideo -pql</code></li>
                            <li>Your video will be generated in the media/videos folder</li>
                        </ul>
                    </li>
                </ol>
                
                <h4>Features:</h4>
                <ul>
                    <li>✅ Automatic document chunking and scene creation</li>
                    <li>✅ Multi-scene video generation with smooth transitions</li>
                    <li>✅ Support for both PDF and text input</li>
                    <li>✅ Intelligent content analysis and visualization</li>
                    <li>✅ Complete Manim code generation</li>
                </ul>
                
                <h4>Requirements:</h4>
                <ul>
                    <li>Google Gemini API key (get one at <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a>)</li>
                    <li>Manim installed locally to render the videos</li>
                </ul>
                </div>
                """)
            
            # Set up the event handler
            generate_btn.click(
                fn=self.process_input,
                inputs=[
                    pdf_file, text_input, document_title, 
                    additional_instructions, api_key_input,
                    auto_generate, quality_choice
                ],
                outputs=[status_output, stats_output, generated_code_output, video_output]
            )
        
        return interface


def main():
    """Launch the Gradio interface."""
    frontend = ManimPipelineFrontend()
    interface = frontend.create_interface()
    
    print("🚀 Starting Manim Video Generator Frontend...")
    print("🌐 Open your browser to the URL shown below")
    
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7862,       # Use different port to avoid conflicts
        share=False,            # Set to True to create a public link
        debug=False
    )


if __name__ == "__main__":
    main()
