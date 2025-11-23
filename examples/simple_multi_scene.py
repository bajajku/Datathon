from manim import *
import numpy as np

class CombinedVideo(Scene):
    """
    Basic Math
    Multi-scene video with 1 parts
    
    Total Duration: 22.0 seconds
    Number of Scenes: 1
    """
    
    def construct(self):
        """Main video construction with multiple scenes."""
        # Title card
        title = Text("Basic Math", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Play all scenes in sequence
        self.scene_1()
        
        # End card
        end_text = Text("End", font_size=36)
        self.play(FadeIn(end_text))
        self.wait(1)

    def scene_1(self):
        """Scene 1: Basic Math - Part 1"""
        # Clear previous scene
        self.clear()
        
        # Scene content
        self.camera.background_color = BLACK

        # Create objects
        chapter1_title = Text("Chapter 1: Addition")
        chapter1_title.move_to([0, 1.5, 0])
        chapter1_title.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        addition_desc = Text("Addition is combining numbers.")
        addition_desc.move_to([0, 0.5, 0])
        addition_desc.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        chapter2_title = Text("Chapter 2: Subtraction")
        chapter2_title.move_to([0, 1.5, 0])
        chapter2_title.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        subtraction_desc = Text("Subtraction is taking away.")
        subtraction_desc.move_to([0, 0.5, 0])
        subtraction_desc.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        chapter3_title = Text("Chapter 3: Multiplication")
        chapter3_title.move_to([0, 1.5, 0])
        chapter3_title.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        multiplication_desc = Text("Multiplication is repeated addition.")
        multiplication_desc.move_to([0, 0.5, 0])
        multiplication_desc.set_color(WHITE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        addition_formula = MathTex(r"2 + 3 = 5")
        addition_formula.move_to([0, -0.5, 0])
        addition_formula.set_color(BLUE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        subtraction_formula = MathTex(r"5 - 3 = 2")
        subtraction_formula.move_to([0, -0.5, 0])
        subtraction_formula.set_color(BLUE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        multiplication_formula = MathTex(r"3 \\times 4 = 12")
        multiplication_formula.move_to([0, -0.5, 0])
        multiplication_formula.set_color(BLUE)
        # For size 1.0, default font size is typically used, no explicit scale or set_font_size needed.

        # Animation Timeline
        current_time = 0.0

        # anim_chapter1_title_write
        animation_start_time = 0.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(chapter1_title), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_addition_desc_write
        animation_start_time = 2.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(addition_desc), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_addition_formula_create
        animation_start_time = 4.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Create(addition_formula), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_chapter1_fade_out
        animation_start_time = 6.5
        animation_duration = 1.0
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(FadeOut(chapter1_title, addition_desc, addition_formula), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_chapter2_title_write
        animation_start_time = 8.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(chapter2_title), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_subtraction_desc_write
        animation_start_time = 10.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(subtraction_desc), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_subtraction_formula_create
        animation_start_time = 12.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Create(subtraction_formula), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_chapter2_fade_out
        animation_start_time = 14.5
        animation_duration = 1.0
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(FadeOut(chapter2_title, subtraction_desc, subtraction_formula), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_chapter3_title_write
        animation_start_time = 16.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(chapter3_title), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_multiplication_desc_write
        animation_start_time = 18.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Write(multiplication_desc), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        # anim_multiplication_formula_create
        animation_start_time = 20.0
        animation_duration = 1.5
        if animation_start_time > current_time:
            self.wait(animation_start_time - current_time)
        self.play(Create(multiplication_formula), run_time=animation_duration)
        current_time = animation_start_time + animation_duration

        total_scene_duration = 22.0
        if total_scene_duration > current_time:
            self.wait(total_scene_duration - current_time)
        
        # Scene transition
        self.wait(0.5)