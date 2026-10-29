# Constitución — Diseño3D

Lo que no se negocia. Cada principio dice de dónde viene. Si algo choca con esta constitución, gana la constitución y se avisa al autor. Cambiar un principio exige un ADR (principio 9).

1. **Cada quien su papel.** El autor autoriza cada plan y hace cada commit; ningún agente ejecuta `git commit` ni `git push`. Quien modela no prueba; quien planea no modela. *Fuente: método del autor (segmentadorDicom).*
2. **Plan antes de modelo, fase por fase.** Nada se modela ni se imprime sin un plan autorizado en `specs/NNN-nombre/`. Lo que se deja para después va a `docs/BACKLOG.md` en el momento, no al final. *Fuente: método del autor.*
3. **Medir antes de decidir.** «Se ve bien» o «parece firme» no cierra nada; cierra un número que coincide con lo esperado (ángulo, separación, giro, error de reproyección) y cómo se midió. *Fuente: método del autor.*
4. **Una sola fuente por cosa.** Cada dato vive en un solo archivo (tabla en `CLAUDE.md`). Los parámetros maestros (tolerancias, grosores, medidas de interfaces) se definen en un único sitio y todas las piezas los leen de ahí. *Fuente: método del autor; entrevista, fase 2.*
5. **Nada toca el anillo del lente.** Las cámaras se sujetan por la carcasa. Ninguna pieza presiona, roza ni rodea con apriete el lente M12; si el lente se mueve, hay que recalibrar. La cámara 2 es especialmente delicada. *Fuente: autor, requisito 4.*
6. **Rigidez: giro relativo entre cámaras muy por debajo de 0.1°.** 0.1° son unos 0.65 mm a 375 mm. Tocar la barra, tirar de un cable o mover la barra entera no debe mover una cámara respecto a la otra. *Fuente: autor, requisito 1.*
7. **Cada configuración es repetible e identificable.** Separación y ángulo se eligen entre posiciones discretas marcadas, se puede volver a la misma otro día, y cada configuración tiene un código grabado en la pieza que también nombra su archivo de configuración. La versión fija a largo plazo es la de pruebas con la posición bloqueada, no otra pieza. *Fuente: autor, requisitos 2 y 3; entrevista, fase 1.*
8. **Nada sin tiempo límite; nada deja el árbol en mal estado.** Todo comando lleva tiempo límite. Ninguna tarea deja archivos a medias, exportaciones huérfanas ni el repo sucio sin decirlo. *Fuente: método del autor.*
9. **Cambiar un principio exige un ADR** en `docs/DECISIONS.md`, autorizado por el autor. *Fuente: método del autor.*
