"""Concepto v02-B: la misma barra con pivote indexado, sobre un pórtico de pie que no toca la caja.

Solo para renders e idea (spec 004). Reutiliza los parámetros del concepto de la abertura
(pivote, rangos, regleta) y de cad/params.py; aquí solo viven los del pórtico.
Mundo: el de la caja (suelo de la caja en z = 0, abertura en y = -BOX_SIZE/2). La mesa está en
z = -BOX_RIM, bajo el suelo de la caja.
"""
from concepto.abertura.params import (BOX_RIM, BOX_SIZE, CONV, HUB_T, PITCH_RANGE, PITCH_STEP,  # noqa: F401
                                      PLATE_T, PROFILE_SIZE, SEP)

# --- Configuración que se dibuja ---
PITCH = 35.0                       # con S225 y cuña 15° los ejes se cruzan en el suelo, a 405 mm

# --- Barra: va entre los postes, por delante de la abertura ---
BAR_LEN = 400.0                   # los postes quedan por fuera del ancho de la caja
AXIS_Y = -235.0                   # eje de la barra: 35 mm por delante de la abertura
AXIS_Z = 375.0                    # justo bajo el canto superior de la abertura (z = BOX_SIZE)
POST_Y = -45.0                    # poste por delante del eje (relativo al eje), para dejar libre la perilla

# --- Pórtico de perfil 2020 ---
TABLE_Z = -BOX_RIM                # la mesa: la caja y las patas apoyan en ella
POST_TOP = 30.0                   # el poste sube por encima del eje
FOOT_Y = (-420.0, 120.0)          # patas a lo largo de Y, por los costados de la caja
BRACKET = 28.0                    # escuadras 2020 en la unión pata–poste
BRACKET_T = 4.0
