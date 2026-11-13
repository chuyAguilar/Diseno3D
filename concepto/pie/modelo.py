"""Ensamble del concepto de pie: pórtico 2020 (dos patas y dos postes) que sostiene la barra con
pivote indexado delante de la abertura. Nada toca la caja: se puede mover la base completa.

Usa las piezas v01 (carro, cuña, carcasa, clips) y el pivote y la regleta del concepto de la abertura.
"""
from build123d import Location, Vector, Vertex

from cad import ensamble
from cad.ensamble import Item
from cad.piezas import clip_cable, perfil_2020
from concepto.abertura import modelo as A
from concepto.pie import params as P

S = P.BOX_SIZE
END_X = P.BAR_LEN / 2
POST_X = END_X + P.HUB_T + P.PLATE_T + P.PROFILE_SIZE / 2      # centro del poste
POST_WY = P.AXIS_Y + P.POST_Y                                   # y del poste en el mundo
FOOT_TOP = P.TABLE_Z + P.PROFILE_SIZE


def bar_transform(pitch):
    return (Location((0, P.AXIS_Y, P.AXIS_Z)) * Location((0, 0, 0), (1, 0, 0), pitch)
            * Location((0, 0, -ensamble.BAR_Z)))


def _profile(length, start, axis):
    """Perfil 2020 de `length` que arranca en `start` y va a lo largo de `axis` ('Y' o 'Z')."""
    p = perfil_2020.build(length)                        # a lo largo de X, centrado
    rot = {"Y": Location((0, 0, 0), (0, 0, 1), 90), "Z": Location((0, 0, 0), (0, 1, 0), -90)}[axis]
    mid = Vector(*start) + Vector(0, length / 2, 0) * (axis == "Y") + Vector(0, 0, length / 2) * (axis == "Z")
    return Location(tuple(mid)) * rot * p


def frame():
    """Patas, postes y escuadras de los dos lados."""
    out = []
    post_len = P.AXIS_Z + P.POST_TOP - FOOT_TOP
    for side, name in ((1, "dcha"), (-1, "izda")):
        x = side * POST_X
        out.append((f"Pata 2020 ({name})", _profile(P.FOOT_Y[1] - P.FOOT_Y[0], (x, P.FOOT_Y[0], P.TABLE_Z + 10), "Y"),
                    "aluminio"))
        out.append((f"Poste 2020 ({name})", _profile(post_len, (x, POST_WY, FOOT_TOP), "Z"), "aluminio"))
        for sy in (-1, 1):   # escuadra delante y detrás del poste
            y0 = POST_WY + sy * P.PROFILE_SIZE / 2
            leg = A._y(min(y0, y0 + sy * P.BRACKET), max(y0, y0 + sy * P.BRACKET), FOOT_TOP, FOOT_TOP + P.BRACKET_T,
                       x - 9, x + 9)
            up = A._y(min(y0, y0 + sy * P.BRACKET_T), max(y0, y0 + sy * P.BRACKET_T), FOOT_TOP, FOOT_TOP + P.BRACKET,
                      x - 9, x + 9)
            out.append((f"Escuadra ({name}, {'detrás' if sy > 0 else 'delante'})", leg + up, "impresa"))
    return out


def camera_axes(sep, conv, pitch):
    T = bar_transform(pitch)
    out = []
    for p, u in ensamble.camera_axes(sep, conv):
        p1 = Vector((T * Vertex(*p)).center())
        p2 = Vector((T * Vertex(*(p + u))).center())
        out.append((p1, (p2 - p1).normalized()))
    return out


def build(sep=P.SEP, conv=P.CONV, pitch=P.PITCH, context=True):
    T = bar_transform(pitch)
    bar = [it for it in ensamble.build(sep, conv, with_context=False)
           if not it.name.startswith(("Perfil", "BE-PINZA", "BE-CLIP"))]
    items = [Item(it.name, T * it.part, it.role) for it in bar]
    barframe = T * Location((0, 0, ensamble.BAR_Z))
    items.append(Item("Perfil 2020 (barra)", barframe * perfil_2020.build(P.BAR_LEN), "aluminio"))
    items.append(Item("BE-REGLETA (concepto)", barframe * A.regleta(), "impresa"))
    clip = clip_cable.build()
    for x in (-60.0, 0.0, 60.0):
        items.append(Item(f"BE-CLIP-CABLE x={x:+.0f}", barframe * Location((x, 0, 0)) * clip, "impresa"))
    plate, hub, pin = A.pinza_pivote(pitch, post_y=P.POST_Y)
    for side, name in ((1, "dcha"), (-1, "izda")):
        place = Location((side * END_X, P.AXIS_Y, P.AXIS_Z))
        for label, shape, role in ((f"BE-PIVOTE-POSTE ({name})", plate, "pivote"),
                                   (f"BE-CUBO-PERFIL ({name})", hub, "cubo"),
                                   (f"Pasador de índice ({name})", pin, "pasador")):
            items.append(Item(label, place * (shape if side > 0 else shape.mirror(A.Plane.YZ)), role))
    items += [Item(n, s, r) for n, s, r in frame()]
    if context:
        items += [Item(n, w, "caja") for n, w in A.box_walls()]
        items += [Item(n, s, r) for n, s, r in A.targets()]
        items.append(Item("Mesa", A._y(-520, 330, P.TABLE_Z - 6, P.TABLE_Z, -330, 330), "mesa"))
    return items
