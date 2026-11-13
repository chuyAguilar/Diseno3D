"""Imágenes del mecanismo de separación: estación de cámara, proceso en 4 pasos y tornillería.

Uso: .venv\\Scripts\\python.exe -m concepto.separacion.render
Escribe en salidas/concepto-separacion/: separacion-1-estacion.png, separacion-2-proceso.png,
separacion-3-tornillos.png.
"""
import tempfile
import time
from pathlib import Path

import matplotlib
import pyvista as pv

from cad.exportar import COLORS as V1, _stl
from concepto.separacion import modelo as M

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "salidas" / "concepto-separacion"
BG = "#FAFAF8"
INK = "#15202A"
COL = {**V1, "regleta": "#B8932A", "diente": "#2E7D4F", "tornillo": "#7D848C"}
ANG = 15.0
DROP = 6.5                        # lo que baja el carro para sacar el diente (TOOTH_H + holgura)
M5_PITCH = 0.8


def mesh(shape):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "m.stl"
        _stl(shape, p, tolerance=0.02, angular_tolerance=0.15)
        return pv.read(str(p))


def add(pl, parts, translucent=()):
    for name, shape, role in parts:
        op = 0.45 if role in translucent else 1.0
        pl.add_mesh(mesh(shape), color=COL[role], opacity=op, smooth_shading=False,
                    specular=0.4 if role in ("aluminio", "tornillo") else 0.1)


def label(pl, pts_texts, size=14):
    for pt, text in pts_texts:
        pl.add_point_labels([pt], [text], font_size=size, text_color=INK, shape_color="white", shape_opacity=0.9,
                            point_size=7, point_color=INK, always_visible=True, margin=4)


def numbers(pl, side=-1, seps=M.SEPS):
    pts = [(M.notch_x(s, side), M.REG_Y1 + 0.5, M.H + 3) for s in seps]
    pl.add_point_labels(pts, [f"{s:.0f}" for s in seps], font_size=13, text_color="#6B4E00", shape_opacity=0.0,
                        show_points=False, always_visible=True)


def carro_bottom():
    from cad.piezas import carro
    return carro.BOTTOM_Z


def estacion_png(fixed):
    sep = 150.0
    xc = -sep / 2
    pl = pv.Plotter(off_screen=True, window_size=(1900, 1350))
    pl.set_background(BG)
    pl.enable_anti_aliasing("ssaa")
    add(pl, fixed)
    add(pl, M.estacion(sep, ANG))
    numbers(pl, seps=M.SEPS[:6])
    est = M.estacion(sep, ANG)
    tapa = next(sh for n, sh, r in est if n.startswith("BE-CARCASA-TAPA")).bounding_box()
    cuna = next(sh for n, sh, r in est if n.startswith("BE-CUNA")).bounding_box()
    ax = M.notch_x(sep, -1)
    label(pl, [((xc + M.CARRO2_M5_X, 0, carro_bottom()), "1"), ((-M.REG_SCREW_X, M.REG_Y1 + 2.75, 0), "2"),
               ((xc, 15, -7), "3"), ((cuna.center().X, cuna.center().Y, cuna.min.Z + 2), "4"),
               ((tapa.max.X - 6, tapa.min.Y + 6, tapa.min.Z), "5")], size=22)
    label(pl, [((-140, M.REG_Y1, 8), "Regleta: muesca en V por separación, con su número"),
               ((ax, M.REG_Y1 + 6, -3), "Diente del carro")], size=15)
    pl.add_text("Estación de cámara con regleta — separación S150 (vista desde abajo y delante)\n"
                "Se mueve: carro, cuña, carcasa y cámara. Fijo: perfil y regleta. Los números 1–5 son los tornillos de la tabla.\n"
                "Carro v02 de 90 mm: sus 2 M5 (1) quedan fuera de la cuña y se aflojan sin desmontar la cámara.",
                position="upper_left", font_size=12, color=INK)
    pl.camera_position = [(xc + 150, 300, -140), (xc + 5, 0, -25), (0, 0, 1)]
    pl.screenshot(str(OUT / "separacion-1-estacion.png"))
    pl.close()


