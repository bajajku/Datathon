"""
Execution Package

Handles execution of generated Manim code to produce MP4 videos.
"""

from .manim_executor import ManimExecutor, ExecutionResult, execute_manim_code

__all__ = ['ManimExecutor', 'ExecutionResult', 'execute_manim_code']
