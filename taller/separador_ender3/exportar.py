"""Exporta los separadores para imprimir y revisar.

Uso: .venv\\Scripts\\python.exe -m taller.separador_ender3.exportar

Escribe en taller/separador_ender3/salidas/:
  SEP-ENDER3-L*.stl   una pieza por archivo
  separadores.3mf     las dos piezas, para Bambu Studio (solo geometría: la capa se elige allí)
  vista.png           vista previa
  datos.txt           cotas medidas sobre el modelo
"""
import tempfile
from pathlib import Path

import pyvista as pv
from build123d import Location, Mesher

from cad.exportar import _stl
from taller.separador_ender3 import medir_pieza, modelo
from taller.separador_ender3 import params as P

OUT = Path(__file__).resolve().parent / "salidas"
GAP = 6.0      # entre piezas en el 3MF y en la vista


def main():
    OUT.mkdir(exist_ok=True)
    parts = modelo.variants()
    placed = [Location((k * (P.OUTER_D + GAP), 0, 0)) * p for k, p in enumerate(parts)]
    mesher = Mesher()
    for part, p in zip(parts, placed):
        _stl(part, OUT / f"{part.label}.stl")
        mesher.add_shape(p, part_number=part.label)
    mesher.write(str(OUT / "separadores.3mf"))

    pl = pv.Plotter(off_screen=True, window_size=(1400, 1000))
    pl.set_background("#FAFAF8")
    pl.enable_anti_aliasing("ssaa")
    with tempfile.TemporaryDirectory() as tmp:
        for k, p in enumerate(placed):
            path = Path(tmp) / f"{k}.stl"
            _stl(p, path, tolerance=0.01, angular_tolerance=0.1)
            pl.add_mesh(pv.read(str(path)), color=("#2459B8", "#C2570F")[k], smooth_shading=True,
                        split_sharp_edges=True, specular=0.3)
            bb = p.bounding_box()
            pl.add_point_labels([(bb.center().X, 0, bb.max.Z + 2.5)], [parts[k].label], font_size=16,
                                shape_opacity=0.0, show_points=False, text_color="#15202A",
                                always_visible=True)
    pl.add_text("Separadores de cama Ender 3 V3 (PETG, capa 0.1 mm) · 1 ranura = 15.0 mm, 2 ranuras = 14.7 mm",
                position="upper_left", font_size=11, color="#15202A")
    pl.camera_position = [(28, -40, 24), ((P.OUTER_D + GAP) / 2, 0, 7.5), (0, 0, 1)]
    pl.enable_parallel_projection()   # sin perspectiva: los largos se comparan a la vista
    pl.reset_camera()
    pl.screenshot(str(OUT / "vista.png"))
    pl.close()

    lines = [f"Original: largo {P.ORIG_LEN} mm, Ø ext {P.OUTER_D} mm, agujero {P.BORE_MEASURED} mm (fotos/)",
             f"Agujero dibujado: {P.BORE_D:.2f} mm (+{P.BORE_D - P.BORE_MEASURED:.2f} de compensación)",
             f"Imprimir en PETG, de pie, capa {P.LAYER_H} mm", ""]
    for part in parts:
        m = medir_pieza.medidas(part)
        lines.append(f"{part.label}: largo {m['largo']:.2f} mm, Ø ext {m['exterior']:.2f} mm, "
                     f"agujero {m['agujero']:.2f} mm, {m['ranuras']} ranura(s), "
                     f"{m['largo'] / P.LAYER_H:.1f} capas")
    (OUT / "datos.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nEscrito en {OUT}")


if __name__ == "__main__":
    main()
