"""BE-PROBETA: pieza de prueba de holguras (B7).

Cinco columnas, una por holgura de PROBE_CLEARANCES (0.0 a 0.4 mm, de izquierda a
derecha). Filas, de atrás adelante:
  - agujeros para pasador de acero Ø3
  - alojamientos de tuerca 1/4-20
  - llaves para la boca de la ranura 2020
  - muescas en el canto para el borde de 4.5 mm de la caja
"""
from build123d import (Align, BuildPart, BuildSketch, Box, Cylinder, Locations, Mode, Plane,
                       RegularPolygon, Text, extrude)

from cad import params as P

PLATE = (90.0, 84.0, 8.0)
COLS = tuple(-32.0 + 16.0 * i for i in range(len(P.PROBE_CLEARANCES)))
ROW_PIN, ROW_NUT, ROW_KEY = 22.0, 2.0, -16.0
NOTCH_DEPTH = 10.0
KEY_H, KEY_LEN = 1.5, 10.0
LABEL_Y, LABEL_DEPTH = 36.0, 0.6


def layout():
    """Posiciones de cada elemento, para las pruebas y para leer la probeta impresa."""
    w, d, h = PLATE
    out = []
    for x, c in zip(COLS, P.PROBE_CLEARANCES):
        out.append({
            "clearance": c,
            "pin": (x, ROW_PIN, h / 2),
            "nut": (x, ROW_NUT, h - P.NUT_14_20_H / 2),
            "key": (x, ROW_KEY, h + KEY_H / 2),
            "notch": (x, -d / 2 + NOTCH_DEPTH / 2, h / 2),
        })
    return out


def build():
    w, d, h = PLATE
    with BuildPart() as part:
        Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
        for x, c in zip(COLS, P.PROBE_CLEARANCES):
            with Locations((x, ROW_PIN, 0)):
                Cylinder((P.PIN_D + P.HOLE_COMP + c) / 2, h, align=(Align.CENTER, Align.CENTER, Align.MIN),
                         mode=Mode.SUBTRACT)
            with BuildSketch(Plane.XY.offset(h)):
                with Locations((x, ROW_NUT)):
                    RegularPolygon((P.NUT_14_20_FLATS + c) / 2, 6, major_radius=False, rotation=30)
            extrude(amount=-P.NUT_14_20_H, mode=Mode.SUBTRACT)
            with Locations((x, ROW_NUT, 0)):
                Cylinder((P.BOLT_14_20_D + P.HOLE_COMP) / 2, h, align=(Align.CENTER, Align.CENTER, Align.MIN),
                         mode=Mode.SUBTRACT)
            with Locations((x, ROW_KEY, h)):
                Box(P.SLOT_OPENING - c, KEY_LEN, KEY_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((x, -d / 2, 0)):
                Box(P.BOX_RIM + c, NOTCH_DEPTH, h, align=(Align.CENTER, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY.offset(h)):
            for x, c in zip(COLS, P.PROBE_CLEARANCES):
                with Locations((x, LABEL_Y)):
                    Text(f"{c:.1f}", font_size=4.5)
        extrude(amount=-LABEL_DEPTH, mode=Mode.SUBTRACT)
    part.part.label = "BE-PROBETA-v01"
    return part.part
