# Memoria — estado de hoy

Spec activo: `specs/001-barra-v01/` (fases 1–4 hechas; falta que el autor dé por buenos los archivos de `salidas/S150-A12.5/` para cerrar el spec).

## Dónde estamos (2026-10-29)

- Método montado: etapa 1 (constitución, CLAUDE.md, memory, BACKLOG, plantilla de spec, settings, .gitignore). Etapas 2 (papeles) y 3 (barreras) pendientes.
- Entrevista de definición de la pieza base (barra estéreo para dos cámaras): **fases 1, 2 y 3 cerradas** (en `docs/CONTEXT.md`); falta la fase 4 (consolidación).
- Decidido: perfil 2020 de borde a borde de la caja, cámaras colgando por dentro, PLA para empezar (PETG después), CAD en build123d, se transporta. La fase 4 consolida en `docs/CONTEXT.md`.
- Montaje actual (`camarasPosicion.jpeg`): dos cámaras en carcasas impresas, cada una con pinza y brazos GoPro al techo de la caja de luz; cables sueltos; Marker0 en el suelo.

## Lo siguiente

1. Revisión del autor de `salidas/S150-A12.5/` (STEP, 3MF, 4 PNG) para pedir capital; si la da por buena, se cierra el spec 001. Ensamble en `cad/ensamble.py`, exportación en `cad/exportar.py`.
   La separación v01 se sujeta por apriete: B9 (regleta) pendiente por P7.
   Nota build123d 0.13: el texto en planos no horizontales se graba fuera de BuildPart (`carcasa.engrave`). La barra v01 servirá para pedir capital a la empresa (STEP/3MF + PNG).
   Medidas de cámara: de `Camera_Case_Snap_Base` (cavidad 39.12, pared 1.52, lente Ø14.6, tuerca 1/4-20 en un lateral); «sin medir» hasta B4.
2. Fase 4 de la entrevista: consolidar `docs/CONTEXT.md`.
3. Comprar los materiales (B8, `docs/COMPRAS.md`).
