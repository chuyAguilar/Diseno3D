# CONTEXT — Barra estéreo para dos cámaras

Requisitos, interfaces, parámetros maestros, entorno y manufactura de la pieza base. Se rellena con la entrevista de definición (fases 1–3) y se consolida en la fase 4. Lo que aquí se fija lo leen todas las piezas (P4).

Estado: **fases 1 y 2 cerradas**; fase 3 pendiente.

## 1. Propósito e integración

### Propósito

Estructura que sostiene las dos cámaras del sistema de navegación (PoyectoNavegacion) con una línea base estéreo rígida, de separación y ángulo conocidos y repetibles, para que la calibración estéreo siga valiendo al tocar o mover la barra. Sustituye las dos pinzas independientes del montaje actual.

Sirve a la vez de banco de pruebas (elegir separación y ángulo) y de estructura fija a largo plazo: la versión fija es la de pruebas con la posición bloqueada (P7).

### Requisitos del autor

| Id | Requisito | Medida |
| --- | --- | --- |
| R1 | Rigidez entre cámaras | Giro relativo ≪ 0.1° (≈ 0.65 mm a 375 mm) (P6). Preferible aluminio 2020 o impresa gruesa con nervios. |
| R2 | Separación elegible y repetible | Marcas cada 25 mm; al menos 100, 150 y 200 mm entre centros de cámara. |
| R3 | Ángulo hacia dentro fijo y conocido | Cuñas con el ángulo grabado (0°, 5°, 10°); campos cruzados a 35–40 cm, donde va Marker0. |
| R4 | Montaje sin tocar el lente | Sujeción por la carcasa (P5). |
| R5 | Sujeción a la caja de luz o a un pie | Sin combarse ni girar; se mueve la barra entera sin aflojar cámaras. |
| R6 | Alivio de tensión de cables | Bridas o clips en la barra; el USB no tira de la cámara. |
| R7 | Punto de referencia en la barra | Agujero o marca legible con un metro de cinta. |

### Interfaces

| Elemento | Datos | Pendiente |
| --- | --- | --- |
| Cámaras (×2) | SVPRO USB, CMOS, lente M12 (el enfoque es la rosca del lente), FOV 85°, MJPEG. | B3: eje del FOV. |
| Carcasa | Thingiverse #4696080 (`recursos/38mm Board Mount…`): placa de 38 mm, carcasa 42.16 × 42.16 mm, base 29.21 mm + tapa trasera a presión 12.65 mm. Tuerca 1/4-20 a presión en la carcasa. | B4: medir la impresa y la salida del cable. |
| Adaptador actual | Thingiverse #2062243 (`recursos/GoPro to tripod…`): 1/4-20 ↔ GoPro. Aletas 2.95 mm, separación 3.45 mm, perno M5. | — |
| Caja de luz | Puluz, 40 × 40 × 40 cm; la barra se sujeta al borde, de ≈ 4.5 mm de grosor. | Fase 3: por dentro o por fuera. |
| Marker0 | En el suelo de la caja, a 35–40 cm de las cámaras. | — |
| Medición en el mundo | Metro de cinta (≈ 1 mm). | — |
| Software | Cada configuración tiene un código grabado (p. ej. `S150-A12.5`) que nombra su archivo de configuración. | B5: formato. |

## 2. Parametrización y estandarización

### Decisiones de arquitectura (fase 2)

| Id | Decisión | Por qué |
| --- | --- | --- |
| D1 | Se elimina la articulación GoPro: carcasa → 1/4-20 → cuña → barra. | La bisagra de fricción tiene ángulo desconocido y cede (P6). |
| D2 | Carcasa rediseñada con un elemento de registro antigiro (pasador o escalón), sin tocar la zona del lente. | Un solo tornillo deja girar la cámara sobre su eje (P5, P6). |
| D3 | El ángulo de la cuña es **por cámara**, hacia dentro; la convergencia total es el doble. | Elegido por el autor. |
| D4 | Objetivo: que los **ejes ópticos se crucen** a la distancia de trabajo. Juego de cuñas de 0° a 15° cada 2.5°. | Cruce a 375 mm: 7.6° (S100), 11.3° (S150), 14.9° (S200). |

Cruce de ejes con cuñas discretas: `D = (S/2) / tan(a)`. Ejemplos con S150: 10° → 425 mm, 12.5° → 338 mm.

### Parámetros maestros

Valores iniciales; los de holgura se validan con una probeta de tolerancias antes de la primera pieza (B7, P3). Se definirán en un único archivo de parámetros cuando haya herramienta CAD (B1, P4).

| Nombre | Valor | Qué es |
| --- | --- | --- |
| `clearance_slide` | 0.30 mm | Holgura de piezas que entran y salen |
| `clearance_press` | 0.10 mm | Holgura de tuercas y pasadores a presión |
| `hole_comp` | +0.20 mm (diámetro) | Compensación de agujeros verticales |
| `wall_struct` | 3.0 mm | Pared mínima portante |
| `wall_min` | 2.0 mm | Pared mínima no portante |
| `sep_step` | 25 mm | Paso de separación entre centros de cámara (R2) |
| `sep_set` | 100, 150, 200 mm (mín.) | Separaciones a probar |
| `angle_step` | 2.5° | Paso de cuñas, por cámara |
| `angle_range` | 0°–15° | Juego de cuñas |
| `work_dist` | 350–400 mm (nominal 375) | Distancia de trabajo a Marker0 |

### Fabricación y tornillería base

- Impresora Bambu Lab, boquilla 0.4 mm. **PLA para empezar; migración prevista a PETG.** Las piezas no deben depender de propiedades exclusivas del PLA, y las holguras se recalibran con la probeta al cambiar de material (B7). Riesgo de fluencia del PLA con carga sostenida y calor: se evalúa en la fase 3.
- Tornillería: **M5** con tuerca en T para el perfil 2020; **M3** en piezas pequeñas; **1/4-20** solo en la interfaz con la cámara (tuerca 11.25 mm entre caras, 5.6 mm de alto).

### Convenciones

- **Unidades:** milímetros y grados; punto decimal; dos decimales en cotas. Roscas imperiales por su nombre (1/4-20) con su medida en mm al lado.
- **Ejes de la barra (OpenCV):** origen en el punto de referencia (R7); X a lo largo de la barra hacia la cámara 2; Y hacia abajo; Z hacia Marker0.
- **Numeración de cámaras:** la que use el software de navegación (índice con que abre cada cámara); se marca físicamente en cada carcasa (B6).
- **Piezas (español):** `BE-<PIEZA>-<variante>-v<NN>`, BE = barra estéreo. Ejemplos: `BE-CUNA-A05.0-v01`, `BE-PINZA-CAJA-v01`, `BE-CARCASA-v01`.
- **Configuración:** `S<separación>-A<ángulo por cámara>`, ángulo con un decimal: `S150-A12.5`. Nombra también su archivo de configuración (B5).
- **Grabado:** cada pieza lleva su nombre y versión; las cuñas, además, el ángulo en grande.

## 3. Entorno y restricciones

*Pendiente (fase 3 de la entrevista).*
