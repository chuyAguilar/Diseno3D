"""Renders y visor del concepto v02 (barra en la abertura con inclinación indexada).

Uso: .venv\\Scripts\\python.exe -m concepto.abertura.render
Escribe en salidas/concepto-abertura/: 1-frente.png, 2-lateral.png, 3-pivote.png,
4-inclinaciones.png, visor.html y datos.txt.
"""
import math
import tempfile
import time
from pathlib import Path

import pyvista as pv

from cad import visor
from cad.exportar import COLORS as V1_COLORS, _stl
from concepto.abertura import modelo as M
from concepto.abertura import params as P

OUT = Path(__file__).resolve().parents[2] / "salidas" / "concepto-abertura"
COLORS = {**V1_COLORS, "pivote": "#5B6B3A", "cubo": "#8C8C84", "pasador": "#B4361C", "caja": "#EDEAE2"}
BG = "#FAFAF8"


def meshes(items):
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, it in enumerate(items):
            path = Path(tmp) / f"{k:02d}.stl"
            _stl(it.part, path, tolerance=0.05, angular_tolerance=0.2)
            out.append((it, pv.read(str(path))))
    return out


def optics(sep, conv, pitch):
    axes = M.camera_axes(sep, conv, pitch)
    cross, along = M.crossing(axes)
    lens_sep = (axes[1][0] - axes[0][0]).length
    return axes, cross, along, lens_sep


def _reach(p, u):
    """Largo del eje hasta el suelo o la pared del fondo, lo que llegue antes."""
    ts = [p.Z / -u.Z] if u.Z < 0 else []
    if u.Y > 0:
        ts.append((P.BOX_SIZE / 2 - p.Y) / u.Y)
    return min(ts) if ts else 600


def inside(c):
    return c.Y <= P.BOX_SIZE / 2 + 1 and c.Z >= -1


def where(c, along):
    if c is None:
        return "los ejes no se cruzan"
    if c.Y > P.BOX_SIZE / 2 + 1:
        return f"cruce detrás de la pared del fondo ({c.Y - P.BOX_SIZE / 2:.0f} mm): menos cuña"
    if c.Z < -1:
        return f"cruce {-c.Z:.0f} mm bajo el suelo: más cuña"
    alt = "en el suelo" if abs(c.Z) < 2 else f"{c.Z:.0f} mm sobre el suelo"
    return f"cruce a {along:.0f} mm de los lentes, {alt}"


def scene(pl, ms, sep, conv, pitch, hide=(), box_opacity=0.22):
    for it, mesh in ms:
        if it.name in hide:
            continue
        col = COLORS[it.role]
        if it.role == "caja" and it.name.startswith("Caja"):
            pl.add_mesh(mesh, color=col, opacity=box_opacity)
        else:
            pl.add_mesh(mesh, color=col, smooth_shading=False, specular=0.3 if it.role == "aluminio" else 0.1)
    axes, cross, _, _ = optics(sep, conv, pitch)
    for (p, u), col in zip(axes, (COLORS["cámara 1"], COLORS["cámara 2"])):
        pl.add_mesh(pv.Line(tuple(p), tuple(p + u * _reach(p, u))), color=col, line_width=3)
    if cross is not None and inside(cross):
        pl.add_mesh(pv.Sphere(radius=5, center=tuple(cross)), color="#B4361C")


