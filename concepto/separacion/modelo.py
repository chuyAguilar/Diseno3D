"""Mecanismo de separación en detalle (concepto, para imágenes): regleta con muescas en V,
carro con brazo y diente, y la tornillería de una estación de cámara.

Marco local de la barra: perfil a lo largo de X con el eje en el origen, Z hacia arriba, el
carro debajo (cara superior en z = -10). La regleta va en la cara +Y del perfil.
Las cabezas de los M3 carro–cuña asoman sobre el carro en y = ±WEDGE_M3_Y: por eso la regleta
empieza REGLETA_Z0 por encima de la cara inferior del perfil y el brazo va desplazado ARM_DX
hacia el centro de la barra (fuera de esa cabeza).
"""
from build123d import (Align, Box, BuildLine, BuildPart, BuildSketch, Cylinder, Location, Polyline, extrude,
                       make_face, Plane)

from cad import ensamble
from cad import params as CP
from cad.piezas import carro, perfil_2020

H = CP.PROFILE_SIZE / 2
REG_Y0 = H                        # cara del perfil
REG_T = 6.0
REG_Y1 = REG_Y0 + REG_T           # cara exterior de la regleta (la de las muescas)
REGLETA_Z0 = -H + 4.0             # por encima de las cabezas M3 (3 mm) + 1 mm
REGLETA_HALF = 170.0
NOTCH_D = 2.5                     # V de 90°: ancho = 2 × profundidad
SEPS = tuple(100.0 + 25.0 * k for k in range(9))       # 100 … 300
ARM_DX = 14.0                     # brazo desplazado hacia el centro de la barra
ARM_W = 10.0
ARM_GAP = 0.2                     # entre el brazo y la regleta
TOOTH_H = 5.0                     # altura del diente: lo que hay que bajar el carro, + 1 mm
TOOTH_PLAY = 0.15                 # por flanco
REG_SCREW_X = 25.0                # M5 de la regleta en ±25: zona central, los carros nunca llegan
# Carro v02: en la v01 la cuña tapa las cabezas de los M5 del carro (no se pueden aflojar sin
# desmontar cuña y cámara). El v02 es más largo y lleva los M5 fuera de la huella de la cuña.
CARRO2_LEN = 90.0                 # 2 × CARRO2_M5_X + 10
CARRO2_M5_X = 40.0                # llave recta libre de cuña y carcasa con las 7 cuñas (medido)


def notch_x(sep, side):
    """x de la muesca de la separación `sep` para la cámara del lado `side` (-1 izda, +1 dcha)."""
    return side * (sep / 2 - ARM_DX)


def _vprism(x, y_face, depth, half_w, z0, z1, inward):
    """Prisma triangular vertical: base en y = y_face, punta hacia -Y (inward=-1) o +Y."""
    with BuildPart() as p:
        with BuildSketch(Plane.XY.offset(z0)):
            with BuildLine():
                Polyline((x - half_w, y_face), (x + half_w, y_face), (x, y_face + inward * depth), close=True)
            make_face()
        extrude(amount=z1 - z0)
    return p.part


