"""
Data Processing Package

Handles input processing, scene structure, and parsing for code generation.
"""

from .input_processor import InputProcessor, process_input
from .scene_structure import SceneStructure, SceneObject, AnimationStep, ObjectType, AnimationType
from .scene_parser import SceneParser, CodeGenerationContext, parse_scene

__all__ = [
    'InputProcessor', 'process_input',
    'SceneStructure', 'SceneObject', 'AnimationStep', 'ObjectType', 'AnimationType', 
    'SceneParser', 'CodeGenerationContext', 'parse_scene'
]
