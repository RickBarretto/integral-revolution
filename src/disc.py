from typing import Generator
from manim.mobject.geometry.arc import Circle
import numpy
from manim import *
from manim.mobject.three_d.three_dimensions import Surface


def curva_parabolóide() -> ParametricFunction:
    """Curva parabolóide no eixo YZ pertencente à superfície da cena."""

    return ParametricFunction(
        lambda valor_z: (0, valor_z**2, valor_z),
        t_range=np.array([0, 2]),
        color=BLUE,
    )


def superfície_parabolóide() -> Surface:
    """Superfície parabolóide de revolução ao redor do eixo Y."""

    return Surface(
        lambda raio, theta: numpy.array(
            [raio * numpy.cos(theta), raio**2, raio * numpy.sin(theta)]
        ),
        u_range=[0, 2],  # Raio de 0 a 2
        v_range=[0, TAU],  # Ângulo de 0° a 360°
        checkerboard_colors=[BLUE_D, BLUE_E],
    )


def camadas_com_espaçamento_de(espaçamento: float | int) -> VGroup:
    """Retorna todas as camadas com espaçamento requisitado.

    A função da curva é z = y^2.
    """

    def círculo_em_y(raio: float, posição: float) -> Circle:
        """Gera círculo"""
        return (
            Circle(radius=raio)
            .move_to((0, posição, 0))
            .rotate(90 * DEGREES, axis=RIGHT)
            .set_fill(color=BLUE_E, opacity=0.3)
            .set_stroke(color=BLUE_E)
        )

    def círculos():
        """Gera círculos enquanto o raio for menor que o limite superior do raio.

        limite superior = 2
        """
        raio = 0
        posição = 0

        while raio < 2:
            yield círculo_em_y(raio, posição)
            posição += espaçamento
            raio = numpy.sqrt(posição)

    camadas = [círculo for círculo in círculos()]
    return VGroup(*camadas)


class MétodoDeDisco(ThreeDScene):
    """Demonstra a Integração pelo método de disco na prática.

    Parabolóide usada na demonstração:
        x = r * cos(theta)
        y = r^2
        z = r * sen(theta)
    """

    def construct(self):
        self.pré_configurar_cena()

        curva = curva_parabolóide()
        superfície = superfície_parabolóide()

        self.play_animações(curva, superfície)

    def pré_configurar_cena(self) -> None:
        """Pré configura a cena"""
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        eixos = ThreeDAxes()
        nomes_dos_eixos = eixos.get_axis_labels(Text("X"), Text("Y"), Text("Z"))
        self.add(eixos, nomes_dos_eixos)

    def play_animações(self, curva, superfície):
        self.play_início()
        self.play_mostrar_curva(curva)
        self.play_mostrar_superfície(superfície)
        self.play_integrar_paraboloide(superfície)
        self.play_mostrar_lateral()
        self.play_fim()

    def play_início(self) -> None:
        """Inicia a apresentação"""
        self.wait(2)

    def play_mostrar_curva(self, paraboloid_curve: ParametricFunction) -> None:
        """Mostra a curva parabolóide no eixo YZ"""
        self.play(Create(paraboloid_curve))
        self.wait(1)

    def play_mostrar_superfície(self, surface: Surface) -> None:
        """Mostra a superfície parabolóide e muda o ângulo da câmera para uma melhor visão."""
        self.play(Create(surface))
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=3)

    def play_integrar_paraboloide(self, surface: Surface) -> None:
        """Integra a parabolóide com várias camadas de discos."""
        self.play(
            surface.animate.set_fill_by_checkerboard(
                [BLUE_D, BLUE_E], opacity=0.4
            )  # type: ignore
        )
        self.play(Create(camadas_com_espaçamento_de(0.5)), run_time=3)
        self.play(Create(camadas_com_espaçamento_de(0.05)), run_time=1)

    def play_mostrar_lateral(self) -> None:
        """Mostra a lateral do parabolóide."""
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, run_time=3)

    def play_fim(self) -> None:
        """Finaliza a apresentação"""
        self.wait(5)


if __name__ == "__main__":
    scene = MétodoDeDisco()
    scene.render()
