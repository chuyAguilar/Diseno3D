"""Cotas de interfaz medidas sobre el modelo (P3). Es la comprobación de «no cambió» (B2)."""
import pytest

from cad import medir
from cad import params as P
from cad.piezas import perfil_2020, probeta

TOL = 0.01


@pytest.fixture(scope="module")
def perfil():
    return perfil_2020.build()


@pytest.fixture(scope="module")
def prob():
    return probeta.build()


def test_parametros_coherentes():
    assert P.ANGLE_SET == (0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0)
    assert all(s % P.SEP_STEP == 0 for s in P.SEP_SET)
    assert P.PRESENTATION_CONFIG[0] in P.SEP_SET and P.PRESENTATION_CONFIG[1] in P.ANGLE_SET
    assert P.CASE_REF_CAVITY > P.CAM_BOARD
    assert all(hasattr(P, n) for n in P.SIN_MEDIR)


def test_perfil_seccion_y_ranura(perfil):
    bb = perfil.bounding_box()
    assert bb.size.X == pytest.approx(P.PROFILE_LEN, abs=TOL)
    assert bb.size.Y == pytest.approx(P.PROFILE_SIZE, abs=TOL)
    assert bb.size.Z == pytest.approx(P.PROFILE_SIZE, abs=TOL)
    # Boca de la ranura superior, medida a media altura del labio.
    z_lip = P.PROFILE_SIZE / 2 - P.SLOT_LIP / 2
    assert medir.gap_width(perfil, (0, 0, z_lip), "y") == pytest.approx(P.SLOT_OPENING, abs=TOL)


def test_probeta_cabe_en_la_cama(prob):
    assert medir.fits_bed(prob, P.BED)


@pytest.mark.parametrize("i", range(len(P.PROBE_CLEARANCES)))
def test_probeta_holguras(prob, i):
    item = probeta.layout()[i]
    c = item["clearance"]
    assert medir.gap_width(prob, item["pin"], "x") == pytest.approx(P.PIN_D + P.HOLE_COMP + c, abs=TOL)
    flats = min(medir.gap_width(prob, item["nut"], "x"), medir.gap_width(prob, item["nut"], "y"))
    assert flats == pytest.approx(P.NUT_14_20_FLATS + c, abs=TOL)
    assert medir.solid_width(prob, item["key"], "x") == pytest.approx(P.SLOT_OPENING - c, abs=TOL)
    assert medir.gap_width(prob, item["notch"], "x") == pytest.approx(P.BOX_RIM + c, abs=TOL)
