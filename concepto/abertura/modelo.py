"""Ensamble de concepto: caja cerrada con el frente abierto (-Y), barra colgada del canto
superior de la abertura y girada `pitch` grados sobre su propio eje.

Mundo: suelo en z = 0, centro de la caja en x = y = 0, abertura en y = -BOX_SIZE/2, fondo en +Y.
La barra, los carros, las cuñas y las carcasas son las piezas v01 (cad/), solo recolocadas.
"""
import math

from build123d import (Align, Box, Cylinder, Location, Plane, Vector, Vertex)

from cad import ensamble
from cad.ensamble import Item
from cad.piezas import clip_cable, perfil_2020
from concepto.abertura import params as P

S = P.BOX_SIZE
AXIS_Y = -S / 2 + P.PIVOT_IN
AXIS_Z = S - P.PIVOT_BELOW
END_X = P.BAR_LEN / 2


def bar_transform(pitch):
    """Del marco de cad.ensamble (perfil en z = BAR_Z) al mundo de la caja, girado `pitch`."""
    return (Location((0, AXIS_Y, AXIS_Z)) * Location((0, 0, 0), (1, 0, 0), pitch)
            * Location((0, 0, -ensamble.BAR_Z)))


def _y(a, b, z0, z1, x0, x1):
    """Caja alineada a ejes, por sus límites."""
    return Location(((x0 + x1) / 2, (a + b) / 2, z0)) * Box(x1 - x0, b - a, z1 - z0,
                                                             align=(Align.CENTER, Align.CENTER, Align.MIN))


