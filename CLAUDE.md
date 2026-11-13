# Leónida al Día · instrucciones para Claude Code

Lee este archivo entero antes de hacer nada. Si la tarea es de una fase concreta, lee también su documento en `docs/`.

## Qué es
Canal de contenido automatizado a **0 €** sobre GTA 6 (sale el **19 de noviembre de 2026**) en YouTube (@LeonidaalDiaGTA6), Instagram y TikTok. Dueño: Adrià. GitHub Actions hace el trabajo diario (noticias, datos, guion con Gemini, voz, montaje), Adrià aprueba en Airtable y Buffer publica. Los vídeos largos se suben a mano en YouTube Studio.

## Reglas que no cambian
1. **Todo a 0 €.** Antes de añadir un servicio o subir el uso de uno, comprueba su límite gratuito y apúntalo en `docs/limites.md` (créalo si no existe) con fuente y fecha.
2. **Nunca** pidas claves, tokens ni contraseñas en el chat. Si hace falta un secret nuevo, explica a Adrià cómo pegarlo él en GitHub (Settings → Secrets and variables → Actions), paso a paso y de uno en uno.
3. **Datos reales y verificados, con fuente.** Nada inventado. Si algo solo lo dicen medios, márcalo `[SEGÚN MEDIOS]`. En la duda, no se publica.
4. Español de España, claro, sin tecnicismos. Respuestas breves.
5. **Por fases:** no pases a la siguiente fase hasta que Adrià escriba «Fase completada».
6. Autonomía: no pidas permiso para cada paso. Sí lo necesitas para publicar algo, borrar algo, gastar cupo de voz (10 audios/día) o tocar `main`.
7. Trabaja en ramas, nunca directamente en `main`. Al terminar algo importante, actualiza solo las líneas afectadas de `docs/ESTADO.md`.
8. Vídeos de otros: solo como **referencia de estructura** (gancho, ritmo, orden). Nunca se copia su texto, su audio ni su imagen. Riesgo grave: 3 avisos de derechos de autor cierran el canal y los asociados.

## Reglas de edición de vídeo (siempre, sin que nadie lo pida)
- La voz no se corta al final de las frases y no se oye ruido al final de cada trozo de voz (`montaje.py` ya lo comprueba: salida 3).
- Logos, carteles y transiciones con imagen **quieta**, sin movimiento de cámara.
- Carteles del centro legibles: fondo negro, tamaño y color distintos de los subtítulos, sin superponerse.
- La música cambia cada cierto tiempo.
- Lo que se ve corresponde con lo que se dice (si se nombra a Tommy Vercetti, sale él; juego antiguo → imágenes de ese juego).
- Más vídeo de los juegos (tráileres y gameplays) que fotos. Nunca repetir tomas; descargar material de sobra.
- Si sale una foto, que enseñe algo (caras: Jason, Lucía), no un trozo sin interés.
- Guion y edición naturales y profesionales, que no suenen a IA (ver `docs/reglas_guion.md`).

## Vídeos largos
16:9, 10-14 min, ritmo rápido, guasa suave, capítulos, material que cuadra con lo que se cuenta. Miniatura, título y hashtags al terminar. No se habla de la música del juego, pero sí de que Bad Bunny es locutor de radio dentro del juego. Una rama por vídeo (`vice-city`, `saga`…). `voces.py` y `montaje.py` eligen guion con `GUION`.

## Mapa del repositorio (lo esencial)
- `gta/config.py` — configuración (canal, `ACTIVO`, umbrales).
- `gta/guion.py`, `gta/cuenta_atras.py` — guiones diarios y cuenta atrás.
- `gta/banco_datos.csv` — banco de datos curiosos con fuente (se acaba antes del 19 nov: añadir datos).
- `video_largo/voces.py`, `video_largo/montaje.py` — vídeos largos (`comprobar_guion.py` no está en `main`: va con cada lote de vídeos, p. ej. rama `videos-8-10`).
- `gta/contentid.py` — prueba de Content ID.
- `.github/workflows/` — tareas de GitHub Actions.
- `docs/` — método viral, reglas de guion, fases y estado.
Si algo no coincide con lo que ves en el repositorio, manda el repositorio: corrige este mapa.

## Servicios y límites gratis (comprobados)
- GitHub Actions: 2.000 min/mes (uso ~500 con los dos proyectos).
- Airtable «Panel GTA 6» (`appLYUwqO5EjDfQtX`, tabla Publicaciones): 1.000 llamadas/mes; uso ~550-650. Agrupa cambios en una llamada.
- Buffer: 100 peticiones/15 min, 250/día, 3.000/30 días.
- Gemini: texto 500/día; voz 10/día por modelo (flash-tts y flash-lite-tts).
- YouTube Data API: 10.000 unidades/día por proyecto; `search.list` cuesta 100, las lecturas `*.list` cuestan 1. Subir vídeos por API **no sirve** (proyecto sin auditar).
Secrets ya existentes: `AIRTABLE_TOKEN`, `GEMINI_API_KEY`, `BUFFER_API_KEY`, `GOOGLE_YT_REFRESH_TOKEN` (y los que veas en los workflows).

## Método viral (nuevo, 13 nov 2026)
Adaptación del sistema «detecta lo que funciona → desmonta su estructura → escribe un guion propio → monta → prueba ganchos → aprobación humana». Detalle en `docs/metodo_viral.md`.

| Fase | Qué | Documento | Agente |
|---|---|---|---|
| 1 | Radar de virales de GTA 6 en YouTube | `docs/fase1_radar.md` | `radar-virales` |
| 2 | Desmontar la estructura de los ganadores | `docs/metodo_viral.md` §2 | `desmontador` |
| 3 | Pruebas de ganchos (Reels de prueba, variantes) | `docs/metodo_viral.md` §5 | `guionista` |

## Agentes (`.claude/agents/`)
- `radar-virales` — construye y mantiene el radar (fase 1).
- `desmontador` — saca la estructura de un vídeo ganador (fase 2).
- `guionista` — escribe guiones de Shorts y vídeos largos con `docs/reglas_guion.md`.
- `editor-video` — monta y revisa vídeos con las reglas de edición.
- `verificador` — comprueba datos, fuentes y reglas antes de montar o publicar. Úsalo siempre antes de dar algo por terminado.
