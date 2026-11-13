"""Concepto v02: barra en el borde superior de la abertura, con inclinación indexada.

Solo para renders e idea (spec 004). Los valores que comparte con la v01 se leen de
cad/params.py (P4); aquí solo viven los nuevos. Todo es parámetro: se cambia aquí y se
vuelve a correr `python -m concepto.abertura.render`.
"""
from cad.params import ANGLE_SET, BOX_RIM, BOX_SIZE, CLEARANCE_SLIDE, M5_D, PROFILE_SIZE  # noqa: F401

# --- Configuración que se dibuja ---
SEP = 250.0                       # marcas de los carros (entre centros de carro)
CONV = 15.0                       # cuña de convergencia por cámara (una de ANGLE_SET)
PITCH = 45.0                      # inclinación hacia el fondo; 0 = cámaras en vertical

# --- Rangos que el diseño admite ---
SEP_RANGE = (100.0, 300.0)
SEP_STEP = 25.0
PITCH_RANGE = (0.0, 60.0)
PITCH_STEP = 5.0                  # un agujero de índice cada 5°
PITCH_COMPARE = (30.0, 45.0, 60.0)

# --- Barra ---
BAR_LEN = 350.0                   # cabe entre las paredes con el pivote y la pinza en cada extremo

# --- Borde de la abertura: canto frontal del techo de la caja ---
EDGE_T = BOX_RIM                  # SIN_MEDIR: grosor del techo en el canto
PIVOT_BELOW = 45.0                # eje del perfil bajo la cara inferior del techo
PIVOT_IN = 30.0                   # eje del perfil detrás del canto, hacia el fondo

# --- Pinza con pivote BE-PINZA-PIVOTE ---
HUB_T = 6.0                       # cubo atornillado al extremo del perfil (M5 al agujero central)
HUB_D = 50.0
BOSS_D = 12.0                     # eje del pivote, pasa por la placa
PLATE_T = 6.0                     # placa del pivote
PLATE_D = 58.0
INDEX_R = 21.0                    # radio de los agujeros de índice
INDEX_D = 3.2                     # pasador Ø3
KNOB_D = 20.0                     # perilla de apriete, por fuera
KNOB_T = 5.0
JAW_T = 6.0                       # mordazas arriba y abajo del techo
JAW_IN = 40.0                     # cuánto entran bajo el techo
SPINE_T = 6.0                     # lomo por delante del canto
CLAMP_W = 18.0                    # ancho de la pinza a lo largo de X

# --- Regleta (spec 002, en concepto) ---
REGLETA_T = 6.0
NOTCH_W = 3.0
NOTCH_D = 2.5

# --- Escena ---
TARGET_Y = 130.0                  # dónde se dibuja Marker0 en el suelo (solo ilustración)
