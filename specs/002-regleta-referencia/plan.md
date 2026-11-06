# Plan — Meta 002

## Lo leído

`specs/002-regleta-referencia/spec.md`, `docs/CONTEXT.md` (§0 V2 y V8, §2 y §3), `docs/BACKLOG.md` (B9, B10), `cad/params.py`, `cad/piezas/{carro,pinza_caja,clip_cable,perfil_2020}.py`, `cad/ensamble.py`, `cad/exportar.py`, `tests/test_sujecion.py`. HEAD: commit 9.

## Ranura y sujeción

Hoy se usan tres ranuras del perfil: la inferior (−Z) para el carro, la −Y para el M5 de las pinzas en los extremos y la superior (+Z) para los clips. **La +Y está libre**, y ahí va la regleta.

**La regleta es una sola pieza** que lleva todas las muescas: la separación entre las dos cámaras la da su forma, no dónde quede la regleta sobre el perfil. Se sujeta con 2 M5 a tuercas en T. Si con un golpe resbalara, las dos cámaras se moverían juntas: la línea base no cambia, solo la posición de la barra, y eso lo detecta el punto de referencia.

Medidas:
- Largo: muescas hasta ±100 mm + la mitad del carro + los extremos para los M5 → ≈ 240 mm. Cabe en la cama de 256 mm de una pieza (B9 hablaba de dos tramos; no hace falta).
- Pinzas en x = ±187…217: no tocan la regleta, que llega hasta ±120.
- Clips en la ranura superior: no tocan la regleta.

## Diente y muesca

- **Muesca:** ranura vertical en V de 90° en la cara exterior (+Y) de la regleta, abierta por abajo. El carro sube contra el perfil y su diente entra en ella al montarlo, sin desmontar nada más.
- **Diente:** el carro crece por su lado +Y hasta la regleta, con un nervio en V que mira a −Y.
- **Holgura:** el diente se dimensiona para que el juego a lo largo de X sea **0.20 mm en total** (`TOOTH_PLAY_X`), dentro del tope de 0.3 mm de V2, y se mide sobre el modelo. Poner `CLEARANCE_SLIDE` en cada flanco de una V de 90° daría ≈ 0.85 mm de juego, demasiado.

## Punto de referencia

En x = 0, en la cara superior de la regleta: una muesca en V vertical, un agujero Ø 2 pasante para enganchar el gancho del metro y «0» grabado. El metro mide desde ahí la altura sobre Marker0 y la distancia a las paredes de la caja.

## Archivos

| Archivo | Qué cambia |
| --- | --- |
| `cad/params.py` | Parámetros nuevos de la regleta, el diente y la referencia |
| `cad/piezas/regleta.py` | **Nuevo.** `build() -> Part` (`BE-REGLETA-v01`); `notch_x() -> tuple[float, ...]` |
| `cad/piezas/carro.py` | Brazo y diente en +Y; la etiqueta pasa a `BE-CARRO-v02` |
| `cad/ensamble.py` | Coloca la regleta; `reference_point() -> Vector` |
| `cad/exportar.py` | Exporta la regleta; añade la referencia a `datos.txt` y una vista `detalle-regleta`; escribe en `salidas/v02/<código>/` para no pisar la presentación v01 (P3 de `clarify.md`) |
| `tests/test_regleta.py` | **Nuevo.** Muescas, juego, cama, referencia |
| `tests/test_ensamble.py` | Interferencia para todas las separaciones; la óptica, igual que en la v01 |
| `docs/CONTEXT.md` | V2 y V8 con el número medido |
| `docs/COMPRAS.md` | +2 tuercas en T M5 y 2 tornillos (caben en las 20 de la lista; se comprueba) |

## Piezas y parámetros

Nuevos en `cad/params.py`:

| Nombre | Valor | Qué es |
| --- | --- | --- |
| `NOTCH_PITCH` | `SEP_STEP / 2` = 12.5 mm | Paso de muescas por lado (P1) |
| `REGLETA_LEN` | ≈ 240 mm | Largo de la regleta |
| `REGLETA_T` | 6.0 mm | Grosor fuera del perfil (≥ `WALL_STRUCT`) |
| `REGLETA_H` | 20.0 mm | Alto: el de la cara del perfil |
| `NOTCH_ANGLE` | 90° | Ángulo de la V |
| `NOTCH_DEPTH` | 2.5 mm | Profundidad de la muesca |
| `TOOTH_PLAY_X` | 0.20 mm | Juego total del diente a lo largo de X |
| `REF_HOLE_D` | 2.0 mm | Agujero del punto de referencia |

Usa también `SEP_SET`, `SLOT_OPENING`, `CLEARANCE_SLIDE`, `M5_D` y `HOLE_COMP`.

## Fases

1. **Regleta y punto de referencia.**
   - *Entrega:* `regleta.py`, sus parámetros y `tests/test_regleta.py`.
   - *Criterio:*
     - El centro de cada muesca está en ±`sep`/2 ± 0.01 mm para todas las separaciones.
     - La llave entra en la ranura con `CLEARANCE_SLIDE` (± 0.01 mm).
     - 0 mm³ de interferencia con el perfil.
     - Cabe en la cama.
     - La referencia está en x = 0 ± 0.01 mm.
     - Cada muesca lleva su número grabado.
2. **Carro con diente, ensamble y exportación.**
   - *Entrega:* el carro con diente, el ensamble, la exportación y las pruebas.
   - *Criterio:*
     - El juego del diente a lo largo de X, medido sobre el modelo, es ≤ 0.30 mm (objetivo 0.20).
     - 0 mm³ de interferencia en el ensamble para todas las separaciones con A12.5.
     - Los centros de lente y el cruce de `S150-A12.5` son iguales a la v01 ± 0.01 mm.
     - La suite pasa.
     - `cad.exportar` genera `datos.txt` con la referencia y la vista `detalle-regleta`.

## Lo que va al BACKLOG

- **Alta:** imprimir la regleta y un carro y medir V2 en físico (± 0.3 mm tras desmontar y montar). Necesita el perfil (B8).
- **Baja:** muescas intermedias si se quiere una separación fuera de `SEP_SET`.

## ADR que se proponen

- **ADR-003:** la separación la fija una regleta de una sola pieza; si resbala, las dos cámaras se mueven juntas. Se escribe en la etapa 2 del método.

## Preguntas abiertas

En `clarify.md`: P1–P3, respondidas el 2026-10-29 (las tres, opción recomendada).

## Títulos de commit

1. `Modela la regleta de separación con el punto de referencia`
2. `Añade el diente al carro y monta la regleta en el ensamble`
