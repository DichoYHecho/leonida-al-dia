# Vídeo 6 · Material para rehacer la imagen (en curso, 14-15 nov 2026)

Revisión aprobada por el usuario el 14 nov: doc «Vídeo 6 · Revisión del guion y la edición» (https://claude.ai/artifact/H6qsXHSzxz9EAYfBniKQiB).
El guion ya está reescrito y subido (video_largo/guion_pol.py, 1.769 palabras, unos 8,7 min de voz). Los planos de guion_pol.py son todavía los antiguos y hay que rehacerlos.

## Lo que NO vale (archive.org o terceros)
Grupos GTA1_1997 (G1_PS, G1_Demo1, G1_Demo2), GTA3_2001 (G3_PS2a/b), SA_2004 (SA_PS2a/b), LCS_2005 (LCS_PS2), Vice_City_2002 (VC02_Trailer3, VC10_Aniv), VC_DE (VCDE_Juego), Historia_GTA y los trozos GTA_15_xx (GTA_15), GTA5_2013 (V_Juego_1..4) y GTA_Online (ON_Juego).
También quedan fuera G3_Aniv (720p), G3_DE (5r2a2o2k) y SA_DE (rr54344t): son comparativas con rótulos y barridos.
Los planos intro_original G1_Demo1_01 y G3_DE_01 hay que cambiarlos.

## Vídeos oficiales de Rockstar
Catálogo sacado con la API pública de rockstargames.com/videos: `graph.rockstargames.com`, operación `VideosList`, sha256 `d43c485f…72c0`, variable `gameId`.
La resolución se comprueba en el CDN: `videos-rockstargames-com.akamaized.net/v4/<id>/flv/en-us-<res>.mp4`.

| Juego | Id | Mejor resolución | Título | ¿Sirve? |
|---|---|---|---|---|
| Bully | totcka8o | 1080p | Anniversary Edition Trailer | Sí: bloques 6 y gancho |
| Bully | kat41srk, as4kct4k | < 1080p | Scholarship Edition Trailer, Valentine's Special | No |
| GTA IV / EFLC | todos | < 1080p | — | No |
| GTA III / Vice City / San Andreas (originales) | a1t1t316, 45r58989, tror41c2, 36cra2or | < 1080p | — | No |
| The Trilogy | 8ta2r546 | 2160p | The Trilogy – The Definitive Edition Trailer | Sí: bloques 2, 3, 4, 5 y 13. Lo usan otros vídeos (VC_Tril): cruzar tramos |
| The Trilogy | 5r2a2o2k, ao1c441c, rr54344t | 2160p | Comparativas | No (rótulos y barridos) |
| GTA V / GTA Online / GTA VI | ver `video_trece_anos/planos_4k.md` | 2160p | — | Sí, sin repetir tramos del vídeo 5 (prefijo K5_) |

## Plan por bloque (aprobado como enfoque: la imagen cuenta la polémica)
- **Gancho:** Bully Anniversary (1080p) + tarjeta «Miami · 2006» + 4K de GTA VI.
- **1 (1997):**
  - Tarjetas propias (Clifford y BMG, la pregunta en los Lores con la cita del Hansard, Brasil 1998).
  - Capturas web a 2560x1440: Game Developer y Killscreen sobre Clifford; Wired de 1998 sobre Brasil; la página de Hansard del 20 may 1997.
- **2 (2001):** Trilogy 4K (Liberty City) + tarjeta con los cambios tras el 11-S.
- **3 (2002-2003):** Trilogy 4K (Vice City), captura de Game Developer (demanda, 2 y 28 ene 2004), foto de Commons de un tribunal de Florida.
- **4 (Hot Coffee):** Trilogy 4K (San Andreas), captura del blog de la ESRB (20 jul 2005), nota de prensa de la FTC (jun 2006), tarjeta «24,5 M$».
- **5 (Australia):** Trilogy 4K (San Andreas) y la ficha de clasificación australiana.
- **6 (Bully):** Bully Anniversary 1080p, capturas de The Register (13 oct 2006) y The Escapist (4 mar 2008).
- **7 (Thompson):** capturas de bit-tech (27 de 31 cargos) y Engadget (inhabilitación), foto de Commons del Tribunal Supremo de Florida, tarjeta de cargos.
- **8 a 12 (GTA V y Online):** 4K oficiales de `planos_4k.md`, tramos nuevos; capturas de NBC/CNBC, Fortune, Fox Business o la petición, Steam o PC Gamer y Game Informer.
- **13 (Trilogy):** Trilogy 4K + captura de NME (disculpa del 19 nov 2021).
- **14 (hackeo):** captura de The Guardian (19 sep 2022) + tarjeta de YouTube al vídeo 5 (https://youtu.be/0wN5lX7CVvc).
- **14b (despidos 2025):** capturas de The Register (6 nov 2025) y Aftermath (10 sep 2026). Sin nombres ni caras de trabajadores.
- **15 (Miami Beach):** captura de WLRN (24 sep 2026) + 4K de GTA VI (Vice City).
- **16 y cierre:** 4K de GTA VI y GTA V, tramos nuevos.

## Pendiente
- **Voces:** 16 voces nuevas: hook, p01, p02, p03, p06, p07, p08, p09, p10, p11, p12, p14, p14b, p15, p16 y cierre. Se pide desde las 9:00 de Madrid (8:00 UTC), con cola_voces.yml o voces_video.yml.
- **Despidos:** antes de publicar, comprobar si ya hay sentencia en el juicio de Glasgow (bloque 14b).
- **Música:** lista de 10-15 pistas libres por estilo (FreePD, Pixabay sin Content ID, Incompetech CC BY) para que el usuario elija.
- **Tarjeta de YouTube:** se pone en Studio, en el bloque 14, apuntando al vídeo 5.
