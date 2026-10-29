# Meta 001 — Barra estéreo v01

## Por qué

El autor tiene que pedir capital a su empresa para los materiales de `docs/COMPRAS.md` y quiere convencerla enseñando el diseño real, no una ilustración. Además, la v01 es la primera versión de las piezas que se van a imprimir: el trabajo sirve para presentar y para fabricar. Viene de la entrevista de definición (`docs/CONTEXT.md`, fases 1–3) y cierra B2 y adelanta B7 del BACKLOG.

## Qué se construye

1. Un modelo paramétrico en build123d de todas las piezas de la barra, con los parámetros maestros en un solo archivo (P4): carcasa nueva con antigiro (D2), cuñas de 0° a 15° cada 2.5° (D4), carro sobre el perfil 2020, pinza de borde de caja (E1), clip de cable (R6), y el perfil 2020 como pieza de referencia (no se imprime).
2. La probeta de tolerancias (B7).
3. El ensamble completo en una configuración de presentación, dentro de la caja de 400 mm y con Marker0.
4. Para la presentación: el ensamble en STEP y 3MF (se abre y se gira en Bambu Studio o cualquier visor CAD) y vistas en PNG: isométrica, frontal, detalle de la cuña y detalle de la pinza.
5. Las pruebas automáticas de cotas de interfaz: la comprobación de «no cambió» (B2).

## Criterio de cierre

- Todas las pruebas pasan, y miden: interferencia 0 mm³ entre piezas del ensamble; ángulo de cada cuña medido sobre el modelo igual al nominal ± 0.01°; cruce de ejes del ensamble igual a `(S/2)/tan(a)` ± 1 mm; toda pieza impresa cabe en 256 × 256 × 256 mm; ninguna pieza impresa invade el volumen libre alrededor del lente (P5).
- Existen el STEP, el 3MF y los 4 PNG del ensamble, y el autor los abre y los da por buenos para presentar.

## Lo que no se toca

- Las decisiones y parámetros de `docs/CONTEXT.md`: si el modelo pide cambiar alguno, se para y se pregunta.
- `recursos/`: se leen, no se editan.
- Ninguna pieza se imprime dentro de esta meta salvo la probeta, y solo si el autor quiere.

## Preguntas que el plan tiene que contestar

- De dónde salen las medidas de la cámara (placa, portalente, conector) mientras no haya calibre (B4).
- Qué configuración se usa para la presentación.
- Cómo se generan las imágenes PNG sin una herramienta de render externa.
