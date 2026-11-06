"""Separador de cama de la Ender 3 V3: la única fuente de sus medidas (P4).

Medidas del original con calibre digital, en `fotos/` (spec 003).
"""
from cad.params import HOLE_COMP

# --- Original, medido (fotos/) ---
ORIG_LEN = 15.7          # largo.jpeg
OUTER_D = 7.8            # ancho.jpeg
BORE_MEASURED = 4.5      # tamaño interior.jpeg (puntas de interiores)

# --- Piezas nuevas ---
BORE_D = BORE_MEASURED + HOLE_COMP   # el agujero impreso sale más cerrado (clarify P4)
SHORTEN = (0.7, 1.0)                 # cuánto más cortas que el original
LENGTHS = tuple(round(ORIG_LEN - s, 2) for s in SHORTEN)   # 15.0, 14.7

CHAMFER = 0.3            # canto exterior de abajo, contra la pata de elefante
MARK_W = 0.6             # ancho de cada ranura de identificación
MARK_D = 0.3             # profundidad de la ranura
MARK_PITCH = 2.0         # entre ranuras
LAYER_H = 0.1            # altura de capa para que 14.7 salga exacto (se elige en Bambu Studio)
