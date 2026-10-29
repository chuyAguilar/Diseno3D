"""Parámetros maestros de la barra estéreo: la única fuente (P4).

Unidades: milímetros y grados. Cada valor dice de dónde sale. Los marcados
SIN_MEDIR vienen de la carcasa de referencia de Thingiverse y se confirman con
calibre (BACKLOG B4). Las holguras son iniciales hasta la probeta (B7).
"""

# --- Holguras y paredes (docs/CONTEXT.md, fase 2) ---
CLEARANCE_SLIDE = 0.30   # piezas que entran y salen
CLEARANCE_PRESS = 0.10   # tuercas y pasadores a presión
HOLE_COMP = 0.20         # se suma al diámetro de los agujeros verticales
WALL_STRUCT = 3.0        # pared mínima portante
WALL_MIN = 2.0           # pared mínima no portante

# --- Configuraciones (R2, R3, D3, D4) ---
SEP_STEP = 25.0
SEP_SET = (100.0, 125.0, 150.0, 175.0, 200.0)
ANGLE_STEP = 2.5                                    # por cámara
ANGLE_SET = tuple(i * ANGLE_STEP for i in range(7))  # 0.0 … 15.0
WORK_DIST = 375.0                                   # nominal; rango 350–400
PRESENTATION_CONFIG = (150.0, 12.5)                 # S150-A12.5 (clarify P3)

# --- Impresión (Bambu Lab) ---
BED = (256.0, 256.0, 256.0)

# --- Perfil de aluminio 2020, ranura de 6 mm (E3) ---
PROFILE_SIZE = 20.0
PROFILE_LEN = 440.0
SLOT_OPENING = 6.2       # ancho de la boca de la ranura
SLOT_LIP = 1.8           # grosor del labio
SLOT_CHAMBER_W = 11.0    # ancho de la cámara interior
SLOT_DEPTH = 6.1         # de la cara exterior al núcleo
PROFILE_BORE = 4.2       # agujero central

# --- Tornillería (B4 de la fase 2) ---
NUT_14_20_FLATS = 11.11  # tuerca 1/4-20, entre caras
NUT_14_20_H = 5.6
BOLT_14_20_D = 6.35
M5_D = 5.0
M3_D = 3.0
PIN_D = 3.0              # pasador de acero Ø3
PIN_LEN = 12.0

# --- Caja de luz (E1) ---
BOX_SIZE = 400.0
BOX_RIM = 4.5            # grosor del borde donde muerde la pinza

# --- Cámara y carcasa de referencia (SIN_MEDIR: Camera_Case_Snap_Base, clarify P1-P2) ---
CASE_REF_OUTER = 42.16
CASE_REF_DEPTH = 29.21
CASE_REF_WALL = 1.52
CASE_REF_CAVITY = 39.12
CAM_BOARD = 38.0
LENS_HOLE_D = 14.6       # agujero del lente en la carcasa de referencia
LENS_KEEPOUT = 1.5       # holgura radial mínima entre el lente y cualquier pieza (P5)

SIN_MEDIR = ("CASE_REF_OUTER", "CASE_REF_DEPTH", "CASE_REF_WALL", "CASE_REF_CAVITY",
             "CAM_BOARD", "LENS_HOLE_D")

# --- Probeta de tolerancias (B7) ---
PROBE_CLEARANCES = (0.0, 0.1, 0.2, 0.3, 0.4)
