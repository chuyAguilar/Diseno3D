# Plan — Meta 001

## Lo leído

`specs/001-barra-v01/spec.md`, `docs/CONTEXT.md` (fases 1–3), `docs/BACKLOG.md`, `recursos/38mm Board Mount…` (STL y README) y `recursos/GoPro to tripod…` (`goProToTripod.scad`). Repo sin código; Python 3.10.11 por defecto en pyenv, 3.12.10 disponible.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `requirements.txt` | build123d, pyvista, pytest, con versiones fijas |
| `.venv/` | Entorno de Python 3.12 del proyecto (fuera de git) |
| `cad/params.py` | **Única fuente** de parámetros maestros y de interfaz (P4) |
| `cad/piezas/perfil_2020.py` | Perfil de referencia, para el ensamble y las pruebas (no se imprime) |
| `cad/piezas/carcasa.py` | `BE-CARCASA` base y `BE-CARCASA-TAPA`: placa de 38 mm, tuerca 1/4-20 insertada, 2 pasadores Ø3 antigiro |
| `cad/piezas/cuna.py` | `BE-CUNA-Axx.x`: cuña con ángulo, pasadores, rosca pasante 1/4-20 y ángulo grabado |
| `cad/piezas/carro.py` | `BE-CARRO`: abraza el perfil, 2 tornillos M5 con tuerca en T, ventana para leer la marca de separación |
| `cad/piezas/pinza_caja.py` | `BE-PINZA-CAJA`: apoya el perfil sobre el borde de 4.5 mm y lo aprieta con un tornillo M3 |
| `cad/piezas/clip_cable.py` | `BE-CLIP-CABLE`: clip para la ranura 2020 |
| `cad/piezas/probeta.py` | `BE-PROBETA`: agujeros, pasadores, ranura y alojamiento 1/4-20 con varias holguras (B7) |
| `cad/ensamble.py` | Ensambla una configuración `S<sep>-A<ang>` dentro de la caja, con Marker0 |
| `cad/exportar.py` | Exporta STL por pieza, STEP y 3MF del ensamble y los 4 PNG a `salidas/` |
| `tests/test_piezas.py` | Cotas de interfaz, ángulos, cama de impresión, zona libre del lente |
| `tests/test_ensamble.py` | Interferencias, cruce de ejes, separación |
| `.gitignore` | Añade `.venv/` y `salidas/` (todo lo exportado se regenera) |

## Piezas y parámetros

- Usan los de `docs/CONTEXT.md` (`clearance_*`, `hole_comp`, `wall_*`, `sep_*`, `angle_*`, `work_dist`), copiados una sola vez a `cad/params.py`.
- Parámetros de interfaz nuevos, también en `params.py`: perfil 2020 (20 × 20, ranura de 6 mm); tuerca 1/4-20 (11.25 mm entre caras × 5.6 mm, del `.scad` de referencia); pasador Ø3; tuerca en T M5; borde de caja de 4.5 mm; placa de cámara de 38 mm; `lens_keepout`, el volumen libre alrededor del portalente (P5).
- Las medidas de la cámara se toman de la carcasa de referencia, que ya encaja en las cámaras reales (P1 de `clarify.md`), y se marcan «sin medir» hasta B4.
- Funciones: cada pieza expone `build(**params) -> Part`; `ensamble.build(sep_mm: int, ang_deg: float) -> Compound`; `exportar.main(config: str) -> None`.

## Fases

1. **Entorno, parámetros y probeta.** `.venv`, `requirements.txt`, `params.py`, perfil de referencia y probeta. *Criterio:* `pytest` corre en < 60 s y pasa; la probeta cabe en la cama y sus holguras van de 0.0 a 0.4 mm en pasos de 0.1 mm, verificadas sobre el modelo.
2. **Carcasa y cuñas.** *Criterio:* cavidad = 38 mm + 2·`clearance_slide`; el portalente tiene ≥ 1.5 mm de holgura radial respecto a cualquier pieza impresa (P5); el ángulo de cada una de las 7 cuñas, medido entre sus dos caras de apoyo, es igual al nominal ± 0.01°; paredes ≥ `wall_struct` en las zonas de carga.
3. **Carro, pinza y clip.** *Criterio:* la llave del carro entra en la ranura con `clearance_slide`; la boca de la pinza mide 4.5 mm + `clearance_slide`; todas las piezas caben en 256 × 256 × 256 mm.
4. **Ensamble y exportación.** *Criterio:* interferencia 0 mm³ entre piezas; el cruce de ejes calculado sobre el ensamble es igual a `(S/2)/tan(a)` ± 1 mm; se generan STEP, 3MF y 4 PNG; el autor los abre y los da por buenos.

## Lo que va al BACKLOG

- **Media:** volver a medir la cámara real con calibre y ajustar `params.py` (ya existe, B4).
- **Media:** pieza de bloqueo para la versión fija a largo plazo (P7), cuando se elija la configuración.
- **Baja:** soporte para pie o trípode (E1 lo descarta por ahora).

## ADR que se proponen

- **ADR-001:** build123d como CAD y `cad/params.py` como única fuente de parámetros.
- **ADR-002:** se elimina la bisagra GoPro (D1) y la carcasa se rediseña con antigiro (D2).

Se escriben en `docs/DECISIONS.md` en la etapa 2 del método.

## Preguntas abiertas

En `clarify.md`: P1–P4.

## Títulos de commit

1. `Monta el entorno build123d, los parámetros maestros y la probeta`
2. `Modela la carcasa con antigiro y las cuñas de 0 a 15 grados`
3. `Modela el carro, la pinza de borde y el clip de cable`
4. `Ensambla la barra S150-A12.5 y exporta STEP, 3MF y vistas`
