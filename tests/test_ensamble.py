"""Fase 4 del spec 001: el ensamble, medido sobre el modelo (P3)."""
import math
from itertools import combinations

import pytest

from cad import ensamble
from cad import params as P

SEP, ANG = P.PRESENTATION_CONFIG


@pytest.fixture(scope="module")
def items():
    return ensamble.build(SEP, ANG)


def _bbox_overlap(a, b):
    A, B = a.bounding_box(), b.bounding_box()
    return (A.min.X < B.max.X and B.min.X < A.max.X and A.min.Y < B.max.Y and B.min.Y < A.max.Y
            and A.min.Z < B.max.Z and B.min.Z < A.max.Z)


def test_sin_interferencias(items):
    """0 mm³ entre cualquier par de piezas, incluidas las paredes de la caja (Marker0 se apoya en el suelo)."""
    bad = []
    for a, b in combinations(items, 2):
        if {a.role, b.role} <= {"caja", "marker"} or not _bbox_overlap(a.part, b.part):
            continue
        vol = sum(s.volume for s in (a.part & b.part).solids())
        if vol > 1e-3:
            bad.append((a.name, b.name, round(vol, 3)))
    assert bad == []


def test_ejes_simetricos_y_hacia_dentro():
    (p1, u1), (p2, u2) = ensamble.camera_axes(SEP, ANG)
    assert p1.Y == pytest.approx(0, abs=1e-6) and p2.Y == pytest.approx(0, abs=1e-6)
    assert p1.X == pytest.approx(-p2.X, abs=1e-6)
    tilt = math.degrees(math.acos(-u1.Z))
    assert tilt == pytest.approx(ANG, abs=0.01)
    assert u1.X > 0 > u2.X


def test_cruce_de_ejes():
    (p1, _), (p2, _) = ensamble.camera_axes(SEP, ANG)
    lens_sep = p2.X - p1.X
    point, dist = ensamble.axes_crossing(SEP, ANG)
    # A lo largo del eje: (S/2)/sin(a); en vertical, desde el plano de los lentes: (S/2)/tan(a).
    assert dist == pytest.approx((lens_sep / 2) / math.sin(math.radians(ANG)), abs=1.0)
    assert p1.Z - point.Z == pytest.approx((lens_sep / 2) / math.tan(math.radians(ANG)), abs=1.0)
    assert point.X == pytest.approx(0, abs=0.01)
