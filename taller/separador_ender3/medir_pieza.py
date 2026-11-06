"""Medidas de un separador sobre el modelo (P3): las usan la prueba y `datos.txt`."""
from cad import medir
from taller.separador_ender3 import params as P


def medidas(part):
    bb = part.bounding_box()
    z = P.CHAMFER + 1.0                       # por encima del bisel y por debajo de las ranuras
    section = medir._probe(part, (0, 0, z), "x", P.OUTER_D + 4, 0.05)
    groove_x = P.OUTER_D / 2 - P.MARK_D / 2   # dentro de la profundidad de la ranura
    segments = medir._probe(part, (groove_x, 0, bb.size.Z / 2), "z", bb.size.Z + 2, 0.05).solids()
    return {
        "largo": bb.size.Z,
        "exterior": section.bounding_box().size.X,
        "agujero": medir.gap_width(part, (0, 0, z), "x"),
        "ranuras": len(segments) - 1,
    }
