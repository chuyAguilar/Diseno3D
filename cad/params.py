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

BOARD_T = 1.6            # grosor de la placa de la cámara
LENS_BARREL_D = 14.0     # diámetro exterior del portalente M12 (cabe en el agujero de 14.6)
CAM_BEHIND_BOARD = 20.4  # fondo libre detrás de la placa (conector USB y componentes)
CABLE_SLOT = (12.0, 8.0) # salida del cable en la pared +Y: ancho × alto

SIN_MEDIR = ("CASE_REF_OUTER", "CASE_REF_DEPTH", "CASE_REF_WALL", "CASE_REF_CAVITY",
             "CAM_BOARD", "LENS_HOLE_D", "BOARD_T", "LENS_BARREL_D", "CAM_BEHIND_BOARD", "CABLE_SLOT",
             "CABLE_D")

# --- Carcasa nueva BE-CARCASA (D2). Mira hacia -Z; la cara trasera de montaje está en z = 0 ---
CASE_WALL = WALL_MIN
CASE_CAVITY = CAM_BOARD + 2 * CLEARANCE_SLIDE
CASE_OUTER = CASE_CAVITY + 2 * CASE_WALL
CASE_BACK_T = 8.0        # aloja la tuerca 1/4-20 y los pasadores; ≥ WALL_STRUCT
CASE_DEPTH = CASE_BACK_T + CAM_BEHIND_BOARD + BOARD_T   # hasta la cara frontal de la placa
CASE_FLANGE = 56.0       # brida frontal para los 4 tornillos M3 de la tapa
CASE_FLANGE_T = 4.0
CASE_SCREW_XY = 24.5     # tornillos de la tapa en (±, ±)
CASE_LID_T = 3.0
CASE_POST = 3.0          # postes que aprietan la placa contra la tapa
CASE_PIN_X = 13.0        # pasadores antigiro en (±CASE_PIN_X, 0) de la cara trasera
PIN_DEPTH = 6.0
LENS_CLEAR_D = LENS_BARREL_D + 2 * LENS_KEEPOUT

# --- Tornillos de unión ---
BOLT_14_20_LEN = 12.7
BOLT_14_20_HEAD_D = 9.5
BOLT_14_20_HEAD_H = 6.35
M3_NUT_FLATS = 5.5
M3_NUT_H = 2.4

# --- Marco de la barra: el perfil va a lo largo de X, centrado en el origen; Z hacia arriba ---
PROFILE_BOTTOM = -PROFILE_SIZE / 2

# --- Carro BE-CARRO: bajo el perfil, con llave en la ranura inferior y 2 M5 a tuercas en T ---
CARRO_SIZE = CASE_OUTER          # mismo apoyo que la cuña
CARRO_T = 10.0
KEY_H = 1.5                      # altura de la llave; menor que SLOT_LIP
CARRO_M5_X = 12.0                # M5 en (±CARRO_M5_X, 0)
M5_HEAD_D = 8.5
M5_HEAD_H = 5.0

# --- Pinza BE-PINZA-CAJA: muerde el borde superior de una pared lateral y sostiene el perfil ---
PINZA_LEN = 30.0                 # a lo largo de la barra
PINZA_CRADLE_WALL = 4.0
PINZA_FLOOR = 5.0                # entre el borde de la caja y el perfil
PINZA_JAW = 5.0
PINZA_JAW_DEPTH = 25.0           # cuánto baja por la pared
PINZA_CRADLE_UP = 6.0            # cuánto sube la cuna por los lados del perfil (desde su centro)

# --- Clip de cable BE-CLIP-CABLE: cierre de cuarto de vuelta en la ranura superior ---
CABLE_D = 4.5                    # SIN_MEDIR: diámetro del cable USB
CLIP_TAB_L = 10.5                # entre SLOT_OPENING y SLOT_CHAMBER_W
CLIP_TAB_T = 1.5
CLIP_RING_WALL = 1.6

# --- Cuña BE-CUNA (D3, D4). Cara superior en z = 0 contra el carro; la inferior, inclinada, contra la carcasa ---
WEDGE_T0 = 11.0          # grosor en el canto fino: cabe la cabeza del 1/4-20 a 0°
WEDGE_SEAT = 4.0         # material bajo la cabeza del tornillo
WEDGE_M3_Y = 15.0        # tornillos M3 al carro en (0, ±WEDGE_M3_Y)

# --- Probeta de tolerancias (B7) ---
PROBE_CLEARANCES = (0.0, 0.1, 0.2, 0.3, 0.4)
