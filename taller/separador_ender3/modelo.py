"""SEP-ENDER3-L<largo>: tubo con el eje en Z, apoyado en z = 0.

Las piezas se distinguen por ranuras en el costado, a media altura: tantas como su
posición en `params.LENGTHS` + 1 (1 ranura la de 15.0, 2 la de 14.7).
"""
from build123d import Axis, BuildLine, BuildPart, BuildSketch, Cylinder, Location, Plane, Polyline, make_face, revolve

from taller.separador_ender3 import params as P


def groove_z(length, n):
    """Altura del centro de cada una de las n ranuras."""
    return [length / 2 + (k - (n - 1) / 2) * P.MARK_PITCH for k in range(n)]


def build(length, grooves):
    r_in, r_out, c = P.BORE_D / 2, P.OUTER_D / 2, P.CHAMFER
    with BuildPart() as part:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline((r_in, 0), (r_out - c, 0), (r_out, c), (r_out, length), (r_in, length), close=True)
            make_face()
        revolve(axis=Axis.Z)
    result = part.part
    ring = Cylinder(r_out + 1, P.MARK_W) - Cylinder(r_out - P.MARK_D, P.MARK_W)
    for z in groove_z(length, grooves):
        result -= Location((0, 0, z)) * ring
    result.label = f"SEP-ENDER3-L{length:.1f}"
    return result


def variants():
    """Una pieza por largo de `params.LENGTHS`, con 1, 2… ranuras."""
    return [build(length, k + 1) for k, length in enumerate(P.LENGTHS)]
