from typing import Generator
from manim import *
from manim.mobject.three_d.three_dimensions import Surface
import numpy


def superfície_conífera() -> Surface:
    """Superfície conífera com revolução ao redor do eixo Z"""
    return Surface(
        lambda theta, raio: numpy.array(
            [
                raio * numpy.cos(theta),
                raio * numpy.sin(theta),
                2 - raio,
            ]
        ),
        u_range=[0, TAU],  # Ângulo de 0° a 360°
        v_range=[0, 2],  # Raio de 0 a 2
        checkerboard_colors=[BLUE_D, BLUE_E],
    )


def cilíndros_com_incremento_de(incremento: float):
    def cilíndro_com_altura(raio: float, altura: float) -> Cylinder:
        """Gera cilíndro"""
        return (
            Cylinder(radius=raio, height=altura)
            .shift(numpy.array([0.0, 0.0, altura / 2]))
        )

    def intervalo_da_altura():
        assert incremento > 0
        iteração = 0
        while iteração < 2:
            yield iteração
            iteração += incremento

    camadas = [
        cilíndro_com_altura(2 - altura, altura)
        for altura in intervalo_da_altura()
    ]

    return VGroup(*camadas)


class MétodoDoCilíndro(ThreeDScene):
    def construct(self) -> None:
        self.pré_configurar_cena()

        cone = superfície_conífera()
        self.play_animação(cone)

    def pré_configurar_cena(self) -> None:
        """Pré configura a cena"""
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        eixos = ThreeDAxes()
        nomes_dos_eixos = eixos.get_axis_labels(Text("X"), Text("Y"), Text("Z"))
        self.add(eixos, nomes_dos_eixos)

    def play_animação(self, cone: Surface):
        self.play_intro()
        self.play_gerar_cone(cone)
        self.play_integrar_cone(cone)
        self.play_outro()

    def play_intro(self):
        title = Text("Método do Cilíndro", font_size=36)
        self.play(Create(title))
        self.wait(2)
        self.remove(title)

    def play_outro(self):
        self.wait(2)

    def play_gerar_cone(self, cone: Surface):
        self.play(Create(cone, run_time=3))

    def play_integrar_cone(self, cone: Surface):
        self.play(cone.animate.set_opacity(0.4))
        self.play(Create(cilíndros_com_incremento_de(0.5), run_time=3))
        self.play(Create(cilíndros_com_incremento_de(0.1), run_time=3))
        self.play(Create(cilíndros_com_incremento_de(0.05), run_time=3))


if __name__ == "__main__":
    scene = MétodoDoCilíndro()
    scene.render()
