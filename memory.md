# Memoria — estado de hoy

Spec activo: `specs/004-reorientacion-abertura/` (concepto con renders entregado el 2026-11-12; el desarrollo lo hará otra persona, B12). La v01 (spec 001) queda como histórico: su geometría no corresponde a la caja real (ADR-002).

## Dónde estamos (2026-11-12)

- **Corrección de geometría (ADR-002):** la caja Puluz está cerrada por cinco lados; las cámaras cuelgan del canto superior de la abertura y miran en diagonal hacia el fondo. Concepto en `concepto/abertura/` (`python -m concepto.abertura.render`, ≈ 35 s): pinza con pivote indexado de 0 a 60° cada 5°, que gira toda la barra; configuración dibujada S225-A15-P40, con los ejes cruzados a 405 mm (propósito: zona de trabajo a unos 40 cm). Renders y `visor.html` (sin panel, para compartir) en `specs/004-reorientacion-abertura/`. Los modelos de cámara que usa el autor (Thingiverse 4696080 y 2062243) son los de `recursos/`; `modelos3d/` es una copia.

- Método montado: etapa 1 (constitución, CLAUDE.md, memory, BACKLOG, plantilla de spec, settings, .gitignore). Etapas 2 (papeles) y 3 (barreras) pendientes.
- Entrevista de definición de la pieza base (barra estéreo para dos cámaras): **cerrada (fases 1–4)**. `docs/CONTEXT.md` §0 lista los requisitos verificables V1–V10 con su estado en la v01.
- Decidido: perfil 2020 de borde a borde de la caja, cámaras colgando por dentro, PLA para empezar (PETG después), CAD en build123d, se transporta.
- Montaje actual (`camarasPosicion.jpeg`): dos cámaras en carcasas impresas, cada una con pinza y brazos GoPro al techo de la caja de luz; cables sueltos; Marker0 en el suelo.

## Lo siguiente

1. Revisión del autor de `salidas/S150-A12.5/` (STEP, 3MF, 4 PNG) para pedir capital; si la da por buena, se cierra el spec 001. Ensamble en `cad/ensamble.py`, exportación en `cad/exportar.py`.
   La separación v01 se sujeta por apriete: B9 (regleta) pendiente por P7.
   Nota build123d 0.13: el texto en planos no horizontales se graba fuera de BuildPart (`carcasa.engrave`). La barra v01 servirá para pedir capital a la empresa (STEP/3MF + PNG).
   Medidas de cámara: de `Camera_Case_Snap_Base` (cavidad 39.12, pared 1.52, lente Ø14.6, tuerca 1/4-20 en un lateral); «sin medir» hasta B4.
2. Spec 002 (regleta, B9 + B10): en pausa; su idea entra en el concepto v02 (muescas de 100 a 300 mm).
3. Comprar los materiales (B8, `docs/COMPRAS.md`).
4. Spec 003 (`specs/003-separador-ender3/`, separadores de la Ender 3 V3 en `taller/`): impresos y funcionando (2026-11-05); falta el largo medido con calibre para cerrarlo (P3). Fue la prueba del proceso para B11.
5. Herramientas nuevas (2026-11-05): `cad/visor.py` (visor 3D HTML, ≈ 7 s, para revisar antes de STL), `docs/PRUEBAS.md` (bitácora de mediciones) y `docs/PARAMETROS.md` (generada por `cad/listar_params.py`, con prueba de que está al día).
