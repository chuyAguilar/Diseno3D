"""BE-CLIP-CABLE: sujeta el USB a la barra para que un tirón no llegue a la cámara (R6).

Marco de la barra; se monta en la ranura superior (cara z = +PROFILE_SIZE/2). Cierre de
cuarto de vuelta: la pestaña entra a lo largo de la ranura y, girada 90°, queda bajo los
labios. Se modela ya girada. Encima, un anillo abierto donde entra el cable a presión.
"""
from build123d import Align, BuildPart, Box, Cylinder, Locations, Mode

from cad import params as P

TOP = P.PROFILE_SIZE / 2
LIP_BOTTOM = TOP - P.SLOT_LIP
NECK_D = P.SLOT_OPENING - P.CLEARANCE_SLIDE
HEAD = (12.0, 12.0, 2.0)
RING_IN = P.CABLE_D + P.CLEARANCE_SLIDE
RING_OUT = RING_IN + 2 * P.CLIP_RING_WALL
RING_Z = TOP + HEAD[2] + RING_OUT / 2 - 0.5


def build():
    with BuildPart() as part:
        tab_top = LIP_BOTTOM - P.CLEARANCE_SLIDE
        with Locations((0, 0, tab_top)):
            Box(NECK_D, P.CLIP_TAB_L, P.CLIP_TAB_T, align=(Align.CENTER, Align.CENTER, Align.MAX))
            Cylinder(NECK_D / 2, TOP - tab_top, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, TOP)):
            Box(*HEAD, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, RING_Z)):
            Cylinder(RING_OUT / 2, HEAD[0], rotation=(0, 90, 0))
            Cylinder(RING_IN / 2, HEAD[0], rotation=(0, 90, 0), mode=Mode.SUBTRACT)
        with Locations((0, 0, RING_Z + RING_OUT / 2)):
            Box(HEAD[0], P.CABLE_D * 0.75, RING_OUT / 2, mode=Mode.SUBTRACT)
    part.part.label = "BE-CLIP-CABLE-v01"
    return part.part
