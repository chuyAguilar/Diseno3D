# Meta 002 — Regleta de separación y punto de referencia

## Por qué

En la v01 el carro se sujeta al perfil solo por apriete (2 M5 a tuercas en T). Con un golpe de transporte la separación puede cambiar, y eso choca con P7 y deja sin cumplir V2 (`docs/CONTEXT.md` §0). Además, la barra no tiene punto de referencia (R7, V8), así que su posición en el mundo no se puede medir con el metro desde un punto conocido del modelo. Vienen de B9 (alta) y B10 (media) del BACKLOG; el autor eligió hacerlas ahora, el 2026-10-29.

## Qué se construye

1. `BE-REGLETA`: una pieza impresa fija en una ranura lateral del perfil, con una muesca por cada separación de `SEP_SET` a cada lado del centro y su número grabado.
2. El punto de referencia en el centro de la regleta (x = 0, que es el origen de los ejes de la barra y queda encima de Marker0), grabado y legible con metro de cinta.
3. `BE-CARRO` nuevo: un diente que entra en la muesca, de modo que la posición a lo largo de la barra la fija la forma y el apriete solo la sujeta.
4. El ensamble y la exportación al día con las dos piezas, y pruebas que lo midan.

## Criterio de cierre

- En el modelo, el centro de cada muesca está en ±`sep`/2 ± 0.01 mm para todas las separaciones de `SEP_SET`.
- El juego del diente en la muesca a lo largo de X es ≤ 0.3 mm en total, que es el tope de V2.
- Interferencia de 0 mm³ en el ensamble para todas las separaciones; toda pieza nueva cabe en la cama.
- El punto de referencia está en x = 0 ± 0.01 mm del ensamble.
- Los centros de lente y el cruce de ejes de `S150-A12.5` no cambian respecto a la v01 (± 0.01 mm): la geometría óptica sigue igual.
- La suite completa pasa.

## Lo que no se toca

- La carcasa, la tapa, las cuñas, la pinza y el clip, y las decisiones D1–D6 y E1–E4.
- La posición de la carcasa bajo el carro: la óptica no cambia.
- `recursos/`.
- Los archivos de presentación de la v01: si el autor los da por buenos, siguen valiendo para pedir el capital.

## Preguntas que el plan tiene que contestar

- En qué ranura va la regleta y cómo se sujeta al perfil.
- El paso de las muescas: cada 12.5 mm por lado (las 5 separaciones) o solo 100/150/200.
- La forma del diente y la muesca para que el juego quede ≤ 0.3 mm.
- La forma del punto de referencia.
