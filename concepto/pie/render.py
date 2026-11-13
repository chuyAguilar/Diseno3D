"""Renders y visor del concepto de pie (pórtico que no toca la caja).

Uso: .venv\\Scripts\\python.exe -m concepto.pie.render
Escribe en salidas/concepto-pie/: 1-frente.png, 2-lateral.png, visor.html, visor-pagina.html y datos.txt.
"""
import time
from pathlib import Path

import pyvista as pv

from cad import visor
from concepto.abertura import modelo as A
from concepto.abertura.render import BG, COLORS as A_COLORS, _reach, meshes, where
from concepto.pie import modelo as M
from concepto.pie import params as P

OUT = Path(__file__).resolve().parents[2] / "salidas" / "concepto-pie"
COLORS = {**A_COLORS, "mesa": "#B9A88E"}


def shot(name, ms, axes, cross, title, cam, hide=(), parallel=False, labels=()):
    pl = pv.Plotter(off_screen=True, window_size=(1800, 1250))
    pl.set_background(BG)
    pl.enable_anti_aliasing("ssaa")
    for it, mesh in ms:
        if it.name in hide:
            continue
        if it.role == "caja" and it.name.startswith("Caja"):
            pl.add_mesh(mesh, color=COLORS["caja"], opacity=0.22)
        else:
            pl.add_mesh(mesh, color=COLORS[it.role], smooth_shading=False,
                        specular=0.3 if it.role == "aluminio" else 0.1)
    for (p, u), col in zip(axes, (COLORS["cámara 1"], COLORS["cámara 2"])):
        pl.add_mesh(pv.Line(tuple(p), tuple(p + u * _reach(p, u))), color=col, line_width=3)
    if cross is not None:
        pl.add_mesh(pv.Sphere(radius=5, center=tuple(cross)), color="#B4361C")
    for pt, text in labels:
        pl.add_point_labels([pt], [text], font_size=15, text_color="#15202A", shape_color="white", shape_opacity=0.85,
                            point_size=8, point_color="#15202A", always_visible=True, margin=4)
    pl.add_text(title, position="upper_left", font_size=12, color="#15202A")
    pl.camera_position = cam
    if parallel:
        pl.enable_parallel_projection()
    pl.screenshot(str(OUT / name))
    pl.close()


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    items = M.build()
    ms = meshes(items)
    axes = M.camera_axes(P.SEP, P.CONV, P.PITCH)
    cross, along = A.crossing(axes)
    lens_sep = (axes[1][0] - axes[0][0]).length
    code = f"S{P.SEP:.0f}-A{P.CONV:g}-P{P.PITCH:g}"
    sub = (f"{code} · lentes a {lens_sep:.0f} mm · cuña {P.CONV:g}° · inclinación {P.PITCH:g}° · "
           f"{where(cross, along)}")

    shot("1-frente.png", ms, axes, cross, f"Concepto v02-B — pórtico de pie, no toca la caja\n{sub}",
         [(-620, -1150, 760), (0, -60, 200), (0, 0, 1)],
         labels=[((-M.POST_X, M.POST_WY, P.AXIS_Z + 45), "poste 2020 + pivote indexado"),
                 ((-M.POST_X, P.FOOT_Y[0] + 40, 30), "pata 2020 sobre la mesa"),
                 ((0, P.AXIS_Y - 20, P.AXIS_Z + 30), "barra delante de la abertura")])
    shot("2-lateral.png", ms, axes, cross, f"Vista lateral (pared derecha oculta): el pórtico queda fuera de la caja\n{sub}",
         [(1500, -150, 210), (0, -150, 210), (0, 0, 1)], hide=("Caja pared dcha",), parallel=True,
         labels=[((0, -P.BOX_SIZE / 2, P.BOX_SIZE + 30), "abertura"), ((0, P.BOX_SIZE / 2, P.BOX_SIZE + 30), "fondo")])

    color = {**COLORS, "caja": "#D9D6CE"}
    visor.write([(it.name, it.role, color[it.role], it.part) for it in items], OUT / "visor.html",
                "Pórtico barra v02", panel=False,
                subtitle=f"Concepto de pie {code} · no toca la caja · lentes a {lens_sep:.0f} mm · "
                         f"ejes cruzados a {along:.0f} mm",
                lines=[(tuple(p), tuple(p + u * _reach(p, u)), COLORS[f"cámara {i + 1}"])
                       for i, (p, u) in enumerate(axes)],
                points=[(tuple(cross), "#B4361C", "cruce")], share=OUT / "visor-pagina.html")

    lines = [f"Concepto de pie {code}", f"Separación entre lentes: {lens_sep:.1f} mm",
             f"Cruce de ejes: y = {cross.Y:.1f}, z = {cross.Z:.1f} mm; {along:.1f} mm a lo largo de cada eje",
             f"Postes en x = ±{M.POST_X:.0f} mm, y = {M.POST_WY:.0f} mm; patas de {P.FOOT_Y[1] - P.FOOT_Y[0]:.0f} mm",
             f"Barra de {P.BAR_LEN:.0f} mm con el eje en y = {P.AXIS_Y:.0f}, z = {P.AXIS_Z:.0f} mm"]
    (OUT / "datos.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\n{time.time() - t0:.0f} s -> {OUT}")


if __name__ == "__main__":
    main()
