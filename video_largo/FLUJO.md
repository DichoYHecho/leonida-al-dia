# Flujo de trabajo de los vídeos largos (coste 0 €)

El único límite que obliga a esperar es el cupo diario gratuito de las voces de Gemini. Este orden hace que ese
límite nunca pare el proyecto: siempre hay un vídeo avanzando mientras otro espera voces.

## Orden de cada vídeo

1. **Guion cerrado.** Texto revisado y datos comprobados. Pasa `comprobar_guion.py` sin errores (salvo planos `NUEVO_`).
   A partir de aquí el texto no se toca: cada cambio en un bloque hace que su voz se pida de nuevo y gasta cupo.
2. **A la cola de voces.** Se añade una línea a `.github/cola_voces.txt` (rama `main`): `rama guion`.
   La «Cola diaria de voces» pide cada mañana las voces que falten, en orden, y para cuando se acaba el cupo.
3. **Previa el mismo día, sin esperar voces.** «Montaje del vídeo largo» con `voz_provisional = 1` y
   `forzar_finales = 1`: las voces que falten se ponen con Piper (gratis, sin cupo) y los planos que no existen
   salen como tarjetas «PLANO PENDIENTE». Sirve para revisar ritmo, planos, rótulos y canciones.
4. **Planos y canciones.** Se graban las capturas `NUEVO_` y se cambia su fila en `video_largo/trozos_57.csv`
   (la columna «Vídeo» pasa a la captura real). Las canciones van en la carpeta `canciones` del equipo de montaje.
5. **Montaje final.** Cuando la cola diga que el guion tiene todas sus voces: montaje con `voz_provisional = 0`.

## Mientras un vídeo espera voces

Se adelanta el siguiente: guion, comprobación de datos y planos. Así el cupo de cada mañana siempre tiene trabajo
y nunca hay un día parado.

## Seguridad

- Cada guion monta y publica en su propia rama (`montaje-13a`, `voces-pol`…): nunca en las del vídeo 1.
- La voz provisional va en una copia de la caché (`cache/voz_previa`): nunca se mezcla con las voces de Gemini.
