"""BE-PINZA-CAJA: apoya el perfil sobre el borde de una pared lateral de la caja (E1).

Marco de la barra (perfil a lo largo de X, centrado en el origen). La pared es el plano
x = 0, de BOX_RIM de grosor, con su borde superior en RIM_TOP. La pinza la muerde con dos
mordazas y un M3 por el lado exterior (+X), y sujeta el perfil en una cuna con un M5 a una
tuerca en T en la ranura -Y. Para la pared opuesta se gira 180° sobre Z.
"""
from build123d import Align, BuildPart, BuildSketch, Box, Cylinder, Locations, Mode, Plane, RegularPolygon, extrude

from cad import params as P
from cad.piezas.carcasa import engrave

RIM_TOP = P.PROFILE_BOTTOM - P.PINZA_FLOOR
GAP = P.BOX_RIM + P.CLEARANCE_SLIDE
CRADLE_IN = P.PROFILE_SIZE + P.CLEARANCE_SLIDE
WIDTH = CRADLE_IN + 2 * P.PINZA_CRADLE_WALL
JAW_X = GAP / 2 + P.PINZA_JAW / 2
CLAMP_Z = RIM_TOP - P.PINZA_JAW_DEPTH * 0.6


def build():
    L = P.PINZA_LEN
    with BuildPart() as part:
        with Locations((0, 0, RIM_TOP)):
            Box(L, WIDTH, P.PINZA_FLOOR, align=(Align.CENTER, Align.CENTER, Align.MIN))
        wall_h = P.PINZA_CRADLE_UP - P.PROFILE_BOTTOM
        with Locations(*[(0, s * (CRADLE_IN / 2 + P.PINZA_CRADLE_WALL / 2), P.PROFILE_BOTTOM) for s in (-1, 1)]):
            Box(L, P.PINZA_CRADLE_WALL, wall_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(*[(s * JAW_X, 0, RIM_TOP) for s in (-1, 1)]):
            Box(P.PINZA_JAW, WIDTH, P.PINZA_JAW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX))
        # M3 de apriete contra la pared, desde fuera (+X), con tuerca alojada en la mordaza.
        with Locations((JAW_X, 0, CLAMP_Z)):
            Cylinder((P.M3_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2, P.PINZA_JAW, rotation=(0, 90, 0),
                     mode=Mode.SUBTRACT)
        with BuildSketch(Plane.YZ.offset(JAW_X + P.PINZA_JAW / 2)):
            with Locations((0, CLAMP_Z)):
                RegularPolygon((P.M3_NUT_FLATS + P.CLEARANCE_PRESS) / 2, 6, major_radius=False)
        extrude(amount=-P.M3_NUT_H, mode=Mode.SUBTRACT)
        # M5 a la ranura -Y del perfil.
        with Locations((0, -(CRADLE_IN / 2 + P.PINZA_CRADLE_WALL / 2), 0)):
            Cylinder((P.M5_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2, P.PINZA_CRADLE_WALL, rotation=(90, 0, 0),
                     mode=Mode.SUBTRACT)
    result = engrave(part.part, "BE-PINZA v01", (JAW_X + P.PINZA_JAW / 2, 0, RIM_TOP - 4), (1, 0, 0), (0, 1, 0), size=3)
    result.label = "BE-PINZA-CAJA-v01"
    return result