def proceso_png(fixed):
    s0, s1 = 150.0, 175.0
    x0, x1 = -s0 / 2, -s1 / 2
    turns = DROP / M5_PITCH
    steps = [
        (f"1 · Montado en {s0:.0f}: el diente está dentro de la muesca «{s0:.0f}»", dict(sep=s0)),
        (f"2 · Afloja los 2 M5 del carro unas {turns:.0f} vueltas y baja el carro {DROP:g} mm:\n"
         "    el diente sale de la muesca; las tuercas en T siguen en la ranura", dict(sep=s0, drop=DROP)),
        (f"3 · Desliza el carro (con cuña y cámara) hasta la muesca «{s1:.0f}»", dict(sep=s0, drop=DROP, x_override=x1)),
        (f"4 · Sube el carro: la V lo centra sola. Aprieta los 2 M5.\n"
         f"    Repite con la otra cámara en «{s1:.0f}» y recalibra el par estéreo", dict(sep=s1)),
    ]
    pl = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(2200, 1500), border=True, border_color="#D9D6CE")
    for k, (title, kw) in enumerate(steps):
        pl.subplot(k // 2, k % 2)
        pl.set_background(BG)
        add(pl, fixed)
        sep = kw.pop("sep")
        add(pl, M.estacion(sep, ANG, **kw), translucent=("diente",))
        numbers(pl, seps=(125.0, 150.0, 175.0, 200.0))
        pl.add_text(title, position="upper_left", font_size=11, color=INK)
        cx = (x0 + x1) / 2
        pl.camera_position = [(cx + 10, 320, -50), (cx + 10, 0, -12), (0, 0, 1)]
        pl.enable_parallel_projection()
        pl.camera.parallel_scale = 48
    pl.screenshot(str(OUT / "separacion-2-proceso.png"))
    pl.close()


def tornillos_png():
    rows = [
        ("1", "Carro a perfil", "M5 x 10, Allen DIN 912", "2", "Tuerca en T M5 para ranura de 6 mm (2020), en la ranura inferior.\n"
                                                                 "En x = ±40 mm, fuera de la cuña y de la carcasa: se aflojan\n"
                                                                 "con llave Allen de 4 mm sin desmontar nada"),
        ("2", "Regleta a perfil", "M5 x 10, botón ISO 7380", "2 en total", "Tuerca en T M5 en la ranura lateral, en x = ±25 mm:\nno estorba al diente en ninguna separación"),
        ("3", "Cuña a carro", "M3, Allen DIN 912", "2", "Tuerca M3 en la cuña. Largo según la cuña: 20 mm (0°) o 25 mm (12.5°).\n"
                                                         "Las demás cuñas no tienen largo estándar. Propuesta: inserto\n"
                                                         "térmico M3 en la cuña y M3 x 12 para todas"),
        ("4", "Carcasa a cuña", "1/4-20 x 1/2\" (12.7 mm)", "1", "Tuerca 1/4-20 insertada en la carcasa, más 2 pasadores\n"
                                                                 "de acero Ø3 x 12 contra el giro"),
        ("5", "Tapa de la carcasa", "M3 x 8, Allen DIN 912", "4", "Tuerca M3 en la brida. Ninguna pieza toca el lente (P5)"),
    ]
    fig, ax = plt.subplots(figsize=(17, 5.6), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.axis("off")
    ax.set_title("Tornillería de una estación de cámara (por cámara, salvo la regleta)", loc="left", fontsize=14,
                 color=INK, pad=12, fontweight="bold")
    table = ax.table(cellText=rows, colLabels=("#", "Unión", "Tornillo", "Cantidad", "Nota"), loc="upper left",
                     cellLoc="left", colLoc="left", colWidths=(0.03, 0.13, 0.2, 0.08, 0.56))
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#D9D6CE")
        cell.set_height(0.08 + 0.055 * (rows[r - 1][4].count("\n") if r else 0) + (0.02 if r == 0 else 0))
        if r == 0:
            cell.set_facecolor("#E9E6DE")
            cell.set_text_props(fontweight="bold", color=INK)
        else:
            cell.set_facecolor("white")
            cell.set_text_props(color=INK)
    fig.savefig(OUT / "separacion-3-tornillos.png", bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    fixed = M.fijo()
    estacion_png(fixed)
    proceso_png(fixed)
    tornillos_png()
    print(f"{time.time() - t0:.0f} s -> {OUT}")


if __name__ == "__main__":
    main()
