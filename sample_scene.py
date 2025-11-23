from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create objects
        description = Text("Einstein's Mass-Energy Equivalence")
        description.move_to([0, -1, 0])
        description.set_color(WHITE)
        description.set_opacity(1.0)
        
        formula = MathTex(r"E = mc^2")
        formula.move_to([0, 1, 0])
        formula.set_color(YELLOW)
        formula.set_font_size(1.5 * DEFAULT_FONT_SIZE) # Apply size factor
        formula.set_opacity(1.0)
        
        # Animate with proper timing
        # Animation: write_formula
        self.wait(0.5) # Delay before write_formula
        self.play(Write(formula), run_time=2.0)
        
        # Animation: show_description
        # The previous animation ends at 0.5 + 2.0 = 2.5s
        # This animation starts at 3.0s, so wait for 3.0 - 2.5 = 0.5s
        self.wait(0.5) 
        self.play(FadeIn(description), run_time=1.0)
        
        # Final wait to match total scene duration
        # Last animation ends at 3.0 + 1.0 = 4.0s
        # Total scene duration is 6.0s, so wait for 6.0 - 4.0 = 2.0s
        self.wait(2.0)