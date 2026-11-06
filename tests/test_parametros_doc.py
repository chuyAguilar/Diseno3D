"""docs/PARAMETROS.md está al día con los params.py (P4)."""
from cad import listar_params


def test_parametros_doc_al_dia():
    assert listar_params.DOC.read_text(encoding="utf-8") == listar_params.render(), \
        "docs/PARAMETROS.md desactualizado: .venv\\Scripts\\python.exe -m cad.listar_params"
