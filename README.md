# Leónida al Día (GTA 6)

Cuenta de fans de GTA 6 en Instagram, TikTok y YouTube Shorts (@leonidaaldia). Este repositorio prepara
cada día propuestas de vídeo (noticias y datos comprobados, siempre con su fuente), las deja en Airtable
para que las revise y publica las aprobadas con Buffer. Todo a 0 €.

## Cómo funciona (hora de Madrid, horario de invierno)

| Hora | Tarea | Archivo |
|---|---|---|
| 08:00 | Lee las noticias de GTA 6 (Rockstar Newswire, Take-Two, Vandal, 3DJuegos, VGC y Push Square), Gemini elige hasta 3 y escribe el guion solo con lo que dice la fuente; prepara también los datos del banco que falten (siempre 2 pendientes). Cada propuesta va con su vídeo | `gta/preparar.py` |
| 12:30 | Repesca: rehace los vídeos que he cambiado en Airtable | `gta/repesca.py` |
| 14:00 y 21:00 (y 18:00 del 16 al 22 nov) | Publica la aprobada: la noticia más reciente o, si no hay, el dato más antiguo | `gta/publicar.py` |
| 19:00 | Segunda lectura de noticias (hasta 2) | `gta/preparar.py` |
| 40 min después de publicar | Comprueba en Buffer que salió en las 3 redes | `gta/comprobar.py` |

- **Voz:** Gemini «Mako», estilo «Promote» (un audio por vídeo; gratis hasta 10 al día). Reserva: Piper «sharvard» (CC BY 3.0, se cita).
- **Subtítulos:** sincronizados con Whisper; si falla, por las pausas de la voz.
- **Imágenes:** solo capturas oficiales de rockstargames.com/VI/media, revisadas una a una (`gta/capturas.csv`).
- **Música:** synthwave hecha con código.
- Las ejecuciones programadas solo funcionan con la variable del repositorio `ACTIVO` = `si`.

## Secrets (los pego yo en Settings › Secrets and variables › Actions)

- `AIRTABLE_TOKEN`: token de la base «Panel GTA 6» (cuenta de adria.sanandreas).
- `GEMINI_API_KEY`: clave de AI Studio del proyecto GTA.
- `BUFFER_API_KEY`: clave de la API de la segunda cuenta de Buffer.

## Reglas de contenido

Todo con su fuente; «Rockstar confirma» solo si es oficial; nada de filtraciones, rumores como hechos ni
destripes; sin enlaces para comprar; cuenta de fans sin relación con Rockstar Games; etiqueta de IA.
