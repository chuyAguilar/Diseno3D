# Meta 004 — Barra en la abertura con inclinación indexada (concepto)

**Estado:** concepto con renders, 2026-11-12. No es una pieza fabricable: es la idea para quien la desarrolle. Sustituye la geometría de la v01 (ADR-002).

## Por qué

La v01 se diseñó con dos supuestos falsos (`docs/CONTEXT.md`, D5 y E1):

1. Las cámaras miraban **en vertical**, con la barra sobre el centro de la caja.
2. La pinza mordía el **borde superior de las paredes laterales**, como si la caja no tuviera techo.

La caja Puluz real (`camarasPosicion.jpeg`, `camarasPosicion2.jpeg`) está **cerrada por cinco lados**: el techo lleva el panel de luz y solo el frente está abierto. Las cámaras se cuelgan del **canto superior de la abertura** y miran **en diagonal**, de arriba al frente hacia abajo al fondo, donde están el tablero ChArUco y Marker0.

## La idea

![Vista desde el frente](renders/1-frente.png)

Un perfil 2020 cuelga del canto superior de la abertura, sujeto por una pinza en cada extremo. Cada pinza tiene un **pivote indexado**: el perfil entero gira sobre su propio eje y un pasador lo fija en una posición marcada. Las dos cámaras van montadas en el perfil con las mismas piezas de la v01 (carro, cuña y carcasa), así que **se inclinan juntas** y la geometría entre ellas no cambia.

![Vista lateral](renders/2-lateral.png)

### Tres ajustes, los tres paramétricos y repetibles (P7)

| Ajuste | Cómo se cambia en la pieza | Rango | Paso |
| --- | --- | --- | --- |
| Separación | Se desliza el carro hasta la muesca de la regleta | 100–300 mm | 25 mm |
| Convergencia | Se cambia la cuña bajo cada carcasa | 0–15° por cámara | 2.5° |
| Inclinación | Se saca el pasador, se gira la barra y se mete en otro agujero; se aprieta la perilla | 0–60° desde la vertical | 5° |

![Pivote](renders/3-pivote.png)

### Qué combinación usar

Los tres ajustes juntos deciden dónde se cruzan los ejes. Con la misma separación y la misma cuña, solo la inclinación mueve el cruce:

![Inclinaciones](renders/4-inclinaciones.png)

| Inclinación | Dónde queda el cruce (S250, cuña 15°) |
| --- | --- |
| 30° | 81 mm bajo el suelo: haría falta más cuña |
| **45°** | **En el suelo, junto a la pared del fondo** (y = 186 mm, z = −1 mm): la diagonal de la foto |
| 60° | Detrás de la pared del fondo: haría falta menos cuña |

Configuración dibujada: **S250-A15-P45**. Los lentes quedan a 234.5 mm uno del otro y los ejes, a 46.9° de la vertical, se cruzan a 453 mm de los lentes. Todo esto está medido sobre el modelo (`salidas/concepto-abertura/datos.txt`).

## Piezas

| Pieza | Estado |
| --- | --- |
| Perfil 2020 | Se acorta a **350 mm** para que quepa entre las paredes con un pivote en cada extremo |
| BE-CARRO, BE-CUNA (×7), BE-CARCASA + tapa, BE-CLIP-CABLE | **Las de la v01, sin cambios.** La carcasa sigue sin tocar el lente (P5) |
| **BE-PINZA-PIVOTE** ×2 (nueva) | Una mordaza en C abraza el canto del techo y se aprieta con un M5. De ella baja una placa con el agujero del eje y 13 agujeros de índice (0–60°, uno cada 5°) |
| **BE-CUBO-PERFIL** ×2 (nueva) | Disco atornillado al extremo del perfil (M5 al agujero central, con un saliente en la ranura para que no gire). Su eje pasa por la placa y lleva un agujero para el pasador |
| Pasador Ø3 + perilla ×2 | El pasador fija el ángulo; la perilla aprieta el cubo contra la placa para quitar el juego |
| BE-REGLETA (spec 002) | Muescas cada 12.5 mm por lado (separaciones de 100 a 300 mm) y punto de referencia en x = 0 |
| BE-PINZA-CAJA (v01) | **Se retira**: no hay borde libre arriba |

## Parámetros

Todos están en `concepto/abertura/params.py`; los que comparte con la v01 los lee de `cad/params.py`. Para dibujar otra configuración se cambian `SEP`, `CONV` o `PITCH` y se corre:

```powershell
.venv\Scripts\python.exe -m concepto.abertura.render   # ≈ 35 s → salidas/concepto-abertura/ (PNG, visor.html, datos.txt)
```

## Lo que quien lo construya tiene que resolver

1. **El canto de la abertura no está medido.** `EDGE_T` usa el 4.5 mm de la v01, que está SIN MEDIR, y hace falta saber si el canto es un marco rígido o tela con varilla. Hay que medirlo antes de imprimir la pinza.
2. **El pivote es la junta crítica de rigidez (P6).** Tiene que cumplir V1 (giro relativo entre cámaras < 0.05°) y, además, que la barra no cabecee bajo carga. Como las dos cámaras están en el mismo perfil, un cabeceo no cambia la calibración entre ellas, pero sí la pose respecto a Marker0. Se mide igual que V1: pose de Marker0 antes y después de tocar la barra.
3. **El espacio a las paredes es justo.** Con el perfil de 350 mm, la pinza llega a x = ±199 mm y las paredes están en ±200. Se gana espacio acortando el perfil o metiendo la placa por dentro del cubo.
4. **El cruce depende de los tres ajustes.** Conviene una tabla (o que `datos.txt` lo diga) con qué cuña usar para cada separación e inclinación. Con la cuña máxima de 15°, separaciones grandes cruzan lejos.
5. **Código de configuración.** El grabado pasa de `S150-A12.5` a algo como `S250-A15-P45`, con la inclinación incluida (P7; formato abierto en B5).

## Criterio de cierre (para la meta que lo desarrolle)

- El modelo tiene 0 mm³ de interferencia con la caja y entre piezas en todo el rango de los tres ajustes.
- En el modelo, cada agujero de índice da su inclinación nominal ± 0.1°.
- Físico: V1 y V2 se cumplen con la barra montada en el canto.

## Lo que no se toca

La carcasa, las cuñas, el carro y los clips de la v01; las holguras de `cad/params.py`; la presentación `salidas/S150-A12.5/` (queda como histórico).
