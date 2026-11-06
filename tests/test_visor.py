"""El visor escribe un HTML autocontenido con una pieza glTF válida por pieza."""
import base64
import json
import re

from build123d import Box, Location

from cad import visor


def test_visor_autocontenido(tmp_path):
    parts = [("A", "pieza", "#2459B8", Box(10, 20, 30)),
             ("B", "pieza", "#C2570F", Location((40, 0, 0)) * Box(5, 5, 5))]
    dest = visor.write(parts, tmp_path / "visor.html", "prueba", notes=["nota"])
    page = dest.read_text(encoding="utf-8")
    data = json.loads(re.search(r'id="data">(.*?)</script>', page, re.S).group(1).replace("<\\/", "</"))
    assert [p["name"] for p in data["parts"]] == ["A", "B"]
    assert data["parts"][0]["size"] == [10, 20, 30]
    assert all(base64.b64decode(p["glb"])[:4] == b"glTF" for p in data["parts"])
