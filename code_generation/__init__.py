"""
Code Generation Package

Converts structured scene descriptions into executable code.
"""

from .manim_code_generator import ManimCodeGenerator, generate_manim_code

__all__ = ['ManimCodeGenerator', 'generate_manim_code']
