#!/usr/bin/env python3
"""
Simple launcher for the Manim Video Generator Frontend

Run this script to start the Gradio web interface.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from frontend.gradio_app import main

if __name__ == "__main__":
    main()
