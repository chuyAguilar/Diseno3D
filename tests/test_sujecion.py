"""Fase 3 del spec 001: carro, pinza de borde y clip, medidos sobre el modelo (P3)."""
import pytest

from cad import medir
from cad import params as P
from cad.piezas import carro, clip_cable, perfil_2020, pinza_caja

TOL = 0.01


@pytest.fixture(scope="module")
def perfil():
    return perfil_2020.build(length=120)


@pytest.fixture(scope="module")
def parts():
    return {"carro": carro.build(), "pinza": pinza_caja.build(), "clip": clip_cable.build()}


def _overlap(a, b):
    return sum(s.volume for s in (a & b).solids())


@pytest.mark.parametrize("name", ["carro", "pinza", "clip"])
def test_sin_interferencia_con_el_perfil(perfil, parts, name):
    assert _overlap(perfil, parts[name]) == pytest.approx(0, abs=1e-6)


def test_llave_del_carro(parts):
    c = parts["carro"]
    key_z = P.PROFILE_BOTTOM + P.KEY_H / 2
    assert medir.solid_width(c, (0, 0, key_z), "y") == pytest.approx(P.SLOT_OPENING - P.CLEARANCE_SLIDE, abs=TOL)
    assert P.KEY_H < P.SLOT_LIP


def test_carro_m5_y_m3(parts):
    c = parts["carro"]
    z = carro.BOTTOM_Z + P.M5_HEAD_H + 2
    assert medir.gap_width(c, (P.CARRO_M5_X, 0, z), "y") == pytest.approx(P.M5_D + P.HOLE_COMP + P.CLEARANCE_SLIDE,
                                                                        abs=TOL)
    z = (carro.TOP_Z + carro.BOTTOM_Z) / 2
    assert medir.gap_width(c, (0, P.WEDGE_M3_Y, z), "x") == pytest.approx(P.M3_D + P.HOLE_COMP + P.CLEARANCE_SLIDE,
                                                                        abs=TOL)


def test_boca_de_la_pinza(parts):
    p = parts["pinza"]
    z = pinza_caja.RIM_TOP - P.PINZA_JAW_DEPTH / 4
    assert medir.gap_width(p, (0, 8, z), "x") == pytest.approx(P.BOX_RIM + P.CLEARANCE_SLIDE, abs=TOL)


def test_cuna_de_la_pinza(parts):
    p = parts["pinza"]
    assert medir.gap_width(p, (0, 0, 3), "y") == pytest.approx(P.PROFILE_SIZE + P.CLEARANCE_SLIDE, abs=TOL)


def test_clip_cierre_y_anillo(parts):
    c = parts["clip"]
    assert P.SLOT_OPENING < P.CLIP_TAB_L < P.SLOT_CHAMBER_W
    neck_z = clip_cable.TOP - P.SLOT_LIP / 2
    assert medir.solid_width(c, (0, 0, neck_z), "x") == pytest.approx(P.SLOT_OPENING - P.CLEARANCE_SLIDE, abs=0.02)
    ring = medir.gap_width(c, (0, 0, clip_cable.RING_Z), "y", span=30)  # la abertura está arriba
    assert ring == pytest.approx(P.CABLE_D + P.CLEARANCE_SLIDE, abs=TOL)


@pytest.mark.parametrize("name", ["carro", "pinza", "clip"])
def test_cabe_en_la_cama(parts, name):
    assert medir.fits_bed(parts[name], P.BED)
