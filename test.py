from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Manim Works!", font_size=72)
        self.play(Write(text))
        self.wait(1)