def pinza_pivote(pitch):
    """BE-PINZA-PIVOTE del extremo +X, en el marco local: eje del perfil = eje X, x = 0 en la
    cara del extremo, techo con su cara inferior en z = PIVOT_BELOW y su canto en y = -PIVOT_IN.
    Devuelve (placa con pinza, cubo + perilla, pasador) por separado para colorearlos."""
    x0, x1 = P.HUB_T, P.HUB_T + P.PLATE_T
    plate = Location((x0, 0, 0)) * Cylinder(P.PLATE_D / 2, P.PLATE_T, rotation=(0, 90, 0),
                                            align=(Align.CENTER, Align.CENTER, Align.MIN))
    # columna de la placa hasta la mordaza inferior
    plate += _y(-P.PIVOT_IN, -P.PIVOT_IN + 30, 0, P.PIVOT_BELOW, x0, x1)
    gap = P.EDGE_T + P.CLEARANCE_SLIDE
    cx0, cx1 = x0, x0 + P.CLAMP_W
    zb = P.PIVOT_BELOW
    plate += _y(-P.PIVOT_IN, -P.PIVOT_IN + P.JAW_IN, zb - P.JAW_T, zb, cx0, cx1)                 # mordaza inferior
    plate += _y(-P.PIVOT_IN - P.SPINE_T, -P.PIVOT_IN, zb - P.JAW_T, zb + gap + P.JAW_T, cx0, cx1)  # lomo
    plate += _y(-P.PIVOT_IN - P.SPINE_T, -P.PIVOT_IN + P.JAW_IN, zb + gap, zb + gap + P.JAW_T, cx0, cx1)  # superior
    # M5 de apriete de la mordaza y agujero del eje
    plate -= Location(((cx0 + cx1) / 2, -P.PIVOT_IN + P.JAW_IN - 12, zb - P.JAW_T)) * Cylinder(
        (P.M5_D + 0.4) / 2, gap + 2 * P.JAW_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    plate -= Location((x0, 0, 0)) * Cylinder(P.BOSS_D / 2 + 0.3, P.PLATE_T, rotation=(0, 90, 0),
                                             align=(Align.CENTER, Align.CENTER, Align.MIN))
    # agujeros de índice: uno cada PITCH_STEP en el rango; el pasador del cubo cuelga en -Z a 0°
    n = int(round((P.PITCH_RANGE[1] - P.PITCH_RANGE[0]) / P.PITCH_STEP)) + 1
    for k in range(n):
        a = math.radians(P.PITCH_RANGE[0] + k * P.PITCH_STEP)
        plate -= Location((x0, P.INDEX_R * math.sin(a), -P.INDEX_R * math.cos(a))) * Cylinder(
            P.INDEX_D / 2, P.PLATE_T, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
    # cubo (gira con el perfil): disco, eje que atraviesa la placa y perilla por fuera
    hub = Cylinder(P.HUB_D / 2, P.HUB_T, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
    hub += Cylinder(P.BOSS_D / 2, P.HUB_T + P.PLATE_T, rotation=(0, 90, 0),
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    knob = Location((x1, 0, 0)) * Cylinder(P.KNOB_D / 2, P.KNOB_T, rotation=(0, 90, 0),
                                           align=(Align.CENTER, Align.CENTER, Align.MIN))
    a = math.radians(pitch)
    pin = Location((0, P.INDEX_R * math.sin(a), -P.INDEX_R * math.cos(a))) * Cylinder(
        P.INDEX_D / 2 - 0.1, x1 + 4, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
    hub = Location((0, 0, 0), (1, 0, 0), pitch) * hub
    return plate, hub + knob, pin


def regleta():
    """Regleta de spec 002 en concepto: cara +Y del perfil, muescas en ±s/2 para cada separación."""
    half = P.SEP_RANGE[1] / 2 + 10
    y0 = P.PROFILE_SIZE / 2
    r = Location((0, y0, 0)) * Box(2 * half, P.REGLETA_T, P.PROFILE_SIZE, align=(Align.CENTER, Align.MIN, Align.CENTER))
    s = P.SEP_RANGE[0]
    while s <= P.SEP_RANGE[1] + 1e-6:
        for side in (-1, 1):
            r -= Location((side * s / 2, y0 + P.REGLETA_T - P.NOTCH_D, -P.PROFILE_SIZE / 2)) * Box(
                P.NOTCH_W, P.NOTCH_D + 1, P.PROFILE_SIZE, align=(Align.CENTER, Align.MIN, Align.MIN))
        s += P.SEP_STEP
    r -= Location((0, y0, 0)) * Cylinder(1.0, P.REGLETA_T, rotation=(-90, 0, 0),
                                         align=(Align.CENTER, Align.CENTER, Align.MIN))   # referencia x = 0
    return r


def box_walls():
    t = P.BOX_RIM
    return [("Caja suelo", _y(-S / 2, S / 2 + t, -t, 0, -S / 2 - t, S / 2 + t)),
            ("Caja fondo", _y(S / 2, S / 2 + t, 0, S, -S / 2 - t, S / 2 + t)),
            ("Caja techo", _y(-S / 2, S / 2 + t, S, S + t, -S / 2 - t, S / 2 + t)),
            ("Caja pared izda", _y(-S / 2, S / 2, 0, S, -S / 2 - t, -S / 2)),
            ("Caja pared dcha", _y(-S / 2, S / 2, 0, S, S / 2, S / 2 + t))]


def targets():
    """Marker0 y un tablero ChArUco de ilustración en el suelo."""
    white, black = ensamble._marker0()
    loc = Location((70, P.TARGET_Y, 0))
    out = [("Marker0 (fondo)", loc * white, "caja"), ("Marker0", loc * black, "marker")]
    sq, nx, ny = 25.0, 7, 5
    org = (-60 - nx * sq / 2, P.TARGET_Y - ny * sq / 2)
    board = Location((org[0] + nx * sq / 2, org[1] + ny * sq / 2, 0)) * Box(
        nx * sq + 10, ny * sq + 10, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    out.append(("Tablero (fondo)", board, "caja"))
    cells = None
    for i in range(nx):
        for j in range(ny):
            if (i + j) % 2 == 0:
                c = Location((org[0] + (i + 0.5) * sq, org[1] + (j + 0.5) * sq, 0.8)) * Box(
                    sq, sq, 0.3, align=(Align.CENTER, Align.CENTER, Align.MIN))
                cells = c if cells is None else cells + c
    out.append(("Tablero", cells, "marker"))
    return out


def camera_axes(sep, conv, pitch):
    T = bar_transform(pitch)
    out = []
    for p, u in ensamble.camera_axes(sep, conv):
        p1 = Vector((T * Vertex(*p)).center())
        p2 = Vector((T * Vertex(*(p + u))).center())
        out.append((p1, (p2 - p1).normalized()))
    return out


def crossing(axes):
    (p, u), (q, v) = axes
    w = p - q
    a, b, c, d, e = u.dot(u), u.dot(v), v.dot(v), u.dot(w), v.dot(w)
    den = a * c - b * b
    if abs(den) < 1e-12:
        return None, float("inf")
    s, t = (b * e - c * d) / den, (a * e - b * d) / den
    return (p + u * s + q + v * t) * 0.5, (s + t) / 2


def build(sep=P.SEP, conv=P.CONV, pitch=P.PITCH, context=True):
    T = bar_transform(pitch)
    bar = [it for it in ensamble.build(sep, conv, with_context=False)
           if not it.name.startswith(("Perfil", "BE-PINZA", "BE-CLIP"))]
    items = [Item(it.name, T * it.part, it.role) for it in bar]
    barframe = T * Location((0, 0, ensamble.BAR_Z))
    items.append(Item("Perfil 2020", barframe * perfil_2020.build(P.BAR_LEN), "aluminio"))
    items.append(Item("BE-REGLETA (concepto)", barframe * regleta(), "impresa"))
    clip = clip_cable.build()
    for x in (-60.0, 0.0, 60.0):
        items.append(Item(f"BE-CLIP-CABLE x={x:+.0f}", barframe * Location((x, 0, 0)) * clip, "impresa"))
    plate, hub, pin = pinza_pivote(pitch)
    for side, name in ((1, "dcha"), (-1, "izda")):
        place = Location((side * END_X, AXIS_Y, AXIS_Z))
        parts = [(f"BE-PINZA-PIVOTE ({name})", plate, "pivote"), (f"BE-CUBO-PERFIL ({name})", hub, "cubo"),
                 (f"Pasador de índice ({name})", pin, "pasador")]
        for label, shape, role in parts:
            s = shape if side > 0 else shape.mirror(Plane.YZ)
            items.append(Item(label, place * s, role))
    if context:
        items += [Item(n, w, "caja") for n, w in box_walls()]
        items += [Item(n, s, r) for n, s, r in targets()]
    return items
