"""BE-CARRO: une la cuña al perfil 2020 en la separación elegida (R2).

Marco de la barra: perfil a lo largo de X, centrado en el origen. El carro apoya su cara
superior en la cara inferior del perfil, centrado con una llave que entra en la boca de la
ranura, y se aprieta con 2 M5 a tuercas en T. La cuña se atornilla debajo con 2 M3.
Un índice en V en la cara +Y marca el centro para leer la separación.
"""
from build123d import (Align, BuildLine, BuildPart, BuildSketch, Box, Cylinder, Locations, Mode, Plane, Polyline,
                       extrude, make_face)

from cad import params as P
from cad.piezas.carcasa import engrave

TOP_Z = P.PROFILE_BOTTOM
BOTTOM_Z = TOP_Z - P.CARRO_T


def build():
    s = P.CARRO_SIZE
    with BuildPart() as part:
        with Locations((0, 0, TOP_Z)):
            Box(s, s, P.CARRO_T, align=(Align.CENTER, Align.CENTER, Align.MAX))
            Box(s, P.SLOT_OPENING - P.CLEARANCE_SLIDE, P.KEY_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # M5 a las tuercas en T, con la cabeza metida por debajo.
        m5 = [(-P.CARRO_M5_X, 0, BOTTOM_Z), (P.CARRO_M5_X, 0, BOTTOM_Z)]
        with Locations(*m5):
            Cylinder((P.M5_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2, P.CARRO_T + P.KEY_H,
                     align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            Cylinder((P.M5_HEAD_D + 2 * P.CLEARANCE_SLIDE + 1.0) / 2, P.M5_HEAD_H,
                     align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        # M3 a la cuña: paso vertical; la cabeza apoya arriba, fuera de la huella del perfil.
        with Locations((0, P.WEDGE_M3_Y, BOTTOM_Z), (0, -P.WEDGE_M3_Y, BOTTOM_Z)):
            Cylinder((P.M3_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2, P.CARRO_T,
                     align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        # Índice en V en la cara +Y, en x = 0.
        with BuildSketch(Plane.XY.offset(BOTTOM_Z)):
            with BuildLine():
                Polyline((-2.5, s / 2), (2.5, s / 2), (0, s / 2 - 2.5), close=True)
            make_face()
        extrude(amount=P.CARRO_T, mode=Mode.SUBTRACT)
    result = engrave(part.part, "BE-CARRO v01", (0, -s / 2, (TOP_Z + BOTTOM_Z) / 2), (0, -1, 0), (1, 0, 0), size=3)
    result.label = "BE-CARRO-v01"
    return result
