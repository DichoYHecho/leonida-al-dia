# Método viral · Leónida al Día

Inspirado en un sistema visto en Instagram (13 nov 2026). Lo adaptamos a lo que ya tenemos y a 0 €. Una persona (Adrià) aprueba siempre antes de publicar.

## Flujo
1. **Radar** (fase 1): cada mañana, detectar en YouTube los vídeos de GTA 6 que rinden muy por encima de lo normal de su canal. Salida: `radar/AAAA-MM-DD.json` y `radar/ultimo.md`.
2. **Desmontar** (fase 2): de los mejores, sacar la **estructura**, no el contenido: tipo de gancho, segundos que dura, bloques (gancho → contexto → datos → prueba → cierre), palabras por segundo, cierre o pregunta final. Fuente: título, descripción, duración y subtítulos públicos (sin descargar el vídeo). Salida: `radar/estructuras/<id>.json`.
3. **Guion propio**: `guionista` aplica `docs/reglas_guion.md` y las estructuras ganadoras a **nuestros** datos verificados (`gta/banco_datos.csv`, noticias con fuente). Nunca se reescribe el texto de otro.
4. **Montaje**: voz Mako (Gemini), subtítulos con Whisper, montaje con las reglas de `CLAUDE.md`. No usamos voz clonada.
5. **Pruebas de ganchos** (fase 3): 2 ganchos por guion. Instagram: Reels de prueba (solo para no seguidores, hasta 72 h); requisito de seguidores sin confirmar (200 o 1.000 según la fuente): comprobar en la app antes. Si Buffer no lo permite, se hace a mano. Lo que gane se apunta en `docs/reglas_guion.md` §«Aprendido».
6. **Aprobar y publicar**: como ahora (Airtable → Buffer). Nada sale sin aprobación.

## Lo que NO hacemos
- Revisar perfiles ajenos de Instagram o TikTok con robots (no hay vía gratuita y oficial).
- Copiar texto, audio o imágenes de otros creadores.
- Titulares engañosos, bots, compra de seguidores.

## Formato de un candidato del radar
```json
{"id":"…","url":"https://youtu.be/…","titulo":"…","canal":"…","canal_id":"…","publicado":"ISO","duracion_s":0,
 "formato":"short|largo|medio","vistas":0,"mediana_canal":0,"multiplicador":0.0,"vistas_hora":0.0,
 "idioma":"es|en|otro","tema":"…","tipo_gancho":"…"}
```
`tema` y `tipo_gancho` los pone Gemini **solo** a partir del título y la descripción; si no está claro, `"desconocido"`.

## Estado
- 13 nov: método definido. Fase 1 en marcha (rama `radar`).
