# Plan — Meta 003

## Lo leído

Las fotos del calibre que el autor dejó en `tests/`:
- `ancho.jpeg`: diámetro exterior 7.8 mm.
- `largo.jpeg`: largo 15.7 mm.
- `tamaño interior.jpeg`: agujero de 4.5 mm, medido con las puntas de interiores.

También `cad/params.py` (`HOLE_COMP` = 0.20) y `.gitignore` (`salidas/` ya queda fuera de git en cualquier carpeta).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `taller/README.md` | Para qué es `taller/`: piezas sueltas fuera de la barra, con el mismo método |
| `taller/separador_ender3/fotos/` | Las tres fotos, que se mueven desde `tests/` (`tests/` es solo para pytest) |
| `taller/separador_ender3/params.py` | Medidas del original y los dos acortamientos; importa `HOLE_COMP` de `cad/params.py` |
| `taller/separador_ender3/modelo.py` | `build(length: float) -> Part`; `variants() -> list[Part]` |
| `taller/separador_ender3/exportar.py` | STL de cada pieza, 3MF con las dos, `vista.png` y `datos.txt` en `taller/separador_ender3/salidas/` |
| `tests/test_taller_separador.py` | Mide largo, diámetro exterior, agujero y que cada pieza lleva su marca |

## Piezas y parámetros

| Nombre | Valor | De dónde |
| --- | --- | --- |
| `ORIG_LEN` | 15.7 mm | `largo.jpeg` |
| `OUTER_D` | 7.8 mm | `ancho.jpeg` |
| `BORE_MEASURED` | 4.5 mm | `tamaño interior.jpeg` |
| `BORE_D` | `BORE_MEASURED + HOLE_COMP` = 4.7 mm | Respuesta del autor |
| `SHORTEN` | (0.7, 1.0) mm | El autor → largos 15.0 y 14.7 |
| `CHAMFER` | 0.3 mm | Bisel en el canto exterior de abajo, contra la «pata de elefante» de la primera capa |
| `MARK_W`, `MARK_D` | 0.6 mm, 0.3 mm | Ranuras de identificación |

**Cómo se distinguen las dos piezas.** Una diferencia de 0.3 mm no se ve a simple vista. Por eso cada pieza lleva ranuras en el costado, a media altura: **1 ranura la de 15.0 y 2 ranuras la de 14.7**, de 0.3 mm de profundidad. No hay sitio para texto: la pared mide 1.55 mm.

## Impresión (Bambu Lab, PETG)

- De pie, sobre una de sus caras planas.
- Capa de **0.1 mm**: 14.7 no es múltiplo de 0.2, y con capas de 0.2 mm el laminador lo redondearía a 14.6 o a 14.8.
- El 3MF solo guarda la geometría. La altura de capa y el filamento se eligen en Bambu Studio; la exportación no los puede fijar.
- Al imprimir, se mide el largo con el calibre. Si sale corto o largo de forma sistemática, el error se apunta y se corrige en el modelo (P3).

## Fases

1. **Modelo, prueba y exportación.**
   - *Criterio:* en el modelo, largo 15.00 y 14.70, diámetro exterior 7.80 y agujero 4.70, todo ± 0.01 mm. La pieza de 15.0 tiene 1 ranura y la de 14.7 tiene 2. La suite pasa. Se generan los 2 STL, el 3MF, el PNG y `datos.txt`.
   - *Después de imprimir:* el autor mide el largo y lo apunta en `tasks.md`, con criterio ± 0.1 mm.

## Lo que va al BACKLOG

- **Media:** convertir este proceso en la skill `fase`/`pieza` de la etapa 2 del método (diseñador CAD repetible), con lo que se aprenda aquí.

## ADR que se proponen

Ninguno.

## Preguntas abiertas

Ninguna: las cuatro se respondieron el 2026-11-03 (`clarify.md`).

## Títulos de commit

1. `Modela los separadores de cama de la Ender 3 V3`
