from manim import *import numpy as np

class CombinedVideo(Scene):
    """
    Basic Math
    Multi-scene video with 1 parts
    
    Total Duration: 23.0 seconds
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
                # Create objects
                ch1_title = Text("Chapter 1: Addition")
                ch1_title.move_to([0, 2, 0])
                ch1_title.set_color(WHITE)
                ch1_title.scale(1.2)
                ch1_title.set_opacity(1.0)

                ch1_desc = Text("Addition is combining numbers.")
                ch1_desc.move_to([0, 1, 0])
                ch1_desc.set_color(WHITE)
                ch1_desc.scale(1.0)
                ch1_desc.set_opacity(1.0)

                ch2_title = Text("Chapter 2: Subtraction")
                ch2_title.move_to([0, 2, 0])
                ch2_title.set_color(WHITE)
                ch2_title.scale(1.2)
                ch2_title.set_opacity(1.0)

                ch2_desc = Text("Subtraction is taking away.")
                ch2_desc.move_to([0, 1, 0])
                ch2_desc.set_color(WHITE)
                ch2_desc.scale(1.0)
                ch2_desc.set_opacity(1.0)

                ch3_title = Text("Chapter 3: Multiplication")
                ch3_title.move_to([0, 2, 0])
                ch3_title.set_color(WHITE)
                ch3_title.scale(1.2)
                ch3_title.set_opacity(1.0)

                ch3_desc = Text("Multiplication is repeated addition.")
                ch3_desc.move_to([0, 1, 0])
                ch3_desc.set_color(WHITE)
                ch3_desc.scale(1.0)
                ch3_desc.set_opacity(1.0)

                ch1_formula = MathTex(r"2 + 3 = 5")
                ch1_formula.move_to([0, -0.5, 0])
                ch1_formula.set_color(BLUE)
                ch1_formula.scale(1.0)
                ch1_formula.set_opacity(1.0)

                ch2_formula = MathTex(r"5 - 3 = 2")
                ch2_formula.move_to([0, -0.5, 0])
                ch2_formula.set_color(BLUE)
                ch2_formula.scale(1.0)
                ch2_formula.set_opacity(1.0)

                ch3_formula = MathTex(r"3 \times 4 = 12")
                ch3_formula.move_to([0, -0.5, 0])
                ch3_formula.set_color(BLUE)
                ch3_formula.scale(1.0)
                ch3_formula.set_opacity(1.0)

                # Animation Timeline
                current_time = 0.0

                # anim_ch1_title_write (start_time: 0.0, duration: 1.5)
                self.wait(0.0 - current_time)
                self.play(Write(ch1_title), run_time=1.5)
                current_time = 1.5

                # anim_ch1_desc_write (start_time: 2.0, duration: 2.0)
                self.wait(2.0 - current_time)
                self.play(Write(ch1_desc), run_time=2.0)
                current_time = 4.0

                # anim_ch1_formula_create (start_time: 4.5, duration: 1.5)
                self.wait(4.5 - current_time)
                self.play(Create(ch1_formula), run_time=1.5)
                current_time = 6.0

                # anim_ch1_fade_out (start_time: 7.0, duration: 1.0)
                self.wait(7.0 - current_time)
                self.play(FadeOut(ch1_title, ch1_desc, ch1_formula), run_time=1.0)
                current_time = 8.0

                # anim_ch2_title_write (start_time: 8.0, duration: 1.5)
                self.wait(8.0 - current_time)
                self.play(Write(ch2_title), run_time=1.5)
                current_time = 9.5

                # anim_ch2_desc_write (start_time: 9.5, duration: 2.0)
                self.wait(9.5 - current_time)
                self.play(Write(ch2_desc), run_time=2.0)
                current_time = 11.5

                # anim_ch2_formula_create (start_time: 12.0, duration: 1.5)
                self.wait(12.0 - current_time)
                self.play(Create(ch2_formula), run_time=1.5)
                current_time = 13.5

                # anim_ch2_fade_out (start_time: 14.5, duration: 1.0)
                self.wait(14.5 - current_time)
                self.play(FadeOut(ch2_title, ch2_desc, ch2_formula), run_time=1.0)
                current_time = 15.5

                # anim_ch3_title_write (start_time: 15.5, duration: 1.5)
                self.wait(15.5 - current_time)
                self.play(Write(ch3_title), run_time=1.5)
                current_time = 17.0

                # anim_ch3_desc_write (start_time: 17.0, duration: 2.0)
                self.wait(17.0 - current_time)
                self.play(Write(ch3_desc), run_time=2.0)
                current_time = 19.0

                # anim_ch3_formula_create (start_time: 19.5, duration: 1.5)
                self.wait(19.5 - current_time)
                self.play(Create(ch3_formula), run_time=1.5)
                current_time = 21.0

                self.wait(23.0 - current_time)
        
        # Scene transition
        self.wait(0.5)