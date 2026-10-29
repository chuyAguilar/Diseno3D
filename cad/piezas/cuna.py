"""BE-CUNA-Axx.x: cuña que gira la cámara hacia dentro un ángulo fijo y grabado (D3, D4).

La cara superior (z = 0) se atornilla al carro con 2 M3. La inferior está inclinada
`angle` grados alrededor de Y, más gruesa en -X: montada así, gira la cámara hacia +X
(cámara 1); girada 180° sobre Z sirve para la cámara 2. En la cara inferior van el
tornillo 1/4-20, perpendicular a ella, y los dos pasadores Ø3 de la carcasa.
"""
import math

from build123d import (BuildLine, BuildPart, BuildSketch, Circle, Locations, Mode, Plane, Polyline,
                       RegularPolygon, extrude, make_face)

from cad import params as P
from cad.piezas.carcasa import engrave


def code(angle):
    return f"A{angle:04.1f}"


def thickness_at(angle, x):
    """Grosor de la cuña en la coordenada x."""
    w = P.CASE_OUTER
    return P.WEDGE_T0 + (w / 2 - x) * math.tan(math.radians(angle))


def mount_plane(angle):
    """Plano de la cara inferior en su centro; z_dir sale de la cuña (hacia la carcasa)."""
    a = math.radians(angle)
    return Plane(origin=(0, 0, -thickness_at(angle, 0)),
                 x_dir=(math.cos(a), 0, math.sin(a)),
                 z_dir=(math.sin(a), 0, -math.cos(a)))


def build(angle):
    w = P.CASE_OUTER
    t_thin, t_thick = thickness_at(angle, w / 2), thickness_at(angle, -w / 2)
    mp = mount_plane(angle)
    with BuildPart() as part:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline((-w / 2, 0), (w / 2, 0), (w / 2, -t_thin), (-w / 2, -t_thick), close=True)
            make_face()
        extrude(amount=w / 2, both=True)
        # Tornillo 1/4-20: paso, y alojamiento de la cabeza desde arriba.
        with BuildSketch(mp):
            Circle((P.BOLT_14_20_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2)
        extrude(amount=-40, mode=Mode.SUBTRACT)
        with BuildSketch(mp.offset(-P.WEDGE_SEAT)):
            Circle((P.BOLT_14_20_HEAD_D + 2 * P.CLEARANCE_SLIDE + 1.0) / 2)
        extrude(amount=-40, mode=Mode.SUBTRACT)
        # Pasadores antigiro, alineados con los de la carcasa.
        with BuildSketch(mp):
            with Locations((-P.CASE_PIN_X, 0), (P.CASE_PIN_X, 0)):
                Circle((P.PIN_D + P.HOLE_COMP + P.CLEARANCE_PRESS) / 2)
        extrude(amount=-P.PIN_DEPTH, mode=Mode.SUBTRACT)
        # Tornillos M3 al carro: paso vertical y tuerca por la cara inferior.
        with BuildSketch(Plane.XY):
            with Locations((0, P.WEDGE_M3_Y), (0, -P.WEDGE_M3_Y)):
                Circle((P.M3_D + P.HOLE_COMP + P.CLEARANCE_SLIDE) / 2)
        extrude(amount=-40, mode=Mode.SUBTRACT)
        with BuildSketch(mp):
            with Locations((0, P.WEDGE_M3_Y), (0, -P.WEDGE_M3_Y)):
                RegularPolygon((P.M3_NUT_FLATS + P.CLEARANCE_PRESS) / 2, 6, major_radius=False)
        extrude(amount=-P.M3_NUT_H, mode=Mode.SUBTRACT)
    # Grabado: el ángulo en grande en la cara -Y, el nombre en la +Y.
    result = engrave(part.part, f"{angle:.1f}°", (0, -w / 2, -P.WEDGE_T0 / 2 + 1), (0, -1, 0), (1, 0, 0), size=5)
    result = engrave(result, f"BE-CUNA-{code(angle)} v01", (0, w / 2, -P.WEDGE_T0 / 2 + 1), (0, 1, 0), (-1, 0, 0),
                     size=3)
    result.label = f"BE-CUNA-{code(angle)}-v01"
    return result
