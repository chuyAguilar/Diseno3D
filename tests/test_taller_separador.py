"""Spec 003: separadores de cama de la Ender 3 V3, medidos sobre el modelo (P3)."""
import pytest

from taller.separador_ender3 import medir_pieza, modelo

TOL = 0.01


@pytest.fixture(scope="module")
def piezas():
    return {p.label: medir_pieza.medidas(p) for p in modelo.variants()}


@pytest.mark.parametrize("label, largo, ranuras", [("SEP-ENDER3-L15.0", 15.0, 1), ("SEP-ENDER3-L14.7", 14.7, 2)])
def test_separador(piezas, label, largo, ranuras):
    m = piezas[label]
    assert m["largo"] == pytest.approx(largo, abs=TOL)
    assert m["exterior"] == pytest.approx(7.8, abs=TOL)
    assert m["agujero"] == pytest.approx(4.7, abs=TOL)
    assert m["ranuras"] == ranuras
