# Aclaraciones — Meta 001

## P1 · ¿De dónde salen las medidas de la cámara sin calibre?

- **Opciones:** (a) de la carcasa de Thingiverse que ya usas, que encaja en las cámaras reales: se mide la cavidad y el agujero del lente sobre el STL; (b) esperar al calibre (B4).
- **Recomendada:** (a), marcando esas medidas como «sin medir» en `params.py` hasta B4.
- **Respuesta del autor:** (a): medidas de la carcasa de Thingiverse, marcadas «sin medir» hasta B4.
- **Fecha:** 2026-10-29

## P2 · ¿Qué base de carcasa imprimiste?

- **Opciones:** `Camera_Case_Snap_Base`, `…_Large_Lens_Hole` (agujero de 0.65") o `…_1.7mm_lens`.
- **Respuesta del autor:** `Camera_Case_Snap_Base`.
- **Fecha:** 2026-10-29

## P3 · ¿Qué configuración se usa para la presentación?

- **Opciones:** `S150-A12.5` (los ejes se cruzan a 338 mm, la más cercana a los 375 nominales); `S150-A10.0` (cruce a 425 mm).
- **Recomendada:** `S150-A12.5`. El ensamble acepta cualquier configuración, así que se pueden exportar varias.
- **Respuesta del autor:** `S150-A12.5`.
- **Fecha:** 2026-10-29

## P4 · ¿Cómo se generan los PNG?

- **Opciones:** (a) pyvista sin ventana: vistas sombreadas a partir de los STL, todo en Python; (b) dibujos de líneas en SVG con build123d, más técnicos y menos vistosos.
- **Recomendada:** (a).
- **Respuesta del autor:** (a): pyvista, vistas sombreadas.
- **Fecha:** 2026-10-29
