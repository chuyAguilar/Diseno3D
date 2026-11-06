# Pruebas — bitácora de mediciones

Lo que se midió, contra qué criterio y con qué resultado (P3). Una fila por medición; se añade al cerrar cada fase, con el número que quedó en el `tasks.md` del spec. Los valores de diseño no se copian aquí: viven en los `params.py` y se leen en `docs/PARAMETROS.md` (P4).

**Método:** *Modelo* = medido por `pytest` o por el exportador sobre el CAD. *Física* = medido sobre la pieza impresa o el montaje, con el instrumento que se indique. *Visual* = revisado por el autor en el visor o en las vistas; no cierra un requisito por sí solo.

## Hechas

| Fecha | Spec · fase | Qué | Criterio | Obtenido | Método | ¿Pasa? |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-29 | 001 · 1 | Suite | todas pasan | 8/8 en 6.3 s | Modelo | Sí |
| 2026-10-29 | 001 · 1 | Probeta de holguras (B7): 5 holguras 0.0–0.4 en pasador, tuerca 1/4-20, llave y muesca | nominal ± 0.01 mm | ± 0.01 mm; probeta 90 × 84 × 9.5 mm | Modelo | Sí |
| 2026-10-29 | 001 · 2 | Cavidad de la carcasa | `CAM_BOARD + 2·CLEARANCE_SLIDE` | 38.60 mm | Modelo | Sí |
| 2026-10-29 | 001 · 2 | Invasión de la holgura del portalente (V5, P5) | 0 mm³ | 0 mm³; agujero Ø 17.00 mm | Modelo | Sí |
| 2026-10-29 | 001 · 2 | Ángulo de las 7 cuñas, 0–15° (V3) | nominal ± 0.01° | ± 0.01° en las 7 | Modelo | Sí |
| 2026-10-29 | 001 · 2 | Placa trasera de la carcasa | ≥ `WALL_STRUCT` | 8.0 mm | Modelo | Sí |
| 2026-10-29 | 001 · 3 | Llave del carro | `SLOT_OPENING − CLEARANCE_SLIDE` | 5.90 mm | Modelo | Sí |
| 2026-10-29 | 001 · 3 | Boca de la pinza (V6) | `BOX_RIM + CLEARANCE_SLIDE` | 4.80 mm | Modelo | Sí |
| 2026-10-29 | 001 · 3 | Cuna de la pinza; anillo del clip | perfil + holgura; cable + holgura | 20.30 mm; 4.80 mm | Modelo | Sí |
| 2026-10-29 | 001 · 3 | Interferencia carro, pinza y clip con el perfil | 0 mm³ | 0 mm³ en las 3 | Modelo | Sí |
| 2026-10-29 | 001 · 4 | Interferencia entre todos los pares del ensamble y con las paredes (V9) | 0 mm³ | 0 mm³; 41/41 pruebas en 21.6 s | Modelo | Sí |
| 2026-10-29 | 001 · 4 | Inclinación de cada eje óptico (S150-A12.5) | 12.50° | 12.50° | Modelo | Sí |
| 2026-10-29 | 001 · 4 | Cruce de ejes a lo largo del eje | (137.0/2)/sin 12.5° ± 1 mm | 316.5 mm | Modelo | Sí |
| 2026-10-29 | 001 · 4 | Cruce de ejes respecto a Marker0 (V4) | 350–400 mm de los lentes, o anotado | 309 mm bajo los lentes, 41 mm sobre Marker0 | Modelo | Anotado |
| 2026-11-03 | 003 · 1 | Largo de los separadores en el modelo | 15.00 y 14.70 ± 0.01 mm | 15.00 y 14.70 mm | Modelo | Sí |
| 2026-11-03 | 003 · 1 | Ø exterior y agujero; ranuras | 7.80 y 4.70 ± 0.01 mm; 1 y 2 | 7.80 y 4.70 mm; 1 y 2 | Modelo | Sí |
| 2026-11-05 | 003 · impresión | Separadores montados en la Ender 3 V3 | cumplen su función | Funcionan (lo dice el autor) | Física, sin instrumento | Sí, sin número |
| 2026-11-05 | — | Visor 3D de S150-A12.5 frente a `datos.txt` | mismas cotas | 137.01 mm entre lentes; cruce 41.0 mm sobre Marker0 | Modelo | Sí |

## Pendientes

| Qué | Criterio | Método | De dónde |
| --- | --- | --- | --- |
| Largo impreso de SEP-ENDER3-L15.0 y L14.7 | ± 0.1 mm del modelo | Física, calibre | spec 003 |
| Revisión de `salidas/S150-A12.5/` (STEP, 3MF, PNG, visor) | el autor la da por buena | Visual | spec 001 · 4 |
| Probeta impresa: qué holgura entra en cada encaje (V10) | anotar la holgura que funciona por encaje | Física, calibre y prueba de encaje | B7 |
| Medidas de la cámara y la carcasa marcadas SIN MEDIR | sustituir el valor de referencia por el medido | Física, calibre | B4 |
| Ángulo de las cuñas impresas (V3) | por definir (V3 no fija tolerancia física) | Física, transportador digital o calibre | spec 001 |
| Repetibilidad de la separación (V2) | ± 0.3 mm tras desmontar y volver a montar | Física, calibre | B9, spec 002 |
| Rigidez cámara–cámara (V1) | Δ ángulo < 0.05°; Δrot < 0.05°, Δtras < 0.3 mm | Física, pose de Marker0 y calibración estéreo | B8 |
| Tirón del cable (V7) | V1 se cumple tras tirar del USB | Física | B8 |
