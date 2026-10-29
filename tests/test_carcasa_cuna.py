"""Fase 2 del spec 001: carcasa con antigiro y cuñas, medidas sobre el modelo (P3)."""
import math

import pytest
from build123d import Align, Cylinder, GeomType, Location

from cad import medir
from cad import params as P
from cad.piezas import carcasa, cuna

TOL = 0.01
MID_Z = -20.0


@pytest.fixture(scope="module")
def base():
    return carcasa.build_base()


@pytest.fixture(scope="module")
def lid():
    return carcasa.build_lid()


@pytest.fixture(scope="module")
def wedges():
    return {a: cuna.build(a) for a in P.ANGLE_SET}


def test_cavidad_de_la_placa(base):
    expected = P.CAM_BOARD + 2 * P.CLEARANCE_SLIDE
    assert medir.gap_width(base, (0, 0, MID_Z), "x", span=60) == pytest.approx(expected, abs=TOL)
    assert medir.gap_width(base, (0, 0, MID_Z), "y", span=60) == pytest.approx(expected, abs=TOL)


def test_paredes(base):
    side = medir.solid_width(base, (P.CASE_OUTER / 2 - 0.5, 0, MID_Z), "x")
    back = medir.solid_width(base, (0, 8, -P.CASE_BACK_T / 2), "z")
    assert side >= P.WALL_MIN - TOL
    assert back >= P.WALL_STRUCT
    assert back == pytest.approx(P.CASE_BACK_T, abs=TOL)


def test_montaje_trasero(base):
    pin = P.PIN_D + P.HOLE_COMP + P.CLEARANCE_PRESS
    for x in (-P.CASE_PIN_X, P.CASE_PIN_X):
        assert medir.gap_width(base, (x, 0, -P.PIN_DEPTH / 2), "x") == pytest.approx(pin, abs=TOL)
    nut_z = -P.CASE_BACK_T + P.NUT_14_20_H / 2
    flats = min(medir.gap_width(base, (0, 0, nut_z), "x"), medir.gap_width(base, (0, 0, nut_z), "y"))
    assert flats == pytest.approx(P.NUT_14_20_FLATS + P.CLEARANCE_PRESS, abs=TOL)


def test_lente_libre(base, lid):
    """P5: ninguna pieza impresa entra en la holgura alrededor del portalente."""
    r = P.LENS_BARREL_D / 2 + P.LENS_KEEPOUT - TOL
    keepout = Location((0, 0, carcasa.FRONT_Z)) * Cylinder(r, 30, align=(Align.CENTER, Align.CENTER, Align.MAX))
    for part in (base, lid):
        inter = part & keepout
        assert sum(s.volume for s in inter.solids()) == pytest.approx(0, abs=1e-6)
    hole = medir.gap_width(lid, (0, 0, carcasa.FRONT_Z - P.CASE_LID_T / 2), "x", span=60)
    assert hole == pytest.approx(P.LENS_CLEAR_D, abs=TOL)


def _wedge_angle(part):
    planes = [f for f in part.faces() if f.geom_type == GeomType.PLANE]
    top = max((f for f in planes if f.normal_at().Z > 0.99), key=lambda f: f.area)
    bottom = max((f for f in planes if f.normal_at().Z < -0.5), key=lambda f: f.area)
    cosang = -top.normal_at().dot(bottom.normal_at())
    return math.degrees(math.acos(max(-1.0, min(1.0, cosang))))


@pytest.mark.parametrize("angle", P.ANGLE_SET)
def test_angulo_de_cada_cuna(wedges, angle):
    assert _wedge_angle(wedges[angle]) == pytest.approx(angle, abs=0.01)


@pytest.mark.parametrize("angle", P.ANGLE_SET)
def test_cuna_canto_fino_y_tornillo(wedges, angle):
    w = wedges[angle]
    x = P.CASE_OUTER / 2 - 0.5
    assert medir.solid_width(w, (x, 8, -P.WEDGE_T0 / 2), "z") >= P.WALL_STRUCT
    # El tornillo de 1/2" llega a la tuerca de la carcasa y no la atraviesa más de 1 mm.
    reach = P.BOLT_14_20_LEN - P.WEDGE_SEAT - (P.CASE_BACK_T - P.NUT_14_20_H)
    assert P.NUT_14_20_H * 0.8 <= reach <= P.NUT_14_20_H + 1.0


def test_todo_cabe_en_la_cama(base, lid, wedges):
    for part in (base, lid, *wedges.values()):
        assert medir.fits_bed(part, P.BED), part.label
