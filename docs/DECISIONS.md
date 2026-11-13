# Decisiones — ADR

El porqué de lo que no es obvio. Un ADR por decisión, numerado; no se borran, se sustituyen por otro que lo diga.

## ADR-001 · El agente hace commit y push (cambia P1)

- **Fecha:** 2026-11-05. **Estado:** aceptado por el autor.
- **Contexto:** P1 venía de la plantilla del método (segmentadorDicom): el autor hacía cada commit y ningún agente ejecutaba `git commit` ni `git push`; `.claude/settings.json` lo bloqueaba. En este proyecto el autor no quiere esa restricción.
- **Decisión:** el agente hace `git add` de archivos concretos, `git commit` y `git push` al cerrar cada fase. Se mantiene: el autor autoriza cada plan (P2), quien planea no modela y quien modela no prueba. Siguen bloqueados `git push --force` / `-f`; reescribir historia subida o cambiar la visibilidad del repo exige que el autor lo pida.
- **Consecuencias:** el historial se sube sin esperar al autor; un commit equivocado se corrige con otro commit, no reescribiendo. Desaparece el aviso «a los 10 commits sin subir».

## ADR-002 · La barra cuelga del canto de la abertura y se inclina con pivote indexado (sustituye D5 y E1)

- **Fecha:** 2026-11-12. **Estado:** aceptado por el autor como concepto (spec 004); falta desarrollarlo.
- **Contexto:** la v01 suponía cámaras en vertical sobre Marker0 (D5) y una pinza sobre el borde superior de las paredes laterales (E1). Las fotos `camarasPosicion.jpeg` y `camarasPosicion2.jpeg` muestran que la caja Puluz está cerrada por cinco lados (el techo lleva el panel de luz), que las cámaras cuelgan del canto superior de la abertura y que miran en diagonal hacia el fondo.
- **Opciones para la inclinación:** (1) pivote indexado en la pinza, que gira toda la barra con un pasador cada 5°; (2) una pinza fija por cada ángulo. El autor eligió la 1 para ajustar sin reimprimir.
- **Decisión:** el perfil cuelga del canto superior de la abertura con una BE-PINZA-PIVOTE en cada extremo y gira sobre su eje de 0° a 60°, con un índice cada 5°. Las cámaras se inclinan juntas sobre el mismo perfil y conservan las piezas v01 (carro, cuña, carcasa).
- **Consecuencias:** se retira BE-PINZA-CAJA. Aparece una tercera coordenada en el código de configuración (P de inclinación). El pivote pasa a ser la junta crítica de rigidez, que hay que medir con V1. El cruce de ejes depende de separación, cuña e inclinación juntas.
