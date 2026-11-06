# Parámetros — tabla generada

**No se edita a mano.** Sale de los `params.py` con `.venv\Scripts\python.exe -m cad.listar_params`;
la prueba `tests/test_parametros_doc.py` falla si no coincide. Para cambiar un valor se cambia
su `params.py` (P4) y se regenera. Unidades: mm y grados. «SIN MEDIR» = valor de la carcasa
de referencia, pendiente de calibre (B4).

## Barra estéreo (`cad/params.py`)

| Nombre | Valor | Se calcula como | Nota (del comentario) | Lo usan |
| --- | --- | --- | --- | --- |
| **Holguras y paredes (docs/CONTEXT.md, fase 2)** | | | | |
| `CLEARANCE_SLIDE` | 0.3 | — | piezas que entran y salen | `otros parámetros`, `piezas/carcasa`, `piezas/carro`, `piezas/clip_cable`, `piezas/cuna`, `piezas/pinza_caja` |
| `CLEARANCE_PRESS` | 0.1 | — | tuercas y pasadores a presión | `piezas/carcasa`, `piezas/cuna`, `piezas/pinza_caja` |
| `HOLE_COMP` | 0.2 | — | se suma al diámetro de los agujeros verticales | `piezas/carcasa`, `piezas/carro`, `piezas/cuna`, `piezas/pinza_caja`, `piezas/probeta`, `taller/separador_ender3/params` |
| `WALL_STRUCT` | 3 | — | pared mínima portante | `otros parámetros` |
| `WALL_MIN` | 2 | — | pared mínima no portante | `otros parámetros` |
| **Configuraciones (R2, R3, D3, D4)** | | | | |
| `SEP_STEP` | 25 | — | — | — |
| `SEP_SET` | (100, 125, 150, 175, 200) | — | — | — |
| `ANGLE_STEP` | 2.5 | — | por cámara | `otros parámetros` |
| `ANGLE_SET` | (0, 2.5, 5, 7.5, 10, 12.5, 15) | `tuple(i * ANGLE_STEP for i in range(7))` | 0.0 … 15.0 | `cad/exportar` |
| `WORK_DIST` | 375 | — | nominal; rango 350–400 | — |
| `PRESENTATION_CONFIG` | (150, 12.5) | — | S150-A12.5 (clarify P3) | `cad/ensamble`, `cad/exportar`, `cad/visor` |
| **Impresión (Bambu Lab)** | | | | |
| `BED` | (256, 256, 256) | — | — | — |
| **Perfil de aluminio 2020, ranura de 6 mm (E3)** | | | | |
| `PROFILE_SIZE` | 20 | — | — | `otros parámetros`, `piezas/clip_cable`, `piezas/perfil_2020`, `piezas/pinza_caja` |
| `PROFILE_LEN` | 440 | — | — | `cad/ensamble`, `piezas/perfil_2020` |
| `SLOT_OPENING` | 6.2 | — | ancho de la boca de la ranura | `otros parámetros`, `piezas/carro`, `piezas/clip_cable`, `piezas/perfil_2020`, `piezas/probeta` |
| `SLOT_LIP` | 1.8 | — | grosor del labio | `otros parámetros`, `piezas/clip_cable`, `piezas/perfil_2020` |
| `SLOT_CHAMBER_W` | 11 | — | ancho de la cámara interior | `otros parámetros`, `piezas/perfil_2020` |
| `SLOT_DEPTH` | 6.1 | — | de la cara exterior al núcleo | `piezas/perfil_2020` |
| `PROFILE_BORE` | 4.2 | — | agujero central | `piezas/perfil_2020` |
| **Tornillería (B4 de la fase 2)** | | | | |
| `NUT_14_20_FLATS` | 11.11 | — | tuerca 1/4-20, entre caras | `piezas/carcasa`, `piezas/probeta` |
| `NUT_14_20_H` | 5.6 | — | — | `piezas/carcasa`, `piezas/probeta` |
| `BOLT_14_20_D` | 6.35 | — | — | `piezas/carcasa`, `piezas/cuna`, `piezas/probeta` |
| `M5_D` | 5 | — | — | `piezas/carro`, `piezas/pinza_caja` |
| `M3_D` | 3 | — | — | `piezas/carcasa`, `piezas/carro`, `piezas/cuna`, `piezas/pinza_caja` |
| `PIN_D` | 3 | — | pasador de acero Ø3 | `piezas/carcasa`, `piezas/cuna`, `piezas/probeta` |
| `PIN_LEN` | 12 | — | — | — |
| **Caja de luz (E1)** | | | | |
| `BOX_SIZE` | 400 | — | — | `cad/ensamble` |
| `BOX_RIM` | 4.5 | — | grosor del borde donde muerde la pinza | `cad/ensamble`, `piezas/pinza_caja`, `piezas/probeta` |
| **Cámara y carcasa de referencia (SIN_MEDIR: Camera_Case_Snap_Base, clarify P1-P2)** | | | | |
| `CASE_REF_OUTER` | 42.16 | — | **SIN MEDIR** | — |
| `CASE_REF_DEPTH` | 29.21 | — | **SIN MEDIR** | — |
| `CASE_REF_WALL` | 1.52 | — | **SIN MEDIR** | — |
| `CASE_REF_CAVITY` | 39.12 | — | **SIN MEDIR** | — |
| `CAM_BOARD` | 38 | — | **SIN MEDIR** | `otros parámetros` |
| `LENS_HOLE_D` | 14.6 | — | **SIN MEDIR** · agujero del lente en la carcasa de referencia | — |
| `LENS_KEEPOUT` | 1.5 | — | holgura radial mínima entre el lente y cualquier pieza (P5) | `otros parámetros` |
| `BOARD_T` | 1.6 | — | **SIN MEDIR** · grosor de la placa de la cámara | `otros parámetros`, `piezas/carcasa` |
| `LENS_BARREL_D` | 14 | — | **SIN MEDIR** · diámetro exterior del portalente M12 (cabe en el agujero de 14.6) | `otros parámetros` |
| `CAM_BEHIND_BOARD` | 20.4 | — | **SIN MEDIR** · fondo libre detrás de la placa (conector USB y componentes) | `otros parámetros` |
| `CABLE_SLOT` | (12, 8) | — | **SIN MEDIR** · salida del cable en la pared +Y: ancho × alto | `piezas/carcasa` |
| **Carcasa nueva BE-CARCASA (D2). Mira hacia -Z; la cara trasera de montaje está en z = 0** | | | | |
| `CASE_WALL` | 2 | `WALL_MIN` | — | `otros parámetros`, `piezas/carcasa` |
| `CASE_CAVITY` | 38.6 | `CAM_BOARD + 2 * CLEARANCE_SLIDE` | — | `otros parámetros`, `piezas/carcasa` |
| `CASE_OUTER` | 42.6 | `CASE_CAVITY + 2 * CASE_WALL` | — | `otros parámetros`, `cad/ensamble`, `piezas/carcasa`, `piezas/cuna` |
| `CASE_BACK_T` | 8 | — | aloja la tuerca 1/4-20 y los pasadores; ≥ WALL_STRUCT | `otros parámetros`, `cad/ensamble`, `piezas/carcasa` |
| `CASE_DEPTH` | 30 | `CASE_BACK_T + CAM_BEHIND_BOARD + BOARD_T` | hasta la cara frontal de la placa | `piezas/carcasa` |
| `CASE_FLANGE` | 56 | — | brida frontal para los 4 tornillos M3 de la tapa | `piezas/carcasa` |
| `CASE_FLANGE_T` | 4 | — | — | `piezas/carcasa` |
| `CASE_SCREW_XY` | 24.5 | — | tornillos de la tapa en (±, ±) | `piezas/carcasa` |
| `CASE_LID_T` | 3 | — | — | `piezas/carcasa` |
| `CASE_POST` | 3 | — | postes que aprietan la placa contra la tapa | `piezas/carcasa` |
| `CASE_PIN_X` | 13 | — | pasadores antigiro en (±CASE_PIN_X, 0) de la cara trasera | `otros parámetros`, `piezas/carcasa`, `piezas/cuna` |
| `PIN_DEPTH` | 6 | — | — | `piezas/carcasa`, `piezas/cuna` |
| `LENS_CLEAR_D` | 17 | `LENS_BARREL_D + 2 * LENS_KEEPOUT` | — | `piezas/carcasa` |
| **Tornillos de unión** | | | | |
| `BOLT_14_20_LEN` | 12.7 | — | — | — |
| `BOLT_14_20_HEAD_D` | 9.5 | — | — | `piezas/cuna` |
| `BOLT_14_20_HEAD_H` | 6.35 | — | — | — |
| `M3_NUT_FLATS` | 5.5 | — | — | `piezas/carcasa`, `piezas/cuna`, `piezas/pinza_caja` |
| `M3_NUT_H` | 2.4 | — | — | `piezas/carcasa`, `piezas/cuna`, `piezas/pinza_caja` |
| **Marco de la barra: el perfil va a lo largo de X, centrado en el origen; Z hacia arriba** | | | | |
| `PROFILE_BOTTOM` | -10 | `-PROFILE_SIZE / 2` | — | `piezas/carro`, `piezas/pinza_caja` |
| **Carro BE-CARRO: bajo el perfil, con llave en la ranura inferior y 2 M5 a tuercas en T** | | | | |
| `CARRO_SIZE` | 42.6 | `CASE_OUTER` | mismo apoyo que la cuña | `piezas/carro` |
| `CARRO_T` | 10 | — | — | `piezas/carro` |
| `KEY_H` | 1.5 | — | altura de la llave; menor que SLOT_LIP | `piezas/carro`, `piezas/probeta` |
| `CARRO_M5_X` | 12 | — | M5 en (±CARRO_M5_X, 0) | `otros parámetros`, `piezas/carro` |
| `M5_HEAD_D` | 8.5 | — | — | `piezas/carro` |
| `M5_HEAD_H` | 5 | — | — | `piezas/carro` |
| **Pinza BE-PINZA-CAJA: muerde el borde superior de una pared lateral y sostiene el perfil** | | | | |
| `PINZA_LEN` | 30 | — | a lo largo de la barra | `piezas/pinza_caja` |
| `PINZA_CRADLE_WALL` | 4 | — | — | `piezas/pinza_caja` |
| `PINZA_FLOOR` | 5 | — | entre el borde de la caja y el perfil | `piezas/pinza_caja` |
| `PINZA_JAW` | 5 | — | — | `piezas/pinza_caja` |
| `PINZA_JAW_DEPTH` | 25 | — | cuánto baja por la pared | `piezas/pinza_caja` |
| `PINZA_CRADLE_UP` | 6 | — | cuánto sube la cuna por los lados del perfil (desde su centro) | `piezas/pinza_caja` |
| **Clip de cable BE-CLIP-CABLE: cierre de cuarto de vuelta en la ranura superior** | | | | |
| `CABLE_D` | 4.5 | — | **SIN MEDIR** · SIN_MEDIR: diámetro del cable USB | `cad/exportar`, `piezas/clip_cable` |
| `CLIP_TAB_L` | 10.5 | — | entre SLOT_OPENING y SLOT_CHAMBER_W | `piezas/clip_cable` |
| `CLIP_TAB_T` | 1.5 | — | — | `piezas/clip_cable` |
| `CLIP_RING_WALL` | 1.6 | — | — | `piezas/clip_cable` |
| **Cuña BE-CUNA (D3, D4). Cara superior en z = 0 contra el carro; la inferior, inclinada, contra la carcasa** | | | | |
| `WEDGE_T0` | 11 | — | grosor en el canto fino: cabe la cabeza del 1/4-20 a 0° | `piezas/cuna` |
| `WEDGE_SEAT` | 4 | — | material bajo la cabeza del tornillo | `piezas/cuna` |
| `WEDGE_M3_Y` | 15 | — | tornillos M3 al carro en (0, ±WEDGE_M3_Y) | `otros parámetros`, `piezas/carro`, `piezas/cuna` |
| **Probeta de tolerancias (B7)** | | | | |
| `PROBE_CLEARANCES` | (0, 0.1, 0.2, 0.3, 0.4) | — | — | `piezas/probeta` |

