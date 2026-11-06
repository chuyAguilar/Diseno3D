"""Genera docs/PARAMETROS.md a partir de los params.py (P4: el documento no es fuente).

Uso: .venv\\Scripts\\python.exe -m cad.listar_params
`tests/test_parametros_doc.py` falla si el documento quedó desactualizado.
"""
import ast
import importlib
import io
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PARAMETROS.md"
SOURCES = [("cad.params", "Barra estéreo (`cad/params.py`)")] + [
    (f"taller.{p.parent.name}.params", f"Taller · {p.parent.name} (`taller/{p.parent.name}/params.py`)")
    for p in sorted((ROOT / "taller").glob("*/params.py"))]


def _fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, tuple):
        return "(" + ", ".join(_fmt(x) for x in v) + ")"
    return repr(v) if isinstance(v, str) else str(v)


def _comments(src):
    """{línea: comentario} y [(línea, título de sección)] desde los `# --- … ---`."""
    by_line, sections = {}, []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            text = tok.string.lstrip("#").strip()
            m = re.fullmatch(r"-{2,}\s*(.*?)\s*-{2,}", text)
            if m:
                sections.append((tok.start[0], m.group(1)))
            else:
                by_line[tok.start[0]] = text
    return by_line, sections


def _users(name, own):
    pat = re.compile(rf"\b{re.escape(name)}\b")
    bare = re.compile(rf"(?<![\"'])\b{re.escape(name)}\b(?![\"'])")   # sin contar la lista SIN_MEDIR
    out = ["otros parámetros"] if len(bare.findall(own.read_text(encoding="utf-8"))) > 1 else []
    for path in sorted([*ROOT.glob("cad/**/*.py"), *ROOT.glob("taller/**/*.py")]):
        if path == own or path.name == "listar_params.py":
            continue
        if pat.search(path.read_text(encoding="utf-8")):
            out.append(path.relative_to(ROOT).as_posix().removesuffix(".py").replace("cad/piezas/", "piezas/"))
    return ", ".join(f"`{u}`" for u in out) or "—"


def section(modname, title):
    mod = importlib.import_module(modname)
    path = Path(mod.__file__)
    src = path.read_text(encoding="utf-8")
    comments, sections = _comments(src)
    unmeasured = set(getattr(mod, "SIN_MEDIR", ()))
    rows, current = [], None
    lines = [f"## {title}", ""]
    for node in ast.parse(src).body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if name == "SIN_MEDIR":
            continue
        head = [t for ln, t in sections if ln < node.lineno]
        if head and head[-1] != current:
            current = head[-1]
            rows.append(f"| **{current}** | | | | |")
        expr = ast.get_source_segment(src, node.value)
        value = _fmt(getattr(mod, name))
        how = "" if expr.strip() == repr(getattr(mod, name)) or re.fullmatch(r"[-\d.]+", expr) else f"`{expr}`"
        note = comments.get(node.lineno, "")
        if name in unmeasured:
            note = ("**SIN MEDIR** · " + note).rstrip(" ·")
        rows.append(f"| `{name}` | {value} | {how or '—'} | {note or '—'} | {_users(name, path)} |")
    lines += ["| Nombre | Valor | Se calcula como | Nota (del comentario) | Lo usan |",
              "| --- | --- | --- | --- | --- |", *rows, ""]
    return lines


def render():
    out = ["# Parámetros — tabla generada", "",
           "**No se edita a mano.** Sale de los `params.py` con `.venv\\Scripts\\python.exe -m cad.listar_params`;",
           "la prueba `tests/test_parametros_doc.py` falla si no coincide. Para cambiar un valor se cambia",
           "su `params.py` (P4) y se regenera. Unidades: mm y grados. «SIN MEDIR» = valor de la carcasa",
           "de referencia, pendiente de calibre (B4).", ""]
    for modname, title in SOURCES:
        out += section(modname, title)
    return "\n".join(out)


def main():
    DOC.write_text(render(), encoding="utf-8")
    print(f"Escrito {DOC.relative_to(ROOT)} ({DOC.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
