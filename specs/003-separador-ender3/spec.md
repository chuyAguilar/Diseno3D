# Meta 003 — Separador de cama para la Ender 3 V3 (prueba del proceso)

## Por qué

El autor necesita dos separadores para nivelar la cama de su Ender 3 V3, iguales al original salvo el largo: uno 0.7 mm más corto y otro 1.0 mm más corto. Es una pieza sencilla y sirve para probar de punta a punta, con algo real, el proceso que luego se usará en la barra: medir, parametrizar, modelar, comprobar con números, previsualizar, imprimir y volver a medir. Lo pidió el autor el 2026-11-03. No forma parte de la barra.

## Qué se construye

1. Un modelo paramétrico en `taller/separador_ender3/`, aparte de `cad/`, con las medidas del original y las fotos del calibre como fuente.
2. Dos piezas, `SEP-ENDER3-L15.0` y `SEP-ENDER3-L14.7`, una de cada.
3. Para cada pieza un STL, más un 3MF con las dos para Bambu Studio, una vista previa en PNG y un `datos.txt` con las cotas medidas sobre el modelo.
4. Una prueba de pytest que mide el modelo.

## Criterio de cierre

- En el modelo: largo 15.00 y 14.70 mm, diámetro exterior 7.80 mm y agujero 4.70 mm, todo ± 0.01 mm.
- La suite completa pasa.
- En la pieza impresa, medida con el mismo calibre que el original: largo igual al nominal ± 0.1 mm. El autor apunta lo que mide en `tasks.md`.

## Lo que no se toca

- `cad/` y la barra, salvo leer `HOLE_COMP` de `cad/params.py` (una sola fuente, P4).
- Los specs 001 y 002.

## Preguntas que el plan tiene que contestar

- Cómo se distinguen dos piezas que solo se diferencian en 0.3 mm.
- Qué altura de capa hace falta para que 14.7 mm salga exacto.
