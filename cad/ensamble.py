"""Ensamble de una configuración S<sep>-A<ang> dentro de la caja de luz, con Marker0.

Marco del mundo: suelo de la caja en z = 0, centro de la caja en x = y = 0, Marker0 en
el origen. El perfil cruza la caja a lo largo de X sobre las paredes laterales, justo
encima de Marker0 (D5). La cámara 1 está en -X y la 2 en +X; la cuña de la 2 va girada 180°.

`sep` es la posición de los carros (las marcas de la barra). La separación real entre los
centros de los lentes es algo menor con cuña, porque la cuña gira la carcasa hacia dentro;
`camera_axes` la da medida sobre el ensamble.
"""
from dataclasses import dataclass

from build123d import Align, Box, Location, Plane, Vector, Vertex

from cad import params as P
from cad.piezas import carcasa, carro, clip_cable, cuna, perfil_2020, pinza_caja

BAR_Z = P.BOX_SIZE - pinza_caja.RIM_TOP          # el borde de la pared queda en z = BOX_SIZE
WALL_X = P.BOX_SIZE / 2 + P.BOX_RIM / 2
CLIP_X = (-40.0, 40.0, 120.0, 180.0)
ROT_Z180 = Location((0, 0, 0), (0, 0, 180))


@dataclass
class Item:
    name: str
    part: object
    role: str          # "impresa", "aluminio", "cámara 1", "cámara 2", "caja", "marker"


def config_code(sep, ang):
    return f"S{sep:.0f}-{cuna.code(ang)}"


def _case_location(ang):
    mp = cuna.mount_plane(ang)
    return Location(Plane(origin=mp.origin, x_dir=mp.x_dir, z_dir=-mp.z_dir))


def _camera_base(i, sep):
    """Marco del carro de la cámara i (0 o 1) en el mundo."""
    side = -1 if i == 0 else 1
    loc = Location((0, 0, BAR_Z)) * Location((side * sep / 2, 0, 0))
    return loc * ROT_Z180 if i == 1 else loc


def _case_world(i, sep, ang):
    return _camera_base(i, sep) * Location((0, 0, carro.BOTTOM_Z)) * _case_location(ang)


def camera_axes(sep, ang):
    """[(centro del lente, dirección)] de cada cámara; el centro es la cara frontal de la placa."""
    out = []
    for i in (0, 1):
        loc = _case_world(i, sep, ang)
        p0 = Vector((loc * Vertex(0, 0, carcasa.FRONT_Z)).center())
        p1 = Vector((loc * Vertex(0, 0, carcasa.FRONT_Z - 1)).center())
        out.append((p0, (p1 - p0).normalized()))
    return out


def cable_paths(sep, ang):
    """Recorrido aproximado de cada USB (solo para las vistas): sale por la ranura de la carcasa,
    sube a la barra, pasa por los clips y baja por el extremo +X."""
    ring_z = BAR_Z + clip_cable.RING_Z
    end_x = P.PROFILE_LEN / 2
    paths = []
    for i in (0, 1):
        loc = _case_world(i, sep, ang)
        exit_ = Vector((loc * Vertex(0, P.CASE_OUTER / 2 + 3, -P.CASE_BACK_T - 5)).center())
        x0 = exit_.X
        pts = [tuple(exit_), (x0, exit_.Y + 6, BAR_Z - 22), (x0, 18, BAR_Z + 4), (x0 + 12, 0, ring_z)]
        pts += [(x, 0, ring_z) for x in range(int(x0) + 30, int(end_x) - 10, 20)]
        pts += [(end_x + 6, 0, ring_z - 4), (end_x + 14, 0, BAR_Z - 25), (end_x + 18, 0, BAR_Z - 90)]
        paths.append(pts)
    return paths


def axes_crossing(sep, ang):
    """Punto medio de la perpendicular común de los dos ejes, y su distancia (mm) a lo largo de cada eje."""
    (p, u), (q, v) = camera_axes(sep, ang)
    w = p - q
    a, b, c, d, e = u.dot(u), u.dot(v), v.dot(v), u.dot(w), v.dot(w)
    den = a * c - b * b
    if abs(den) < 1e-12:
        return None, float("inf")
    s, t = (b * e - c * d) / den, (a * e - b * d) / den
    return (p + u * s + q + v * t) * 0.5, (s + t) / 2


def _marker0():
    """Marker0: placa blanca de 100 mm con un patrón 4×4 tipo ArUco en negro (para las vistas)."""
    bits = (1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0)
    base = Location((0, 0, 0)) * Box(100, 100, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cell = 15.0
    black = Location((0, 0, 0.8)) * Box(90, 90, 0.3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for k, bit in enumerate(bits):
        if bit:
            x, y = -22.5 + (k % 4) * cell, 22.5 - (k // 4) * cell
            black -= Location((x, y, 0.8)) * Box(cell, cell, 0.3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return base, black


def _box():
    s, t = P.BOX_SIZE, P.BOX_RIM
    walls = [Location((0, 0, -t)) * Box(s + 2 * t, s + 2 * t, t, align=(Align.CENTER, Align.CENTER, Align.MIN)),
             Location((0, -s / 2 - t / 2, 0)) * Box(s + 2 * t, t, s, align=(Align.CENTER, Align.CENTER, Align.MIN))]
    for sx in (-1, 1):
        walls.append(Location((sx * WALL_X, 0, 0)) * Box(t, s, s, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return walls


def build(sep=P.PRESENTATION_CONFIG[0], ang=P.PRESENTATION_CONFIG[1], with_context=True):
    """Lista de Item colocados en el mundo."""
    bar = Location((0, 0, BAR_Z))
    items = [Item("Perfil 2020", bar * perfil_2020.build(), "aluminio")]
    pinza = pinza_caja.build()
    items.append(Item("BE-PINZA-CAJA (dcha)", Location((WALL_X, 0, BAR_Z)) * pinza, "impresa"))
    items.append(Item("BE-PINZA-CAJA (izda)", Location((-WALL_X, 0, BAR_Z)) * ROT_Z180 * pinza, "impresa"))
    parts = {"carro": carro.build(), "cuna": cuna.build(ang), "base": carcasa.build_base(), "tapa": carcasa.build_lid()}
    for i in (0, 1):
        base, cam = _camera_base(i, sep), f"cámara {i + 1}"
        items.append(Item(f"BE-CARRO ({cam})", base * parts["carro"], "impresa"))
        items.append(Item(f"BE-CUNA-{cuna.code(ang)} ({cam})", base * Location((0, 0, carro.BOTTOM_Z)) * parts["cuna"],
                          "impresa"))
        case = _case_world(i, sep, ang)
        items.append(Item(f"BE-CARCASA ({cam})", case * parts["base"], cam))
        items.append(Item(f"BE-CARCASA-TAPA ({cam})", case * parts["tapa"], cam))
    clip = clip_cable.build()
    for x in CLIP_X:
        items.append(Item(f"BE-CLIP-CABLE x={x:+.0f}", bar * Location((x, 0, 0)) * clip, "impresa"))
    if with_context:
        for k, w in enumerate(_box()):
            items.append(Item(f"Caja de luz {k + 1}", w, "caja"))
        white, black = _marker0()
        items.append(Item("Marker0 (fondo)", white, "caja"))
        items.append(Item("Marker0", black, "marker"))
    return items
