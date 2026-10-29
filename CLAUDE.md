# CLAUDE.md — Diseño3D

Instrucciones para Claude Code en este repo. Los principios están en `docs/constitution.md` y aquí se citan por número (P1…P9); no se repiten.

## Al arrancar

Lee, en este orden:

1. `docs/constitution.md`.
2. `memory.md`: el estado de hoy y la línea «Spec activo».
3. Si hay spec activo: su `spec.md`, `plan.md` y `tasks.md`.
4. `docs/CONTEXT.md` cuando la tarea toque medidas, interfaces o manufactura.
5. `docs/BACKLOG.md` solo su índice, salvo que la tarea venga de él.

No leas `recursos/` entero: son piezas de terceros (Thingiverse) que sirven de referencia; abre solo el archivo que haga falta.

## El flujo de una meta

1. El autor pide algo; se escribe `specs/NNN-nombre/spec.md` a partir de `specs/_plantilla/`.
2. Se escribe `plan.md` (archivos, fases con criterio medible, BACKLOG, ADR, preguntas, títulos de commit) sin modelar nada (P2).
3. El autor lo lee y dice «autorizado». Solo entonces la línea 1 de `tasks.md` pasa a «Plan autorizado por el autor el AAAA-MM-DD».
4. Se hace una fase cada vez. Se mide su criterio (P3) y se marca su casilla en `tasks.md` con el número obtenido y la fecha.
5. Se cierra la fase (abajo) y se espera a que el autor diga «commiteado» antes de la siguiente.

## Cerrar una fase

- Pon al día `memory.md` (≤ 12 KB, con la línea «Spec activo» correcta).
- Pasa a `docs/BACKLOG.md` lo que quedó pendiente, con su prioridad, y a «Cerrados» lo que se cerró, con la fecha.
- Propón al autor los dos comandos listos para copiar: el `git add` exacto y el `git commit -m "<título>"` (español, imperativo, corto, sin coautor). No los ejecutes (P1).
- Cuenta los commits sin subir (`git rev-list --count @{u}..HEAD`, o `git rev-list --count HEAD` si no hay remoto). Al llegar a 10, avisa al autor de que toca hacer `git push`.

## Reglas de operación

- Nunca `git commit` ni `git push`, de ninguna forma (P1).
- Ninguna pieza toca el anillo del lente (P5); ninguna decisión de rigidez sin número (P3, P6).
- Medidas en milímetros y grados. Las roscas imperiales (1/4-20) se nombran como tales y su medida en mm va al lado.
- Los parámetros maestros viven solo donde diga `docs/CONTEXT.md` (P4); ninguna pieza repite un número a mano.
- Todo comando con tiempo límite (P8). Los temporales van al scratchpad o a `Claude outputs/`, nunca a la raíz.
- Documentos y textos para personas en español; identificadores (archivos de modelo, variables, parámetros) en inglés.
- Si algo choca con la constitución, para y avisa al autor.

## Entorno

- Windows 11, PowerShell y Git Bash. Python vía pyenv (`python`).
- Herramienta CAD: **sin decidir** (BACKLOG, alta). Hasta entonces no hay suite ni comprobación de «no cambió».
- Fabricación prevista: impresión 3D y/o perfil de aluminio 2020 (se define en `docs/CONTEXT.md`, fase 3).

## Cómo reportar

- Corto. Primero el resultado, luego el número que lo respalda, luego lo pendiente.
- Archivos como `ruta:línea`. Si un paso se saltó o una medida no se hizo, se dice.
- Al cerrar: archivos tocados con sus bytes, título del commit y `git add`.

## Una sola fuente por cosa

| Archivo | Qué guarda |
| --- | --- |
| `docs/constitution.md` | Lo que no se negocia |
| `CLAUDE.md` | Cómo se trabaja |
| `memory.md` | El estado de hoy y el spec activo |
| `docs/CONTEXT.md` | Requisitos, interfaces, parámetros maestros, entorno y manufactura |
| `docs/ARCHITECTURE.md` | El qué (etapa 2) |
| `docs/DECISIONS.md` | El porqué: ADR numerados (etapa 2) |
| `docs/BACKLOG.md` | Lo que falta |
| `docs/PRUEBAS.md` | Lo que se probó (etapa 2) |
| `specs/NNN-nombre/` | Una meta: `spec.md`, `plan.md`, `clarify.md`, `tasks.md` |
| `recursos/` | Piezas de terceros de referencia; no se editan |
