"""BE-CARCASA y BE-CARCASA-TAPA: carcasa de la cámara con antigiro (D2).

La cámara mira hacia -Z. La cara trasera (z = 0) es la de montaje: tuerca 1/4-20
insertada por dentro y dos pasadores Ø3 que impiden el giro. La placa queda apretada
entre la tapa y cuatro postes, así que no se mueve dentro de la carcasa (P6). La tapa
se atornilla con 4 M3 (transporte) y deja holgura alrededor del portalente (P5).
"""
from build123d import (Align, BuildPart, BuildSketch, Box, Circle, Cylinder, Locations, Mode, Plane,
                       RegularPolygon, Text, extrude)

from cad import params as P

ALIGN_TOP = (Align.CENTER, Align.CENTER, Align.MAX)
FRONT_Z = -P.CASE_DEPTH                   # cara frontal de la placa de la cámara
SCREWS = [(sx * P.CASE_SCREW_XY, sy * P.CASE_SCREW_XY) for sx in (-1, 1) for sy in (-1, 1)]


def _hole_d(nominal, fit):
    return nominal + P.HOLE_COMP + fit


def engrave(part, text, origin, normal, x_dir, size=3.5):
    """Devuelve `part` con `text` grabado 0.6 mm en la cara que pasa por `origin` con normal saliente `normal`.

    Se llama fuera de BuildPart: dentro, el texto en un plano no horizontal no llega a la pieza.
    """
    sketch = Plane(origin=origin, x_dir=x_dir, z_dir=normal) * Text(text, font_size=size)
    return part - extrude(sketch, amount=-0.6)


def build_base():
    o, c = P.CASE_OUTER, P.CASE_CAVITY
    with BuildPart() as part:
        Box(o, o, P.CASE_DEPTH, align=ALIGN_TOP)
        with Locations((0, 0, FRONT_Z)):
            Box(P.CASE_FLANGE, P.CASE_FLANGE, P.CASE_FLANGE_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, -P.CASE_BACK_T)):
            Box(c, c, P.CASE_DEPTH - P.CASE_BACK_T, align=ALIGN_TOP, mode=Mode.SUBTRACT)
        # Postes que apoyan la placa por sus esquinas.
        post_c = c / 2 - P.CASE_POST / 2
        post_h = P.CASE_DEPTH - P.CASE_BACK_T - P.BOARD_T
        with Locations(*[(sx * post_c, sy * post_c, -P.CASE_BACK_T) for sx in (-1, 1) for sy in (-1, 1)]):
            Box(P.CASE_POST, P.CASE_POST, post_h, align=ALIGN_TOP)
        # Montaje trasero: tuerca 1/4-20 por dentro, paso del tornillo y pasadores.
        with BuildSketch(Plane.XY.offset(-P.CASE_BACK_T)):
            RegularPolygon((P.NUT_14_20_FLATS + P.CLEARANCE_PRESS) / 2, 6, major_radius=False)
        extrude(amount=P.NUT_14_20_H, mode=Mode.SUBTRACT)
        Cylinder(_hole_d(P.BOLT_14_20_D, P.CLEARANCE_SLIDE) / 2, P.CASE_BACK_T, align=ALIGN_TOP, mode=Mode.SUBTRACT)
        with Locations((-P.CASE_PIN_X, 0, 0), (P.CASE_PIN_X, 0, 0)):
            Cylinder(_hole_d(P.PIN_D, P.CLEARANCE_PRESS) / 2, P.PIN_DEPTH, align=ALIGN_TOP, mode=Mode.SUBTRACT)
        # Brida: paso M3 y alojamiento de tuerca por detrás.
        with Locations(*[(x, y, FRONT_Z) for x, y in SCREWS]):
            Cylinder(_hole_d(P.M3_D, P.CLEARANCE_SLIDE) / 2, P.CASE_FLANGE_T,
                     align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY.offset(FRONT_Z + P.CASE_FLANGE_T)):
            with Locations(*SCREWS):
                RegularPolygon((P.M3_NUT_FLATS + P.CLEARANCE_PRESS) / 2, 6, major_radius=False)
        extrude(amount=-P.M3_NUT_H, mode=Mode.SUBTRACT)
        # Salida del cable en la pared +Y, junto a la placa trasera.
        w, h = P.CABLE_SLOT
        with Locations((0, o / 2, -P.CASE_BACK_T - h / 2 - 1)):
            Box(w, P.CASE_WALL * 3, h, mode=Mode.SUBTRACT)
    result = engrave(part.part, "BE-CARCASA v01", (0, -o / 2, -P.CASE_DEPTH / 2), (0, -1, 0), (1, 0, 0))
    result.label = "BE-CARCASA-v01"
    return result


def build_lid():
    with BuildPart() as part:
        with Locations((0, 0, FRONT_Z)):
            Box(P.CASE_FLANGE, P.CASE_FLANGE, P.CASE_LID_T, align=ALIGN_TOP)
            Cylinder(P.LENS_CLEAR_D / 2, P.CASE_LID_T, align=ALIGN_TOP, mode=Mode.SUBTRACT)
        with Locations(*[(x, y, FRONT_Z) for x, y in SCREWS]):
            Cylinder(_hole_d(P.M3_D, P.CLEARANCE_SLIDE) / 2, P.CASE_LID_T, align=ALIGN_TOP, mode=Mode.SUBTRACT)
    result = engrave(part.part, "TAPA v01", (0, -P.CASE_FLANGE / 2 + 4.5, FRONT_Z - P.CASE_LID_T),
                     (0, 0, -1), (1, 0, 0), size=3)
    result.label = "BE-CARCASA-TAPA-v01"
    return result
