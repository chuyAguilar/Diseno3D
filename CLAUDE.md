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
5. Se cierra la fase (abajo), con su commit y su push, y se espera a que el autor diga «sigue» antes de la siguiente.

## Cerrar una fase

- Pon al día `memory.md` (≤ 12 KB, con la línea «Spec activo» correcta).
- Pasa a `docs/BACKLOG.md` lo que quedó pendiente, con su prioridad, y a «Cerrados» lo que se cerró, con la fecha.
- Haz el `git add` de los archivos exactos (nunca `git add -A`) y `git commit -m "<título>"` (español, imperativo, corto, sin coautor), y luego `git push` (P1, ADR-001).
- Nunca `push --force`, ni reescribir historia ya subida, ni cambiar la visibilidad del repo sin que el autor lo pida.

## Reglas de operación

- Commit y push al cerrar cada fase (P1, ADR-001); nada de `--force`.
- Ninguna pieza toca el anillo del lente (P5); ninguna decisión de rigidez sin número (P3, P6).
- Medidas en milímetros y grados. Las roscas imperiales (1/4-20) se nombran como tales y su medida en mm va al lado.
- Los parámetros maestros viven solo donde diga `docs/CONTEXT.md` (P4); ninguna pieza repite un número a mano.
- Todo comando con tiempo límite (P8). Los temporales van al scratchpad o a `Claude outputs/`, nunca a la raíz.
- Documentos y textos para personas en español; identificadores (archivos de modelo, variables, parámetros) en inglés.
- Si algo choca con la constitución, para y avisa al autor.

## Entorno

- Windows 11, PowerShell y Git Bash. Python vía pyenv (`python`).
- CAD: **build123d** en `.venv` (Python 3.12; `requirements.txt`). Parámetros solo en `cad/params.py`.
- Suite y comprobación de «no cambió»: `.venv\Scripts\python.exe -m pytest -q` (≈ 31 s, 45 pruebas; tiempo límite 300 s).
- Exportar una configuración: `.venv\Scripts\python.exe -m cad.exportar S150-A12.5` (≈ 40 s) → `salidas/`, fuera de git.
- Piezas sueltas fuera de la barra: `taller/<pieza>/` (ver `taller/README.md`); se exportan con `.venv\Scripts\python.exe -m taller.<pieza>.exportar`.
- Revisar el diseño antes de exportar: `.venv\Scripts\python.exe -m cad.visor S150-A12.5` (≈ 7 s) o `-m cad.visor taller.<pieza>` → `visor.html` en su `salidas/`; se abre con doble clic (three.js de jsDelivr: pide internet).
- Tabla de parámetros: `.venv\Scripts\python.exe -m cad.listar_params` regenera `docs/PARAMETROS.md`; la suite falla si queda vieja.
- Ojo: `export_stl` falla en silencio con la «ñ» de la ruta; usar `cad.exportar._stl`, que pasa por una carpeta temporal.
- Fabricación: perfil de aluminio 2020 + piezas impresas en Bambu Lab (PLA, después PETG). Detalle en `docs/CONTEXT.md`.

## Cómo reportar

- Corto. Primero el resultado, luego el número que lo respalda, luego lo pendiente.
- Archivos como `ruta:línea`. Si un paso se saltó o una medida no se hizo, se dice.
- Al cerrar: archivos tocados con sus bytes y el hash y título del commit subido.

## Una sola fuente por cosa

| Archivo | Qué guarda |
| --- | --- |
| `docs/constitution.md` | Lo que no se negocia |
| `CLAUDE.md` | Cómo se trabaja |
| `memory.md` | El estado de hoy y el spec activo |
| `docs/CONTEXT.md` | Requisitos, interfaces, parámetros maestros, entorno y manufactura |
| `docs/ARCHITECTURE.md` | El qué (etapa 2) |
| `docs/DECISIONS.md` | El porqué: ADR numerados |
| `docs/BACKLOG.md` | Lo que falta |
| `docs/COMPRAS.md` | Lo que hay que comprar, con cantidades y precios de referencia |
| `docs/PRUEBAS.md` | Lo que se midió: criterio, número y método |
| `docs/PARAMETROS.md` | Tabla de parámetros **generada** desde los `params.py`; no es fuente |
| `specs/NNN-nombre/` | Una meta: `spec.md`, `plan.md`, `clarify.md`, `tasks.md` |
| `recursos/` | Piezas de terceros de referencia; no se editan |
