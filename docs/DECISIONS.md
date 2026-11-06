# Decisiones — ADR

El porqué de lo que no es obvio. Un ADR por decisión, numerado; no se borran, se sustituyen por otro que lo diga.

## ADR-001 · El agente hace commit y push (cambia P1)

- **Fecha:** 2026-11-05. **Estado:** aceptado por el autor.
- **Contexto:** P1 venía de la plantilla del método (segmentadorDicom): el autor hacía cada commit y ningún agente ejecutaba `git commit` ni `git push`; `.claude/settings.json` lo bloqueaba. En este proyecto el autor no quiere esa restricción.
- **Decisión:** el agente hace `git add` de archivos concretos, `git commit` y `git push` al cerrar cada fase. Se mantiene: el autor autoriza cada plan (P2), quien planea no modela y quien modela no prueba. Siguen bloqueados `git push --force` / `-f`; reescribir historia subida o cambiar la visibilidad del repo exige que el autor lo pida.
- **Consecuencias:** el historial se sube sin esperar al autor; un commit equivocado se corrige con otro commit, no reescribiendo. Desaparece el aviso «a los 10 commits sin subir».
