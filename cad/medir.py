"""Medidas sobre el modelo: se mide la geometría, no se repiten los parámetros (P3)."""
from build123d import Axis, Box, Location, Vector

_AXES = {"x": (Axis.X, 0), "y": (Axis.Y, 1), "z": (Axis.Z, 2)}


def _c(v, i):
    return (v.X, v.Y, v.Z)[i]


def _probe(part, center, axis, span, thickness):
    size = [thickness] * 3
    size[_AXES[axis][1]] = span
    probe = Location(Vector(*center)) * Box(*size)
    return part & probe


def gap_width(part, center, axis, span=40.0, thickness=0.1):
    """Ancho del hueco que contiene `center`, a lo largo de `axis`."""
    i = _AXES[axis][1]
    solids = _probe(part, center, axis, span, thickness).solids()
    c = center[i]
    below = [_c(s.bounding_box().max, i) for s in solids if _c(s.bounding_box().max, i) <= c + 1e-6]
    above = [_c(s.bounding_box().min, i) for s in solids if _c(s.bounding_box().min, i) >= c - 1e-6]
    if not below or not above:
        raise ValueError(f"no hay material a ambos lados de {center} en {axis}")
    return min(above) - max(below)


def solid_width(part, center, axis, span=40.0, thickness=0.1):
    """Ancho del material que contiene `center`, a lo largo de `axis`."""
    i = _AXES[axis][1]
    for s in _probe(part, center, axis, span, thickness).solids():
        bb = s.bounding_box()
        if _c(bb.min, i) - 1e-6 <= center[i] <= _c(bb.max, i) + 1e-6:
            return _c(bb.max, i) - _c(bb.min, i)
    raise ValueError(f"no hay material en {center}")


def fits_bed(part, bed):
    """True si la caja envolvente cabe en la cama en alguna de sus orientaciones planas."""
    bb = part.bounding_box()
    dims = sorted((bb.size.X, bb.size.Y, bb.size.Z))
    return all(d <= b for d, b in zip(dims, sorted(bed)))
