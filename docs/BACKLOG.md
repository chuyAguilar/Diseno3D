# BACKLOG

Lo que falta. Prioridad **alta**: puede dar un resultado equivocado o impide avanzar. **Media**: mejora clara sin riesgo. **Baja**: espera datos o solo si estorba. Lo cerrado pasa a «Cerrados» con la fecha y qué lo cerró.

## Índice

| Id | Qué | Prioridad |
| --- | --- | --- |
| B3 | FOV de 85°: ¿diagonal u horizontal? | Media |
| B4 | Medir la carcasa real y la salida del cable USB | Media |
| B5 | Formato del archivo de configuración por código | Baja |
| B6 | Índice de cada cámara en el software de navegación | Alta |
| B7 | Probeta de tolerancias en la Bambu Lab con PLA | Alta |
| B8 | Comprar los materiales de `docs/COMPRAS.md` | Alta |
| B9 | Regleta con muescas: fijar la separación por forma, no por apriete (P7) | Alta |

## Abiertos

### B3 · FOV de 85°: ¿diagonal u horizontal?

- **Qué:** la ficha de la SVPRO dice «FOV 85°» sin decir sobre qué eje.
- **Por qué queda:** el ángulo de las cuñas y el cruce de campos a 35–40 cm dependen de ello.
- **De dónde:** entrevista, fase 1.
- **Qué haría falta:** medirlo con la cámara (regla a distancia conocida) o con la calibración intrínseca de PoyectoNavegacion.
- **Prioridad:** media.

### B4 · Medir la carcasa real y la salida del cable USB

- **Qué:** la carcasa de referencia (`recursos/38mm Board Mount…`) mide 42.16 × 42.16 mm; falta confirmar con calibre la impresa, el lado por donde sale el cable y su diámetro.
- **Por qué queda:** el modelo de Thingiverse puede no coincidir con lo impreso.
- **De dónde:** entrevista, fase 1.
- **Qué haría falta:** calibre sobre la pieza real.
- **Prioridad:** media.

### B5 · Formato del archivo de configuración por código

- **Qué:** qué guarda el archivo nombrado por el código de configuración (p. ej. `S150-A05`) y en qué formato lo lee el software de navegación.
- **Por qué queda:** el autor no sabe aún cómo lo usará el software; «prepararse para todo».
- **De dónde:** entrevista, fase 1.
- **Qué haría falta:** decidirlo cuando el software lo necesite.
- **Prioridad:** baja.

### B6 · Índice de cada cámara en el software de navegación

- **Qué:** averiguar con qué índice abre el software cada cámara física y marcar «1» y «2» en las carcasas.
- **Por qué queda:** el autor decidió que la numeración la manda el software (entrevista, fase 2).
- **De dónde:** entrevista, fase 2, 2026-10-29.
- **Qué haría falta:** revisar PoyectoNavegacion o abrir las cámaras y anotar cuál es cuál; si el índice cambia al reconectar USB, buscar un identificador estable (número de serie o puerto).
- **Prioridad:** alta — intercambiar las cámaras invalida la calibración estéreo.

### B7 · Probeta de tolerancias en la Bambu Lab con PLA

- **Qué:** imprimir una pieza de prueba con agujeros, pasadores, ranura deslizante y alojamiento de tuerca 1/4-20 para fijar `clearance_slide`, `clearance_press` y `hole_comp`.
- **Por qué queda:** los valores de `docs/CONTEXT.md` son iniciales (P3).
- **De dónde:** entrevista, fase 2, 2026-10-29.
- **Qué haría falta:** B1 resuelto; medir con calibre.
- **Prioridad:** alta — antes de la primera pieza funcional.

### B8 · Comprar los materiales

- **Qué:** lo que lista `docs/COMPRAS.md` (perfil 2020, tuercas en T M5, tornillería, pasadores, PETG…). Se pide capital a la empresa mostrando el diseño de la barra.
- **Por qué queda:** el autor no los tiene.
- **De dónde:** entrevista, fase 3, 2026-10-29.
- **Qué haría falta:** confirmar la longitud exacta cuando esté diseñada la pinza de borde.
- **Prioridad:** alta — la estructura depende de él.

### B9 · Regleta con muescas para la separación

- **Qué:** una regleta impresa (en dos tramos, por la cama de 256 mm) fija en una ranura lateral del perfil, con muescas cada 25 mm, y un diente en el carro que entra en la muesca.
- **Por qué queda:** en la v01 el carro se sujeta al perfil solo con 2 M5 a tuercas en T, es decir, por apriete; con golpes de transporte podría deslizarse, y eso choca con P7. Hoy solo hay un índice en V para leer la marca.
- **De dónde:** spec 001, fase 3, 2026-10-29.
- **Qué haría falta:** decidir qué ranura lateral queda libre (la -Y la usa la pinza en sus extremos) y añadir el diente al carro.
- **Prioridad:** alta — sin ella, la separación no es repetible tras un golpe.

## Cerrados

### B2 · Definir la comprobación de «no cambió»

- **Cerrado el 2026-10-29:** `pytest` sobre `tests/`, que mide en el modelo las cotas de interfaz (no repite los parámetros). Spec 001, fase 1.

### B1 · Elegir la herramienta CAD

- **Cerrado el 2026-10-29:** build123d (Python), decidido por el autor en la fase 3 de la entrevista (`docs/CONTEXT.md`, E4).
