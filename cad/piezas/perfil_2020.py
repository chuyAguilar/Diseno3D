"""Perfil de aluminio 2020 de referencia (no se imprime): sección en YZ, largo en X."""
from build123d import BuildPart, BuildSketch, Circle, Locations, Mode, Plane, Rectangle, extrude

from cad import params as P


def build(length: float = P.PROFILE_LEN):
    s = P.PROFILE_SIZE / 2
    lip_c = s - P.SLOT_LIP / 2
    chamber_h = P.SLOT_DEPTH - P.SLOT_LIP
    chamber_c = s - P.SLOT_LIP - chamber_h / 2
    with BuildPart() as part:
        with BuildSketch(Plane.YZ.offset(-length / 2)):
            Rectangle(P.PROFILE_SIZE, P.PROFILE_SIZE)
            for sign in (1, -1):
                with Locations((0, sign * lip_c)):
                    Rectangle(P.SLOT_OPENING, P.SLOT_LIP, mode=Mode.SUBTRACT)
                with Locations((0, sign * chamber_c)):
                    Rectangle(P.SLOT_CHAMBER_W, chamber_h, mode=Mode.SUBTRACT)
                with Locations((sign * lip_c, 0)):
                    Rectangle(P.SLOT_LIP, P.SLOT_OPENING, mode=Mode.SUBTRACT)
                with Locations((sign * chamber_c, 0)):
                    Rectangle(chamber_h, P.SLOT_CHAMBER_W, mode=Mode.SUBTRACT)
            Circle(P.PROFILE_BORE / 2, mode=Mode.SUBTRACT)
        extrude(amount=length)
    return part.part
