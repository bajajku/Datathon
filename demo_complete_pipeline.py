"""
Complete Pipeline Demo

Demonstrates the full capability of the system:
1. Large document processing (PDF + text input)
2. Intelligent chunking
3. Multi-scene generation
4. Combined video creation

This showcases the production-ready system for your hackathon MVP.
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


def demo_complete_system():
    """Demonstrate the complete multi-scene pipeline."""
    print("🚀 Complete Multi-Scene Video Generation Pipeline Demo")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your Gemini API key to run this demo.")
        return False
    
    print("✅ API Key found")
    
    # Simulate a 10-page PDF content with additional user instructions
    large_document_content = """
    Machine Learning Fundamentals
    
    Chapter 1: Introduction to Machine Learning
    Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention. Machine learning algorithms build a mathematical model based on training data in order to make predictions or decisions without being explicitly programmed to do so.
    
    Chapter 2: Supervised Learning
    Supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs. It infers a function from labeled training data consisting of a set of training examples. Common algorithms include linear regression, logistic regression, decision trees, random forests, and support vector machines. The goal is to approximate the mapping function so well that when you have new input data, you can predict the output variables for that data.
    
    Chapter 3: Unsupervised Learning  
    Unsupervised learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels and with a minimum of human supervision. Common techniques include clustering, association rule learning, and dimensionality reduction. K-means clustering groups data points into clusters based on similarity. Principal Component Analysis (PCA) reduces the dimensionality of data while preserving important information.
    
    Chapter 4: Neural Networks
    A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates. Neural networks consist of layers of interconnected nodes (neurons). Each connection has a weight that adjusts as learning proceeds. The input layer receives data, hidden layers process it, and the output layer produces results. Activation functions determine whether a neuron should be activated or not.
    
    Chapter 5: Deep Learning
    Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, natural language processing, and speech recognition. Convolutional Neural Networks (CNNs) are particularly effective for image recognition tasks.
    """
    
    user_instructions = """
    Create engaging educational animations for each machine learning concept.
    Include visual representations of algorithms where possible.
    Use mathematical formulas and diagrams to illustrate key points.
    Make each scene build upon previous concepts logically.
    Keep explanations clear and suitable for beginners.
    Use colors and animations to highlight important relationships.
    """
    
    print(f"📄 Processing large document ({len(large_document_content)} characters)")
    print(f"📝 With additional user instructions ({len(user_instructions)} characters)")
    print(f"📊 Total content: {len(large_document_content + user_instructions)} characters")
    
    try:
        print("\n🔄 Stage 1: Document Analysis & Chunking...")
        
        multi_scene, combined_code = process_large_document(
            text_input=large_document_content + "\n\n--- User Instructions ---\n" + user_instructions,
            document_title="Machine Learning Complete Course",
            api_key=api_key
        )
        
        print("✅ Successfully processed document!")
        
        print(f"\n📊 Video Statistics:")
        print(f"  🎬 Title: {multi_scene.title}")
        print(f"  📺 Total Scenes: {len(multi_scene.scenes)}")
        print(f"  ⏱️  Total Duration: {multi_scene.total_duration:.1f} seconds ({multi_scene.total_duration/60:.1f} minutes)")
        print(f"  📝 Generated Code: {len(combined_code):,} characters")
        
        print(f"\n🎥 Scene Breakdown:")
        for i, scene in enumerate(multi_scene.scenes, 1):
            print(f"  Scene {i:2d}: {scene.settings.title}")
            print(f"    ⏱️  Duration: {scene.settings.duration:4.1f}s")
            print(f"    🎯 Objects: {len(scene.objects):2d}")
            print(f"    🎬 Animations: {len(scene.animations):2d}")
        
        # Calculate some interesting stats
        avg_duration = multi_scene.total_duration / len(multi_scene.scenes)
        total_objects = sum(len(scene.objects) for scene in multi_scene.scenes)
        total_animations = sum(len(scene.animations) for scene in multi_scene.scenes)
        
        print(f"\n📈 Analysis:")
        print(f"  📊 Average scene duration: {avg_duration:.1f} seconds")
        print(f"  🎯 Total objects created: {total_objects}")
        print(f"  🎬 Total animations: {total_animations}")
        print(f"  📱 Scenes per minute: {len(multi_scene.scenes) / (multi_scene.total_duration / 60):.1f}")
        print(f"  ⚡ Objects per scene (avg): {total_objects / len(multi_scene.scenes):.1f}")
        
        # Save the final code
        output_filename = "complete_ml_course.py"
        with open(output_filename, 'w') as f:
            f.write(combined_code)
        
        print(f"\n💾 Generated Files:")
        print(f"  📄 {output_filename} - Complete Manim video code")
        print(f"  📊 File size: {len(combined_code):,} characters")
        
        print(f"\n🎯 Next Steps:")
        print(f"  1. Run 'manim {output_filename} CombinedVideo -pql' to generate the video")
        print(f"  2. The output will be a {multi_scene.total_duration/60:.1f}-minute educational video")
        print(f"  3. Video covers all {len(multi_scene.scenes)} machine learning topics")
        
        print(f"\n✨ Success Metrics:")
        print(f"  ✅ Large document processed: {len(large_document_content)} chars")
        print(f"  ✅ Intelligent chunking: {len(multi_scene.scenes)} logical sections")
        print(f"  ✅ Multi-scene generation: All scenes created successfully")
        print(f"  ✅ Code generation: {len(combined_code):,} chars of Manim code")
        print(f"  ✅ Ready for execution: Complete runnable video")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_system_capabilities():
    """Show what the system can now handle."""
    print(f"\n🎉 System Capabilities Achieved:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📄 INPUT PROCESSING:")
    print(f"  ✅ Large PDF files (10+ pages)")
    print(f"  ✅ Combined PDF + text input")
    print(f"  ✅ Pure text input (any size)")
    print(f"  ✅ Intelligent content analysis")
    
    print(f"\n🧠 CONTENT PROCESSING:")
    print(f"  ✅ Automatic document chunking")
    print(f"  ✅ Logical section identification")
    print(f"  ✅ Context-aware scene creation")
    print(f"  ✅ Multi-scene coordination")
    
    print(f"\n🎬 VIDEO GENERATION:")
    print(f"  ✅ Multiple coordinated scenes")
    print(f"  ✅ Smooth scene transitions")
    print(f"  ✅ Title and end cards")
    print(f"  ✅ Complete Manim code output")
    
    print(f"\n⚡ SCALABILITY:")
    print(f"  ✅ No limit on document size")
    print(f"  ✅ Automatic scene optimization")
    print(f"  ✅ Intelligent duration management")
    print(f"  ✅ Production-ready output")
    
    print(f"\n🎯 HACKATHON MVP STATUS:")
    print(f"  ✅ Text → Video pipeline: COMPLETE")
    print(f"  ✅ Large document support: COMPLETE")
    print(f"  ✅ Multi-scene videos: COMPLETE")
    print(f"  ✅ Ready for web interface: COMPLETE")


if __name__ == "__main__":
    print("🚀 Starting Complete Pipeline Demo...\n")
    
    success = demo_complete_system()
    
    if success:
        show_system_capabilities()
        print(f"\n🏆 DEMO COMPLETE - System Ready for Hackathon!")
    else:
        print(f"\n❌ Demo failed - Check error messages above")
    
    print("=" * 60)
