# Import Main
from manim import *


def laser_vermelho():
    return Dot().set_stroke(color=RED).set_fill(color=RED)


class TornoCNC(Scene):
    def construct(self) -> None:
        superfície = Square(side_length=3)
        corte = Circle()

        self.configurar_cena(superfície, corte)
        self.play_animação(superfície, corte)

    def configurar_cena(self, superfície, buraco):
        self.add(superfície)
        self.add(laser_vermelho().align_to(buraco, RIGHT))

    def play_animação(self, superfície, buraco):
        self.wait(2)
        self.play(
            DrawBorderThenFill(buraco, stroke_color="RED", run_time=5),
            Rotate(superfície, angle=((-2) * (2 * PI)), run_time=5),
        )
        self.play(buraco.animate.set_fill(RED, opacity=0.4))
        self.wait(2)


if __name__ == "__main__":
    scene = TornoCNC()
    scene.render()