def shot(name, ms, title, cam, sep=P.SEP, conv=P.CONV, pitch=P.PITCH, hide=(), parallel=False, labels=(),
         size=(1800, 1250), box_opacity=0.22):
    pl = pv.Plotter(off_screen=True, window_size=size)
    pl.set_background(BG)
    pl.enable_anti_aliasing("ssaa")
    scene(pl, ms, sep, conv, pitch, hide, box_opacity)
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
    axes, cross, along, lens_sep = optics(P.SEP, P.CONV, P.PITCH)
    code = f"S{P.SEP:.0f}-A{P.CONV:g}-P{P.PITCH:g}"
    sub = (f"{code} · lentes a {lens_sep:.0f} mm · cuña {P.CONV:g}° · inclinación {P.PITCH:g}° · "
           f"ejes cruzados a {along:.0f} mm, sobre el suelo junto al fondo")
    ax_y, ax_z, end = M.AXIS_Y, M.AXIS_Z, M.END_X

    shot("1-frente.png", ms, f"Concepto v02 — barra en el borde superior de la abertura\n{sub}",
         [(-280, -880, 600), (0, 20, 210), (0, 0, 1)],
         labels=[((-end - 10, ax_y - 20, ax_z + 50), "pinza al canto + pivote indexado"),
                 ((-60, ax_y + 15, ax_z + 25), "perfil 2020 + regleta"),
                 ((tuple(cross)), "cruce de ejes")])
    shot("2-lateral.png", ms, f"Vista lateral (pared derecha oculta): la barra gira {P.PITCH:g}° sobre su eje\n{sub}",
         [(1400, 0, 210), (0, 0, 210), (0, 0, 1)], hide=("Caja pared dcha",), parallel=True,
         labels=[((0, -P.BOX_SIZE / 2, P.BOX_SIZE + 25), "abertura (frente)"),
                 ((0, P.BOX_SIZE / 2, P.BOX_SIZE + 25), "fondo")])
    shot("3-pivote.png", ms, "Pivote: la placa muerde el canto del techo; el cubo gira con el perfil y un pasador "
         f"lo fija en un agujero cada {P.PITCH_STEP:g}°",
         [(end + 190, ax_y - 210, ax_z + 70), (end + 5, ax_y + 5, ax_z - 5), (0, 0, 1)],
         hide=("Caja pared dcha",), size=(1500, 1200), box_opacity=0.15,
         labels=[((end + P.HUB_T + P.PLATE_T + P.KNOB_T, ax_y, ax_z), "perilla de apriete"),
                 ((end + 12, ax_y - 15, ax_z + P.PIVOT_BELOW + 12), "mordaza al canto (M5)")])

    pl = pv.Plotter(off_screen=True, shape=(1, len(P.PITCH_COMPARE)), window_size=(2400, 900), border=False)
    for k, pitch in enumerate(P.PITCH_COMPARE):
        pl.subplot(0, k)
        pl.set_background(BG)
        sub_ms = meshes(M.build(pitch=pitch))
        scene(pl, sub_ms, P.SEP, P.CONV, pitch, hide=("Caja pared dcha",))
        _, c, al, _ = optics(P.SEP, P.CONV, pitch)
        pl.add_text(f"inclinación {pitch:g}°  ·  {where(c, al)}", position="upper_left", font_size=12, color="#15202A")
        pl.camera_position = [(1400, 0, 210), (0, 0, 210), (0, 0, 1)]
        pl.enable_parallel_projection()
    pl.screenshot(str(OUT / "4-inclinaciones.png"))
    pl.close()

    color = {**COLORS, "caja": "#D9D6CE"}
    visor.write([(it.name, it.role, color[it.role], it.part) for it in items], OUT / "visor.html",
                "Barra estéreo v02",
                notes=[f"Separación entre lentes: {lens_sep:.1f} mm", f"Cuña por cámara: {P.CONV:g}°",
                       f"Inclinación de la barra: {P.PITCH:g}° (índice cada {P.PITCH_STEP:g}°)",
                       f"Ejes cruzados a {along:.0f} mm de los lentes, en y = {cross.Y:.0f}, z = {cross.Z:.0f}"],
                lines=[(tuple(p), tuple(p + u * _reach(p, u)), COLORS[f"cámara {i + 1}"])
                       for i, (p, u) in enumerate(axes)],
                points=[(tuple(cross), "#B4361C", "cruce")], panel=False,
                subtitle=f"Concepto {code} · lentes a {lens_sep:.0f} mm · ejes cruzados a {along:.0f} mm",
                share=OUT / "visor-pagina.html")

    lines = [f"Concepto v02 {code}", f"Lentes en {tuple(round(v, 1) for v in axes[0][0])} y "
             f"{tuple(round(v, 1) for v in axes[1][0])}; separación {lens_sep:.1f} mm",
             f"Dirección del eje 1: {tuple(round(v, 3) for v in axes[0][1])} "
             f"({math.degrees(math.acos(-axes[0][1].Z)):.1f}° desde la vertical)",
             f"Cruce de ejes: y = {cross.Y:.1f}, z = {cross.Z:.1f} mm; {along:.1f} mm a lo largo de cada eje", ""]
    for pitch in P.PITCH_COMPARE:
        _, c, al, _ = optics(P.SEP, P.CONV, pitch)
        lines.append(f"Inclinación {pitch:g}°: cruce en y = {c.Y:.1f}, z = {c.Z:.1f} mm ({where(c, al)})")
    (OUT / "datos.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\n{time.time() - t0:.0f} s -> {OUT}")


if __name__ == "__main__":
    main()