def regleta():
    r = Location((0, REG_Y0, REGLETA_Z0)) * Box(2 * REGLETA_HALF, REG_T, H - REGLETA_Z0,
                                                 align=(Align.CENTER, Align.MIN, Align.MIN))
    for s in SEPS:
        for side in (-1, 1):
            r -= _vprism(notch_x(s, side), REG_Y1 + 0.01, NOTCH_D + 0.01, NOTCH_D, REGLETA_Z0 - 1, H + 1, -1)
    for sx in (-1, 1):
        r -= Location((sx * REG_SCREW_X, REG_Y0, 0)) * Cylinder(2.7, REG_T, rotation=(-90, 0, 0),
                                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    r -= Location((0, REG_Y0, 0)) * Cylinder(1.0, REG_T, rotation=(-90, 0, 0),
                                             align=(Align.CENTER, Align.CENTER, Align.MIN))   # referencia x = 0
    return r


def carro_v02(xc):
    """Cuerpo del carro v02 centrado en xc (sin el brazo): llave en la ranura inferior, 2 M5 en
    ±CARRO2_M5_X con la cabeza por debajo, y los 2 M3 de la cuña como en la v01."""
    from build123d import Mode
    w = CP.CARRO_SIZE
    body = Location((xc, 0, carro.TOP_Z)) * Box(CARRO2_LEN, w, CP.CARRO_T, align=(Align.CENTER, Align.CENTER, Align.MAX))
    body += Location((xc, 0, carro.TOP_Z)) * Box(CARRO2_LEN, CP.SLOT_OPENING - CP.CLEARANCE_SLIDE, CP.KEY_H,
                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    for x in (xc - CARRO2_M5_X, xc + CARRO2_M5_X):
        body -= Location((x, 0, carro.BOTTOM_Z)) * Cylinder((CP.M5_D + CP.HOLE_COMP + CP.CLEARANCE_SLIDE) / 2,
                                                             CP.CARRO_T + CP.KEY_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        body -= Location((x, 0, carro.BOTTOM_Z)) * Cylinder((CP.M5_HEAD_D + 2 * CP.CLEARANCE_SLIDE + 1.0) / 2,
                                                             CP.M5_HEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for y in (-CP.WEDGE_M3_Y, CP.WEDGE_M3_Y):
        body -= Location((xc, y, carro.BOTTOM_Z)) * Cylinder((CP.M3_D + CP.HOLE_COMP + CP.CLEARANCE_SLIDE) / 2,
                                                              CP.CARRO_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return body


def brazo(xc, side):
    """Brazo con diente que se añade al carro (BE-CARRO-v02) centrado en xc; side = lado de la cámara."""
    xa = xc - side * ARM_DX
    y0 = REG_Y1 + ARM_GAP
    arm = Location((xa, y0, carro.BOTTOM_Z)) * Box(ARM_W, 22.0 - y0 + 6, REGLETA_Z0 + TOOTH_H - carro.BOTTOM_Z,
                                                  align=(Align.CENTER, Align.MIN, Align.MIN))
    tooth = _vprism(xa, y0 + 0.01, NOTCH_D + ARM_GAP - 0.4, NOTCH_D - TOOTH_PLAY, REGLETA_Z0,
                    REGLETA_Z0 + TOOTH_H, -1)
    return arm + tooth


def tornillos(xc, ang):
    """Cabezas y cañas de la tornillería de la estación (geometría simplificada para la imagen)."""
    out = []
    bz, tz = carro.BOTTOM_Z, carro.TOP_Z
    for x in (xc - CARRO2_M5_X, xc + CARRO2_M5_X):               # M5×10 DIN 912 desde abajo, fuera de la cuña
        out.append(("M5×10 DIN 912 (carro)", Location((x, 0, bz)) * Cylinder(CP.M5_HEAD_D / 2, CP.M5_HEAD_H,
                                                                              align=(Align.CENTER, Align.CENTER, Align.MIN))))
        out.append(("", Location((x, 0, bz + CP.M5_HEAD_H)) * Cylinder(CP.M5_D / 2, 10.0 - 0.01,
                                                                         align=(Align.CENTER, Align.CENTER, Align.MIN))))
    for y in (-CP.WEDGE_M3_Y, CP.WEDGE_M3_Y):                     # M3 carro–cuña, cabeza arriba
        out.append(("M3 DIN 912 (carro–cuña)", Location((xc, y, tz)) * Cylinder(2.75, 3.0,
                                                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))))
    return out


def tornillos_regleta():
    out = []
    for sx in (-1, 1):                                            # M5×10 ISO 7380 (botón)
        out.append(Location((sx * REG_SCREW_X, REG_Y1, 0)) * Cylinder(4.75, 2.75, rotation=(-90, 0, 0),
                                                                       align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return out


def estacion(sep, ang, side=-1, drop=0.0, x_override=None):
    """Piezas de una cámara (carro + brazo, cuña, carcasa y tornillos) en el marco local.
    `drop` baja el carro; `x_override` lo coloca en otra x (para dibujar el deslizamiento)."""
    items = ensamble.build(sep, ang, with_context=False)
    cam = "cámara 1" if side < 0 else "cámara 2"
    keep = [it for it in items if it.name.endswith(f"({cam})")]
    xc = side * sep / 2
    dx = 0.0 if x_override is None else x_override - xc
    move = Location((dx, 0, -drop)) * Location((0, 0, -ensamble.BAR_Z))
    parts = [(it.name, move * it.part, it.role) for it in keep if not it.name.startswith("BE-CARRO")]
    shift = Location((dx, 0, -drop))
    parts.append(("BE-CARRO-v02", shift * carro_v02(xc), "impresa"))
    parts.append(("Brazo con diente (BE-CARRO-v02)", shift * brazo(xc, side), "diente"))
    parts += [(n, shift * s, "tornillo") for n, s in tornillos(xc, ang)]
    return parts


def fijo(length=420.0):
    """Perfil (un tramo) y regleta con sus tornillos: lo que no se mueve."""
    out = [("Perfil 2020", perfil_2020.build(length), "aluminio"), ("BE-REGLETA", regleta(), "regleta")]
    out += [("M5×10 ISO 7380 (regleta)", s, "tornillo") for s in tornillos_regleta()]
    return out
