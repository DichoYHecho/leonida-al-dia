# Fase 1 · Radar de virales de GTA 6 (YouTube)

## Objetivo
Cada día, una lista corta de vídeos de GTA 6 publicados en los últimos 7 días que rinden mucho mejor que lo normal de su canal, para inspirar temas y ganchos (y rellenar `gta/banco_datos.csv` con datos **verificados aparte**).

## Cómo funciona
1. **Descubrir:** `search.list` (type=video, order=viewCount, publishedAfter=hace 7 días) con 3 búsquedas: «GTA 6» con relevanceLanguage=es, «GTA 6» sin idioma, «GTA VI» sin idioma. Máx. 50 resultados cada una. **Máx. 6 búsquedas al día** (≤ 600 unidades).
2. **Datos de los vídeos:** `videos.list` (statistics, contentDetails, snippet) en lotes de 50 (1 unidad por lote).
3. **Lo normal de cada canal:** `channels.list` → lista de subidas; `playlistItems.list` (últimos 50) + `videos.list`. Mediana de vistas de los últimos 30 vídeos con más de 48 h. Guardar en `radar/canales.json` y reutilizar 7 días (ahorra cupo).
4. **Puntuar:** `multiplicador = vistas / mediana_canal`; `vistas_hora = vistas / horas desde publicación`. Formato: short ≤ 180 s, largo ≥ 480 s, el resto «medio».
5. **Filtrar:** multiplicador ≥ 3 y vistas ≥ 10.000 (umbrales en `gta/config.py`: `RADAR_MULT_MIN`, `RADAR_VISTAS_MIN`). Sin directos ni vídeos ya vistos en los 7 días anteriores.
6. **Etiquetar:** 1 llamada de texto a Gemini (flash-lite) con títulos y descripciones → `tema` y `tipo_gancho` (pregunta, dato sorprendente, lista, comparación, contradicción, cuenta atrás, noticia, otro). Prohibido inventar: si no se deduce, «desconocido».
7. **Guardar:** `radar/AAAA-MM-DD.json` y `radar/ultimo.md` (top 10 Shorts y top 10 largos: título, canal, vistas, ×media, duración, enlace, tema, gancho), con commit en la rama `radar-datos`.
8. **Registrar el cupo gastado** al final del informe. Parar si se superan 2.000 unidades en el día.

## Piezas
- `gta/radar.py` y `.github/workflows/radar.yml` (cron diario 06:00 UTC = 07:00 en Madrid en invierno, y lanzamiento a mano).
- Acceso a la API: primero comprobar si `GOOGLE_YT_REFRESH_TOKEN` (y su client id/secret) permite leer datos públicos (ámbito `youtube.readonly` o `youtube`). Si no, Adrià crea una clave de API en el mismo proyecto de Google Cloud y la pega él como secret `YT_API_KEY`. Instrucciones paso a paso, nunca en el chat.
- Airtable: **no** en esta fase. Se decide en la fase 2 si las ideas pasan a «Por Revisar».

## Coste (0 €)
YouTube: < 2.000 de 10.000 unidades/día. GitHub Actions: ~2 min/día ≈ 60 min/mes. Gemini: 1 texto/día.

## Hecho cuando
- [ ] Una ejecución a mano termina bien y deja `radar/ultimo.md` con al menos 5 candidatos.
- [ ] El cupo gastado aparece en el informe y está por debajo de 2.000.
- [ ] El `verificador` comprueba a mano 3 candidatos (vistas y mediana) contra YouTube.
- [ ] La ejecución programada del día siguiente funciona sola.
- [ ] `docs/ESTADO.md` actualizado. Después: esperar «Fase completada».