## Taller · separador_ender3 (`taller/separador_ender3/params.py`)

| Nombre | Valor | Se calcula como | Nota (del comentario) | Lo usan |
| --- | --- | --- | --- | --- |
| **Original, medido (fotos/)** | | | | |
| `ORIG_LEN` | 15.7 | — | largo.jpeg | `otros parámetros`, `taller/separador_ender3/exportar` |
| `OUTER_D` | 7.8 | — | ancho.jpeg | `taller/separador_ender3/exportar`, `taller/separador_ender3/medir_pieza`, `taller/separador_ender3/modelo` |
| `BORE_MEASURED` | 4.5 | — | tamaño interior.jpeg (puntas de interiores) | `otros parámetros`, `taller/separador_ender3/exportar` |
| **Piezas nuevas** | | | | |
| `BORE_D` | 4.7 | `BORE_MEASURED + HOLE_COMP` | el agujero impreso sale más cerrado (clarify P4) | `taller/separador_ender3/exportar`, `taller/separador_ender3/modelo` |
| `SHORTEN` | (0.7, 1) | — | cuánto más cortas que el original | `otros parámetros` |
| `LENGTHS` | (15, 14.7) | `tuple(round(ORIG_LEN - s, 2) for s in SHORTEN)` | 15.0, 14.7 | `taller/separador_ender3/modelo` |
| `CHAMFER` | 0.3 | — | canto exterior de abajo, contra la pata de elefante | `taller/separador_ender3/medir_pieza`, `taller/separador_ender3/modelo` |
| `MARK_W` | 0.6 | — | ancho de cada ranura de identificación | `taller/separador_ender3/modelo` |
| `MARK_D` | 0.3 | — | profundidad de la ranura | `taller/separador_ender3/medir_pieza`, `taller/separador_ender3/modelo` |
| `MARK_PITCH` | 2 | — | entre ranuras | `taller/separador_ender3/modelo` |
| `LAYER_H` | 0.1 | — | altura de capa para que 14.7 salga exacto (se elige en Bambu Studio) | `taller/separador_ender3/exportar` |
