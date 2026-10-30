"""Exporta una configuración para presentarla y fabricarla.

Uso: .venv\\Scripts\\python.exe -m cad.exportar [S150-A12.5]

Escribe en salidas/<código>/:
  ensamble.step   ensamble con nombres y colores (cualquier visor CAD)
  ensamble.3mf    el mismo ensamble para Bambu Studio
  vista-*.png     isométrica, frontal, detalle de la cuña y detalle de la pinza
  datos.txt       separación de los lentes y cruce de ejes medidos sobre el modelo
y en salidas/piezas/ un STL por pieza imprimible, en su orientación de modelado.
"""
import math
import shutil
import tempfile
import re
import sys
from pathlib import Path

import pyvista as pv
from build123d import Color, Compound, Mesher, export_step, export_stl

from cad import ensamble
from cad import params as P
from cad.piezas import carcasa, carro, clip_cable, cuna, pinza_caja, probeta

ROOT = Path(__file__).resolve().parents[1] / "salidas"
COLORS = {"impresa": "#2E3338", "aluminio": "#C3CAD1", "cámara 1": "#2459B8", "cámara 2": "#C2570F",
          "caja": "#F1EEE6", "marker": "#111111"}


def _stl(part, dest, **kw):
    """export_stl falla en silencio si la ruta tiene caracteres no ASCII (la «ñ» de Diseño3D):
    se escribe en una carpeta temporal y se mueve."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pieza.stl"
        if not export_stl(part, str(path), **kw) or not path.exists():
            raise RuntimeError(f"No se pudo exportar {dest.name}")
        shutil.move(str(path), str(dest))


def parse(code):
    m = re.fullmatch(r"S(\d+)-A(\d+(?:\.\d)?)", code)
    if not m:
        raise SystemExit(f"Código no válido: {code} (ejemplo: S150-A12.5)")
    return float(m.group(1)), float(m.group(2))


def export_parts():
    out = ROOT / "piezas"
    out.mkdir(parents=True, exist_ok=True)
    parts = [carcasa.build_base(), carcasa.build_lid(), carro.build(), pinza_caja.build(), clip_cable.build(),
             probeta.build(), *[cuna.build(a) for a in P.ANGLE_SET]]
    for p in parts:
        _stl(p, out / f"{p.label}.stl")
    return [p.label for p in parts]


def export_assembly(items, out):
    children = []
    for it in items:
        part = it.part
        part.label = it.name
        part.color = Color(COLORS[it.role])
        children.append(part)
    export_step(Compound(children=children, label="Barra estéreo v01"), str(out / "ensamble.step"))
    mesher = Mesher()
    for part in children:
        if not part.label.startswith(("Caja", "Marker")):
            mesher.add_shape(part, part_number=part.label)
    mesher.write(str(out / "ensamble.3mf"))


def render(items, sep, ang, out):
    meshes = []
    with tempfile.TemporaryDirectory() as tmp:  # ruta ASCII también para el lector de VTK
        for k, it in enumerate(items):
            path = Path(tmp) / f"{k:02d}.stl"
            _stl(it.part, path, tolerance=0.05, angular_tolerance=0.2)
            meshes.append((it, pv.read(str(path))))
    axes = ensamble.camera_axes(sep, ang)
    cross, along = ensamble.axes_crossing(sep, ang)
    code = ensamble.config_code(sep, ang)
    cables = [pv.Spline(pts, 400).tube(radius=P.CABLE_D / 2) for pts in ensamble.cable_paths(sep, ang)]

    def scene(window, title, camera, opacity_box=0.35, extra=None):
        pl = pv.Plotter(off_screen=True, window_size=window)
        pl.set_background("#FAFAF8")
        pl.enable_anti_aliasing("ssaa")
        for it, mesh in meshes:
            color = COLORS[it.role]
            if it.role == "caja":
                if it.name.startswith("Caja de luz 2"):
                    continue  # pared del fondo: tapa la vista frontal
                pl.add_mesh(mesh, color=color, opacity=opacity_box)
            else:
                pl.add_mesh(mesh, color=color, specular=0.3 if it.role == "aluminio" else 0.1, smooth_shading=False)
        for (p, u), col in zip(axes, (COLORS["cámara 1"], COLORS["cámara 2"])):
            end = p + u * (p.Z / -u.Z)
            pl.add_mesh(pv.Line(tuple(p), tuple(end)), color=col, line_width=3)
        if cross is not None:
            pl.add_mesh(pv.Sphere(radius=4, center=tuple(cross)), color="#B4361C")
        for cable in cables:
            pl.add_mesh(cable, color="#16181A")
        if extra:
            extra(pl)
        pl.add_text(title, position="upper_left", font_size=11, color="#15202A")
        pl.camera_position = camera
        return pl

    bz = ensamble.BAR_Z
    lens_sep = axes[1][0].X - axes[0][0].X
    sub = f"{code} · lentes a {lens_sep:.1f} mm · ejes cruzados a {axes[0][0].Z - cross.Z:.0f} mm bajo los lentes"
    views = {
        "vista-isometrica": ((1800, 1300), f"Barra estéreo v01 — {sub}",
                             [(620, -780, 640), (0, 0, 210), (0, 0, 1)]),
        "vista-frontal": ((1800, 1300), f"Vista frontal — {sub}",
                          [(0, -1500, 230), (0, 0, 220), (0, 0, 1)]),
        "detalle-cuna": ((1500, 1200), f"Cámara 1: carro, cuña de {ang:.1f}° grabada y carcasa con antigiro",
                         [(-sep / 2 - 160, -230, bz + 40), (-sep / 2 + 5, 0, bz - 55), (0, 0, 1)]),
        "detalle-pinza": ((1500, 1200), "Pinza al borde de la caja: muerde la pared con un M3 y sujeta el perfil con un M5",
                          [(ensamble.WALL_X + 150, -170, bz + 60), (ensamble.WALL_X, 0, bz - 25), (0, 0, 1)]),
    }
    for name, (win, title, cam) in views.items():
        pl = scene(win, title, cam, opacity_box=0.25 if name.startswith("detalle") else 0.35)
        pl.screenshot(str(out / f"{name}.png"))
        pl.close()


def main(code=None):
    sep, ang = parse(code) if code else P.PRESENTATION_CONFIG
    code = ensamble.config_code(sep, ang)
    out = ROOT / code
    out.mkdir(parents=True, exist_ok=True)
    labels = export_parts()
    items = ensamble.build(sep, ang)
    export_assembly(items, out)
    render(ensamble.build(sep, ang), sep, ang, out)
    (p1, _), (p2, _) = ensamble.camera_axes(sep, ang)
    cross, along = ensamble.axes_crossing(sep, ang)
    lines = [f"Configuración {code}",
             f"Carros en las marcas ±{sep / 2:.1f} mm",
             f"Separación entre centros de lente: {p2.X - p1.X:.2f} mm",
             f"Cuña por cámara: {ang:.1f}°  (convergencia total {2 * ang:.1f}°)",
             f"Altura de los lentes sobre el suelo (Marker0): {p1.Z:.1f} mm",
             f"Cruce de ejes: {p1.Z - cross.Z:.1f} mm bajo los lentes ({along:.1f} mm a lo largo de cada eje),"
             f" a {cross.Z:.1f} mm sobre Marker0",
             f"Cuña ideal para cruzar en Marker0: {math.degrees(math.atan((p2.X - p1.X) / 2 / p1.Z)):.1f}°",
             "", "Piezas imprimibles (salidas/piezas/): " + ", ".join(labels)]
    (out / "datos.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nEscrito en {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
