# Revisión de calidad: vídeo largo 5, «¿Por qué GTA VI ha tardado 13 años?»

Revisado el 14 nov 2026 sobre el vídeo final de la release `montaje-13a-alta-calidad`. El archivo se actualizó el 13 nov a las 12:25 UTC desde la ejecución 43419919083 (GUION=guion_13a). Son 8:55, 1920x1080 a 29,94 fps, H.264 a 6,7 Mb/s, AAC a 192 kb/s y 459 MB.

Cómo se ha medido:
- 1070 fotogramas (2 por segundo) y 176 cortes de plano detectados con `select=gt(scene,0.25)`.
- En cada fotograma se han medido las columnas y filas negras o borrosas de los bordes y la nitidez (laplaciano).
- Tiras de fotogramas a 0,25 s alrededor de las cartelas, los subtítulos y el final.
- faster-whisper `small` (cpu int8) sobre el audio completo, comparado con `guion_13a.py`.
- Volumen, tono (f0) y centroide espectral de cada bloque, tanto en la mezcla final como en los mp3 de la rama `voces-13a`.
- El plan de planos se ha reconstruido con la misma lógica de `montaje.py` (expandir_grupos y planificar_anclado) y las tablas de trozos. Los nombres de los trozos automáticos (V_Juego_*, ON_Juego_*, GTA_15_*, MI_*) pueden no coincidir uno a uno con los del montaje real, porque las tablas `trozos_auto*.csv` que se usaron pueden ser distintas de las locales. El grupo, la fuente y el minuto sí están comprobados a ojo en los fotogramas.

Fotogramas de ejemplo en `video_trece_anos/revision_fotogramas/` (10 jpg a 1920x1080, numerados como abajo).

---

## 1. Los 10 problemas más graves

1. **Un tercio del vídeo es material de 360p y 480p metido en un marco borroso.** Unos 175 s de 535 (33 %) salen de cuatro fuentes:
   - partidas de GTA V y GTA Online de archive.org a 640x360 (`V_Juego_*`, `ON_Juego_*`);
   - un vídeo de YouTube copiado en archive.org a 854x480 (`GTA_15`, «GTA 15th Anniversary»);
   - otra copia de YouTube a 854x480 (`VCDE_Juego`).

   Todas tienen menos de 600 px de alto, así que `cortar()` las mete en el MARCO del 82 % sobre fondo borroso. Por eso el tamaño de la imagen cambia cada pocos segundos. Otros 160 s salen de fuentes a 1080p reescaladas, y solo 119 s (22 %) son 4K nativo. Fotos 01, 04 y 06.

2. **Texto y marcas de otros en pantalla.**
   - Subtítulos del juego en inglés quemados: 0:14 («Hey, I need a cab…»), 0:28-0:34, 0:54, 2:20-2:22.
   - Fichas en inglés del vídeo de terceros «GTA 15th Anniversary» («October 1997», «25th October 2004», «27th October 2002»…): 0:17-0:25, 3:44, 4:04, 4:24-4:26, 4:34, 4:52-5:03.
   - Marca de agua **«mrmediagame»** de otro canal y banner «Grand Theft Auto Mission Videos / gta-series.com»: 3:46-4:05 (foto 06).
   - Rótulos «original» y «the definitive edition» de un vídeo comparativo ajeno: 5:04-5:20.
   - Interfaz de GTA Online en alemán y nombres de jugadores: 1:24, 1:36-1:38, 2:08.
   - Anuncio «WN Talents» dentro de la captura de Cfx: 2:10-2:13 (foto 05).
   - Textos promocionales en inglés: «ACCESS TO THE CAREER BUILDER» (2:34), «PRE-ORDER NOW» (7:03-7:07 y 7:36-7:38, ya caducado si el vídeo sale tras el lanzamiento), «ROCKSTAR GAMES PRESENTS» (6:42 y 7:46).

3. **La imagen no cuenta lo que dice la voz.**
   - GTA Advance y GTA 2 mientras se habla de Red Dead Online: 3:44-4:05, rótulo «27 NOV 2018 BETA» sobre GTA 2 (foto 06).
   - Ficha de Vice City de 2002 bajo «ÚLTIMO DÍA · 11 MAR 2020»: 4:24 (foto 07).
   - Ficha de GTA London 1969 bajo Ruffian: 4:52-5:00.
   - GTA VI mientras se habla de GTA V (0:38), de GTA Plus (2:42-3:07) o de RDR2 (3:24-3:30: una tele dentro de un piso de GTA VI; 3:36-3:42: peleas en una escalera).
   - El anuncio cómico de la hamburguesa bajo «chantaje y fraude… internamiento hospitalario»: 6:08-6:13.
   - Un hombre tirado en el suelo bajo «¿Fue una espera justa?»: 8:47-8:52.

4. **Las capturas web y las tarjetas propias están en pequeño sobre negro.** Las 16 imágenes NUEVO_ son de 1920x1080, pero `cortar()` las reduce a 1600x880 y les pone bordes negros: 73 s en total. Además:
   - el título del bloque (arriba a la izquierda) pisa la barra de menús de la captura: 2:24, 2:38, 3:48, 4:12, 6:04, 7:10, 7:32;
   - el rótulo central tapa el titular que se quiere enseñar: 0:04, 1:46, 2:12, 7:10, 8:18;
   - la nota de Take-Two sale cortada arriba (1:08) y a la izquierda (7:32) (foto 03).

5. **Hay franjas negras dentro del propio plano (letterbox).** Varias fuentes oficiales son 2,2:1 dentro de un 16:9: el tráiler de RDR2, el de GTA Online para PC (`V_PS5`), el tráiler 2 y el de lanzamiento. El montaje las reescala sin recortar las bandas, así que quedan unos 64 px negros arriba y abajo: 0:35-0:37, 0:44, 2:19, 2:33, 3:10-3:24, 3:30-3:35, 6:49-7:03, 7:29-7:49, 7:52 y 8:00. A esto se suman:
   - el cartel ESRB en 4:3 sobre negro (0:41,5-0:44,5, el «4:3» que se ve en 0:41; foto 02);
   - el logo de GTA Online sobre negro (0:44-0:47);
   - un plano vertical con bordes borrosos dentro del tráiler 1 (6:24,5-6:25,5).

6. **Los rótulos tapan lo importante y chocan con otros textos.** Es una caja negra fija en el centro exacto (y=440) con Montserrat Black de 84/52 px en amarillo y rosa.
   - Se monta encima de otros textos: la tarjeta «El acceso a Rockstar» (5:34-5:37, foto 08), el logo de GTA VI (0:02, 6:20, 7:42) y «NOVEMBER 19, 2026» (7:04, foto 10).
   - Se ancla mal: «MISMO MAPA» sale en 2:24, antes que «2014 · PS4», porque se engancha al primer «mismo» del texto («el mismo juego»).

7. **El vídeo va desfasado unos 0,5 s respecto a rótulos y cartelas.**
   - En 3:08,2-3:09,0, 4:05,8-4:06,2 y 6:23,0-6:23,8 hay negro con el título del bloque anterior todavía puesto.
   - Después, la cartela («2010 · EL OTRO GRAN PROYECTO», «2020», «2023») sigue encima del primer plano del bloque nuevo: 3:09,75-3:10,1, 4:07,25-4:07,6 y 6:24,5-6:25,1 (foto 09).
   - En 4:07,25 se cuela un fotograma suelto de otro plano (una barra de pesas).
   - En 0:26 no hay desfase, así que se va acumulando con los cortes: `-t` por plano y concat `-c copy` redondean a fotogramas enteros.

8. **Se repiten planos dentro del propio vídeo.**
   - `T1_Musica_Petty` sale dos veces (6:25 y 6:43) y `T1_Neones` dos veces seguidas (6:38-6:40).
   - `Mirada_Skyline_Noche` sale dos veces en el cierre.
   - La escena de los dos hombres en la azotea sale tres veces (5:24, 5:46 y 8:26).
   - El coche por la avenida soleada (3:04 y 8:04), la carrera de coches (5:50 y 8:12) y la playa aérea (5:22 y 6:40) salen dos veces cada uno.
   - El logo de GTA VI sale en 0:00, 6:14 y 7:42.
   - De 0:55 a 2:17 casi todo es **el mismo coche blanco por Los Santos nevado**: 24 planos de 3 s de la misma partida.
   - `comprobar_repetidos()` solo compara nombres. `MI_*` (Mirada a 1080p, `trozos_auto_jl.csv`) y `Mirada_*` (Mirada a 2160p, `trozos.csv`) son el mismo vídeo con otro nombre, y el control no los ve.

9. **Casi todo ya ha salido en otros vídeos del canal.** De los 171 trozos del guion expandido, 142 (83 %) ya estaban en los vídeos 1-4, 6 o 7 con el mismo nombre o un tramo solapado. Solo 8 son vídeo nuevo de verdad, y 16 son capturas NUEVO_. En tiempo de pantalla son 413 de 534 s repetidos y 29 s nuevos. Detalle en la sección 4.

10. **El sonido se oye casero.**
    - La música está hecha con numpy (`musica_era`: onda cuadrada «chiptune» para la época de GTA V, breakbeat, hiphop y synthwave) y bajo la voz va a 0,085 de ganancia. Queda unos 20-25 dB por debajo de la voz, prácticamente inaudible, y en cada pausa de 0,7-0,9 s entre frases sube a 0,30: se oye un bombeo constante.
    - El volumen de la voz varía 5 dB entre bloques (de −21,7 dB en p03 a −16,7 dB en p14), porque cada bloque se normaliza por pico y no por sonoridad.
    - El tono cambia entre bloques: p07 a 196 Hz frente a 136-176 Hz en el resto. Es el salto de modelo ya conocido, más diferencias dentro del propio modelo lite.
    - El final congela el último fotograma más de 2 s (8:53-8:55, por `tpad=stop_mode=clone`) y el vídeo termina sin pantalla final.

---

## 2. Tabla de planos (minuto · plano · problema · sustituto)

Leyenda:
- **MARCO**: fuente de menos de 600 px en el marco del 82 % sobre fondo borroso.
- **PAD**: imagen reducida a 1600x880 sobre negro.
- **LB**: franjas negras del letterbox de la fuente.
- **REP-n**: n apariciones previas del trozo (o de su tramo) en los bloques de los vídeos 1-4, 6 y 7. Los tramos de Mirada que se citan como libres no los ha usado nadie, pero su contenido está sin revisar.
- **4K ✓**: resolución comprobada con ffmpeg sobre la URL oficial.

| Minuto | Bloque · plano | Problema | Sustituto concreto (resolución comprobada) |
|---|---|---|---|
| 0:00-0:03 | hook · Mirada_Logo | Logo de GTA VI con el rótulo «SEP 2022 → NOV 2026» encima a la vez (0:02); REP-6 | Fondo negro solo con la fecha animada; si se quiere logo: Pre-Load Now 22-24 s (logo sobre luces, 3840x2160 ✓, `…/VI/downloads/videos/GTAVI_Pre-Load_Now/GTAVI_Pre-Load_Now.mp4`) |
| 0:03-0:07 | hook · NUEVO_Filtracion_Foro | PAD; rótulo tapa la cabecera; captura de PC Gamer con menús | Volver a capturar a 2560x1440 (Playwright msedge, viewport 2560x1440, deviceScaleFactor 1), recortada al titular y con zoom lento; rótulo al lado, no encima |
| 0:07-0:08 | hook · T1_Noche_Aerea | REP-7 | Tráiler 1 libre 63-66 s (Lucía en el coche) o 4,9-8 s (atardecer tras la alambrada); 3840x2160 ✓ |
| 0:08-0:09, 0:13-0:17 | hook · V_Juego_* (GTA5_2013) | MARCO 360p; subtítulos ingleses quemados; REP-4 | Tráiler oficial de GTA V/Online para PC (`ks18e7s9`, 3840x2160 ✓, `https://videos-rockstargames-com.akamaized.net/v4/ks18e7s9/flv/en-us-2160p.mp4`) 9,0-11,9 s (helicóptero y Los Santos al atardecer), recortando el letterbox |
| 0:09-0:13 | hook · NUEVO_Comunicado_Rockstar | PAD; captura de Game Developer con imagen de un tercero | Recaptura a 2560x1440 del tuit o comunicado oficial (texto), sin fotos de terceros |
| 0:17-0:25 | hook · GTA_15_01 | MARCO 480p; ficha inglesa «October 1997» (GTA 1) que no tiene nada que ver; 8,7 s quieto; vídeo de YouTube de terceros; REP-3 | Tráiler 1 44-50 s libre (tienda con cámara de seguridad «FRONT DOOR») o una cifra animada «13 AÑOS» sobre la portada oficial (Cover Art Landscape 15-20 s, 3840x2160 ✓) |
| 0:25,7-0:27,3 | p01 · cartela | Negro plano con texto; bien sincronizada aquí | Ver sección 5 (cartela sobre fotograma difuminado) |
| 0:27-0:35, 0:39-0:41, 0:46-0:55 | p01 · V_Juego_1/2/4 (GTA5_2013, 7 trozos) | MARCO 360p; subtítulos del juego en inglés («overwhelmed by the place…»); REP-3 cada uno | `ks18e7s9` 4K: 16-17 s (atraco), 17-18 s (coches de policía), 18-19 s (moteros, antes del texto). Para «Michael / Franklin / Trevor»: no hay 4K oficial verificado de GTA V 2013 en el CDN; mejor una tarjeta con los tres nombres sobre una captura nueva de Rockstar Newswire de GTA V a 2560x1440 |
| 0:35-0:37 | p01 · V_PS5 (helicóptero) | LB de 64 px arriba y abajo; fuente a 1080p | El mismo plano de la URL `…/en-us-2160p.mp4` (3840x2160 ✓), recortando las bandas |
| 0:37,8-0:39,4 | p01 · Lanz_Paseo | Jason y Lucía (GTA VI) mientras se habla de GTA V; REP-9 | Quitarlo: en p01 nada de GTA VI |
| 0:41,5-0:44,5 | p01 · V_PS5_01 (ESRB) | Cartel ESRB 4:3 sobre negro: es el «4:3 en 0:41» | Quitar (los segundos 0-3 de `ks18e7s9` son el cartel; empezar en 9 s) |
| 0:44,5-0:47,5 | p01 · V_PS5 (logo GTA Online) | Logo pequeño sobre negro; LB | Quitar o sustituir por la cifra «230 M» en grande sobre `ks18e7s9` 10-11 s |
| 0:55-1:30 | p02 · ON_Juego_* (11 trozos, GTA_Online) | MARCO 360p; siempre el mismo coche blanco en la nieve; interfaz en alemán y nombres de jugadores; REP-3 casi todos | `ks18e7s9` 4K: 23-24 s (coche verde de noche), 28-30 s (club nocturno). Para las cifras de Take-Two: gráfico propio animado (barras +16 % y 78 %) sobre un fondo desenfocado del tráiler 1 libre 4,9-8 s (atardecer) |
| 1:07-1:11 | p02 · NUEVO_Cuentas_TakeTwo | PAD; texto cortado arriba; el título del bloque pisa el texto | Recaptura a 2560x1440 de la nota de Business Wire (URL en edicion.md), con el párrafo del 78 % resaltado (subrayado animado), sin rótulo encima |
| 1:30-2:17 | p03 · ON_Juego_* (13 trozos) | Igual que p02; 47 s de nieve; subtítulo superpuesto en 1:56 | Material oficial de rol no hay; usar Twitch (recaptura 2560x1440), el logo de Twitch de Commons (`File:Twitch_logo_2019.svg`, dominio público, SVG escalable) y `ks18e7s9` 16-19 s |
| 1:44,6-1:48,6 | p03 · NUEVO_Twitch_Captura | PAD; el rótulo «TWITCH» tapa «GRAND THEFT AUTO V» | Recaptura a 2560x1440 de twitchtracker con zoom a la cifra; rótulo abajo a la izquierda |
| 2:09,8-2:13,8 | p03 · NUEVO_Cfx_Comunicado | PAD; anuncio «WN Talents» en la captura; rótulo encima del titular | Recapturar sin anuncios (Playwright con bloqueo de anuncios o recortando solo el titular) |
| 2:14-2:19 | p03 · MI_57 (GTA6_Mirada) | Mirada a 1080p (la URL 2160p existe); REP-3 | Mismo tramo de `rk721912/flv/es-es-2160p.mp4` (3840x2160 ✓) |
| 2:19-2:24 | p04 · V_PS5_01 / V_Juego_4_09 | LB y MARCO; subtítulos ingleses («You met him at our internal rendition site») | `ks18e7s9` 4K 9-11 s (Los Santos), no repetido en este vídeo |
| 2:24-2:28 | p04 · NUEVO_Reediciones_Logos | PAD; banner «PRE-LOAD NOW» de la web de Rockstar; el título pisa el menú; rótulo «MISMO MAPA» antes de tiempo | Recapturar solo la carátula; o dos carátulas oficiales (PS4 2014 / PS5 2022) en composición propia a 2560x1440 |
| 2:28-2:36 | p04 · V_Juego / T1_Autopista / V_PS5 | MARCO; «ACCESS TO THE CAREER BUILDER» en 2:34 | `ks18e7s9` 4K 17-18 s |
| 2:36,5-2:40,6 | p05 · NUEVO_GTAPlus_Captura | PAD; banner PRE-LOAD; el título pisa el menú | Recaptura a 2560x1440 del artículo de Newswire de GTA+ |
| 2:41-3:08 | p05 · MI_116/53/106/17/69 (Mirada 1080p) | GTA VI mientras se explica GTA Plus; 6 s por plano; REP-1 | Si se mantiene GTA VI: la misma escena en 2160p; mejor un gráfico «cuota mensual» sobre el tráiler 2 libre 66-81 s (Lucía en la valla, Jason en la gasolinera; 3840x2160 ✓, LB) |
| 3:08,2-3:10,1 | p06 · cartela | Negro sin texto 0,7 s; luego la cartela encima del primer plano (desfase) | Ver sección 5 |
| 3:10-3:35 | p06 · NUEVO_RDR2_* y RDR2_01-04 (`6c8k48rr`) | Fuente a 1080p; LB 2,2:1; REP-1 en V4 | La misma URL en 2160p: `https://videos-rockstargames-com.akamaized.net/v4/6c8k48rr/flv/en-us-2160p.mp4` (3840x2160 ✓, 60 s). Tramos libres en el canal: 3,8-10 s (campamento), 13-18 s (banco y llanura con tren), 29-35,8 s (caballos y hoguera), 47,4-50 s (Dutch de noche). Recortar las bandas |
| 3:24-3:30 | p06 · MI_23 | Una tele en un piso de GTA VI mientras se habla del desarrollo de RDR2 | RDR2 2160p 29-33 s |
| 3:30-3:42 | p06 · MI_129 / MI_44 | GTA VI con violencia (escalera) bajo la cita de Dan Houser | Foto de Rockstar North de Commons: `File:20231022_Rockstar_North.jpg` (3834x2324, CC0) con zoom lento |
| 3:42-3:48, 3:52-4:05 | p07 · GTA_15_06/16/30/08/29/10/22 | MARCO 480p; GTA Advance y GTA 2; marca «mrmediagame»; fichas en inglés; nada que ver con Red Dead Online | Recaptura a 2560x1440 de la página de Red Dead Online en rockstargames.com, con la fecha 27 NOV 2018 animada, más RDR2 2160p 29-35,8 s (campamento y caballos). No he encontrado ningún vídeo oficial de RDO verificado (ver sección E) |
| 3:48-3:52 | p07 · NUEVO_RDO_Captura | PAD; el título pisa el menú; banner PRE-LOAD | Recaptura a 2560x1440 |
| 4:05,8-4:07,6 | p08 · cartela | Desfase y fotograma suelto en 4:07,25 | Ver sección 5 |
| 4:07-4:11 | p08 · Mirada_Mar_Atardecer | REP-8 (V1 lo usa dos veces) | Mirada 2160p libre 820-840 s o 880-917 s |
| 4:11-4:15 | p08 · NUEVO_Houser_Captura | PAD; página de GamesRadar casi en blanco con el titular pequeño | Recaptura a 2560x1440 recortada al titular; o la foto de Commons `File:Sam_Houser_and_Dan_Houser.png` (1536x2048, CC BY-SA 4.0), en panel lateral porque es vertical |
| 4:15-4:26, 4:30-4:35 | p08 · GTA_15_09/28/23/27/15/24 | MARCO 480p; GTA 1 y GTA 2 pixelados; «ÚLTIMO DÍA» sobre la ficha de Vice City 2002 | Fichas propias con fecha (FEB 2020 · 11 MAR 2020 · 2021 · JUN 2023) sobre Mirada 2160p desenfocada; o `File:20231022_Rockstar_North.jpg` (CC0) |
| 4:26-4:30 | p08 · NUEVO_Absurd_Logo | PAD; página casi en blanco | Logo en grande y centrado, compuesto a 2560x1440 |
| 4:36-4:38 | p09 · T1_Lancha_Rapida / GTA_15_07 | REP-5 / MARCO | Tráiler 1 24-26 s se usa mucho; mejor Commons `File:Dundee_Waterfront_Redevelopment_Feb_2018_a_-_V&A_Near_Completion.jpg` (4928x2372, CC BY-SA 4.0) |
| 4:38-4:42 | p09 · NUEVO_Ruffian_Captura | PAD; página en blanco | Recaptura a 2560x1440 de la nota de Business Wire (edicion.md) recortada |
| 4:42-4:45 | p09 · Mirada_Skyline_Azotea | REP-3 | Mirada 2160p libre 804-814 s |
| 4:45-5:03 | p09 · GTA_15_26/19/12/04/18/03 | MARCO 480p; ficha «29th April 1999 / GTA London»; negro de la fuente en 4:54 | Foto de Dundee (arriba) + recaptura de la web de Rockstar Dundee si existe; tráiler 2 libre 138-147 s (lancha en los manglares) |
| 5:04-5:21 | p10 · G3_DE_02/04, VCDE_Juego_04/13/15, SA_DE_03 | VCDE a 480p de un vídeo de YouTube con rótulos «original»; G3/SA a 1080p | Tráileres oficiales de The Trilogy en 2160p (3840x2160 ✓): `…/v4/8ta2r546/flv/en-us-2160p.mp4` (58 s; tren en Liberty City 12 s, Vice City 18 s, Vinewood 21 s, casinos 24 s), `…/v4/5r2a2o2k/flv/en-us-2160p.mp4` (GTA III, libre 0-10 s y 31-42 s), `…/v4/rr54344t/flv/en-us-2160p.mp4` (San Andreas, libre 0-11 s y 17,7-30,7 s) |
| 5:22-5:24 | p11 · T1_Playa_Aerea | REP-6; repetido en 6:40 | Tráiler 1 12-14 s (motos de agua, se usa menos) o quitarlo |
| 5:24-5:30 | p11 · MI_60 | Azotea (repetida en 5:46 y 8:26) | Mirada 2160p libre 880-917 s |
| 5:33,9-5:37,9 | p11 · NUEVO_Texto_Hechos | Tarjeta propia en PAD; el rótulo «HOTEL · FIRE STICK» encima de su propio titular; la cabecera choca con el título del bloque | Hacer la tarjeta en ASS a 2560x1440 (no PNG), y sin rótulo encima |
| 5:38-5:46 | p11 · MI_55 / MI_132 | Mirada a 1080p | 2160p |
| 5:46-6:02 | p12 · MI_02/68/59/121 | Carrera con «LAP 9/1» cortado a la derecha (5:50); azotea otra vez | Commons `File:London_Southwark_Crown_Court_(50604622932).jpg` (4512x2708, CC BY 2.0), fachada del tribunal donde se juzgó el caso |
| 6:02-6:06 | p12 · NUEVO_Juicio_Southwark | PAD; página de TechRadar casi en blanco | La foto de Southwark de arriba + titular en ASS |
| 6:06-6:23 | p12 · MI_51 | Un solo plano de 16,6 s (el trozo es de 6 s: `planificar` alarga el último y se ve lo que sigue: hamburguesa y logo); el rótulo «5 MILLONES $» encima del logo | Máximo 6 s por plano; para rellenar, la foto de Southwark con otro encuadre y la fecha «DIC 2023 · CONDENA» en ASS (el Old Bailey de Commons no es el tribunal del caso: no usarlo) |
| 6:23-6:25 | p13 · cartela | Desfase | Ver sección 5 |
| 6:25-6:30 y 6:43-6:48 | p13 · T1_Musica_Petty (×2) | El mismo plano de 5 s dos veces en 18 s (anclado en «petty» y además intro_original) | Quitar el ancla `petty` → `T1_Musica_Petty`; para «Tom Petty» usar tráiler 1 libre 41-51 s |
| 6:38-6:40 | p13 · T1_Neones (×2) | El mismo trozo seguido | Tráiler 1 libre 62-72 s (Lucía en el coche, moteros) |
| 6:42 | p13 · Mirada (créditos) | «ROCKSTAR GAMES PRESENTS» en inglés | Elegir otro segundo |
| 6:49-7:03 | p14 · T2_* / Lanz_Moto_Salto / T2_15 | LB 64 px; REP-3 a 8 | Tráiler 2 libre (3840x2160 ✓): 0-6 s no (negro y logo), 45-52 s (gasolinera y coche de noche), 66-81 s, 85-92 s, 105-111 s; recortar las bandas |
| 7:03-7:08 | p14 · VL_Fecha | «NOVEMBER 19, 2026 PRE-ORDER NOW» en inglés + rótulo «RETRASO 19 NOV 2026» encima (foto 10); REP-5 | Fecha propia en grande en ASS; el «pre-order» ya no tiene sentido tras el lanzamiento |
| 7:08,5-7:12,5 | p15 · NUEVO_Schreier_Bluesky | PAD; es GamesRadar, no Bluesky; el rótulo tapa la cita | Recaptura a 2560x1440 del post de Bluesky (sin datos de otros usuarios) |
| 7:12-7:29 | p15 · MI_92 / MI_37 | 1080p; MI_37 alargado 9,6 s | 2160p, máximo 6 s |
| 7:29-7:49 | p16 · LZ_11/04/02/10 | LB; logo de GTA VI con el rótulo encima (7:42); «ROCKSTAR GAMES PRESENTS» (7:46) | Tráiler de lanzamiento libre (3840x2160 ✓): 27,8-40,5 s (Jason y Lucía en el coche, cámara acorazada, avioneta), 42-47 s |
| 7:30,8-7:34,8 | p16 · NUEVO_Zelnick_Captura | PAD; texto cortado a la izquierda | Commons `File:Strauss_Zelnick,_2015_(16339090774).jpg` (1368x2048, CC BY 2.0) en panel lateral + cita en ASS |
| 7:36-7:38 | p16 · Mirada / VL_Fecha | Otra vez «PRE-ORDER NOW» con ESRB y logos de consola | Quitar |
| 7:52-8:31 | p17 · T2_Casa_Aerea, MI_01, T2_Gimnasio_Playa, Mirada_Autopista_2 (=3:04), Mirada_Carrera (=5:50), MI_131 | Repetidos dentro del vídeo; LB en T2 | Cover Art Landscape 8-14 s (el VI animado, 3840x2160 ✓) para «19 NOV 2026»; capturas oficiales de `GTAVI_Screenshots.zip` (3840x2160 ✓, carpetas Places/Vice City, Leonida Keys, Port Gellhorn…) con zoom lento |
| 8:17-8:21 | p17 · NUEVO_VGD_Captura | PAD | Recaptura a 2560x1440 de take2games.com/ir |
| 8:22-8:25 | p17 · Mirada (directo con chat) | Chat en inglés lleno de texto | Otro tramo libre de Mirada 2160p (330-365 s) |
| 8:32-8:55 | cierre · VL_Atardecer_Final, Mirada_Skyline_Noche (×2), VL_Lancha_Pareja, VL_Interior_1, Mirada_Kayak, Mirada_Calles_2 | REP-5 a 11; Skyline repetido; pelea bajo «¿Fue una espera justa?»; el último fotograma congelado 2 s | Capturas oficiales 4K de Jason y Lucía (`People/Jason and Lucia/*.jpg`, 3840x2160 ✓) + pantalla final de 10-20 s para las tarjetas de YouTube |

Fuentes descartadas: todo lo que tiene menos de 1080p (`V_Juego_*` y `ON_Juego_*` a 640x360 ✓, `GTA_15` a 854x480 ✓, `VCDE_Juego` a 854x480 ✓). `GTA_15` y `VCDE_Juego` además son copias de vídeos de YouTube de terceros en archive.org: no hay que usarlas ni en este vídeo ni en los siguientes.

---

## 3. Voz por bloque

Las palabras mal dichas son lo que oye Whisper `small`: hay que confirmarlas a oído antes de regenerar. Los valores de «Mezcla» están medidos en el vídeo final: nivel medio de las tramas con voz, en dB, con la música debajo. Los de «mp3» están medidos en la rama `voces-13a`. Ojo: **el p08 de la rama ya es otro**, regenerado hoy con lite (38,8 s); el del vídeo es el antiguo de flash.

| Bloque | Minuto | Modelo | Mezcla (dB) | f0 mp3 | Centroide mp3 | Palabras/s | Observaciones |
|---|---|---|---|---|---|---|---|
| hook | 0:00-0:25 | lite | −20,4 | 171 Hz | 1457 Hz | 3,1 | Pausas de 0,6-0,8 s bien puestas |
| p01 | 0:27-0:55 | lite | −20,4 | 168 | 1533 | 3,2 | «prisa» se oye «brisa» (0:49,8) |
| p02 | 0:56-1:30 | lite | −19,4 | 162 | 1155 | **4,2** | El más rápido; «pero sí publica» → «pero así publica» (1:08,8); «sigue dando dinero» → «sigue tanto dinero» (1:27,6) |
| p03 | 1:31-2:19 | lite | **−21,7** | 155 | 1307 | 3,3 | El más bajo; pausa de **1,06 s** en 1:53,2; «Cfx.re» → «se ficere» (2:10,7) |
| p04 | 2:20-2:36 | lite | −19,0 | **136** | 1429 | 3,9 | Tono más grave que el resto |
| p05 | 2:37-3:08 | **flash** | −19,6 | 157 | 1477 | 3,5 | Cambio de timbre al entrar (2:37) |
| p06 | 3:10-3:42 | **flash** | −19,4 | 154 | 1273 | 3,7 | «Dead» → «de», «a IGN» se pierde |
| p07 | 3:43-4:05 | **flash** | −20,1 | **196** | 1392 | 3,7 | **Tono un 20 % más agudo** que la media: el salto más claro |
| p08 | 4:08-4:35 | **flash** (en el vídeo) | −19,5 | (el mp3 actual es otro) | — | 3,8 | Whisper del montaje oyó «Jarroxdar» por «Rockstar»; el mío oye bien «al frente de Rockstar» |
| p09 | 4:36-5:03 | lite | −18,4 | **139** | 1256 | 3,3 | «Liddon» → «Laydon» (4:50,8) |
| p10 | 5:04-5:22 | **flash** | −17,8 | 159 | 1487 | **2,9** | «Vice City» suena «By City» (5:10,5); lento |
| p11 | 5:23-5:46 | **flash** | −19,9 | 168 | 1253 | 3,7 | «Kurtaj» → «Kurtis» (5:28,6) |
| p12 | 5:47-6:22 | lite | −20,0 | 163 | 1216 | 2,9 | Muchas pausas largas: 0,8-0,96 s en 5:56,6, 6:00,7, 6:08,1, 6:16,7; «Seguirá en» → «Seguirán» (6:13) |
| p13 | 6:30-6:49 | lite | −17,3 | 163 | 1331 | 3,3 | Suena 3 dB por encima de p12 |
| p14 | 6:50-7:07 | lite | **−16,7** | 176 | 1341 | 3,5 | El más alto: **5 dB más que p03** |
| p15 | 7:08-7:28 | lite | −20,6 | 151 | 1480 | 3,5 | Baja 4 dB de golpe respecto a p14 |
| p16 | 7:29-7:51 | lite | −18,6 | 161 | 1286 | 4,0 | «récords» → «recorres» (7:48,2): revisar a oído |
| p17 | 7:52-8:31 | lite | −19,7 | 161 | 1384 | 3,2 | «Sídney» bien; «fundado en dos mil trece» con una sílaba de más (8:19,4, prob. 0,02) |
| cierre | 8:32-8:53 | lite | −19,9 | 159 | 1408 | 3,3 | Final completo; luego 2 s de imagen congelada |

Conclusiones:
- **Volumen.** De −16,7 a −21,7 dB: 5 dB entre bloques seguidos (p14 → p15 son −4 dB, p12 → p13 son +2,7 dB). Viene de `a = b["audio"] / max|audio| * 0.9` en `main()`: se normaliza cada bloque por pico. Hay que normalizar por sonoridad (loudnorm a −16 LUFS por bloque, o RMS de las tramas con voz) antes de sumar.
- **Timbre.** El cambio a flash (p05-p08, p10-p11) se nota sobre todo en el tono: p07 a 196 Hz, más que en el centroide. Dentro de lite también hay bloques más graves (p04 a 136 Hz, p09 a 139 Hz). Al regenerar con lite conviene repetir toma hasta que el f0 medio quede entre 155 y 170 Hz, y medirlo de forma automática (el script de esta revisión lo hace).
- **Cortes y finales.** Whisper oye la última palabra de todos los bloques: no hay finales comidos. No he encontrado cortes a mitad de palabra. El único hueco largo es el de 1,06 s en 1:53.
- **Respiraciones y ruidos.** El log del montaje quita un chasquido final de 0,10-0,15 s en los 19 bloques. Los mp3 de la rama llegan a pico de 0,0 dBFS, así que hay que comprobar que no saturan antes de `atempo=1.12`.
- **Música bajo la voz.** Es inaudible: la música sola en las pausas está a −26/−33 dB, y bajo la voz va unos 11 dB por debajo de eso, a unos 20-25 dB de la voz. Sube y baja en cada pausa de menos de 1 s, y eso se oye como bombeo.

---

## 4. Repeticiones entre vídeos (en números)

Método: se expande cada guion (V1 `guion_vl`, V2 `guion_vc`, V3 `guion_sg`, V4 `guion_jl`, V5 `guion_13a`, V6 `guion_pol`, V7 `guion_rad`) con la misma `expandir_grupos` y las mismas tablas de trozos. Un trozo cuenta como repetido si sale con el mismo nombre o si toma el mismo vídeo fuente con segundos que se solapan. Para comparar fuentes se tratan como iguales `MI` y `Mirada` (es el mismo «An Extended Look», `rk721912`), `T2` y `Trailer_2`, y `LZ` y `Lanzamiento`.

- **Trozos del vídeo 5:** 171 (16 son capturas NUEVO_).
- **Ya usados en otro vídeo del canal:** **142 de 171 (83 %)**. Otros 5 son de la misma escena (menos de 8 s de distancia) y solo **8 son nuevos de verdad**: ON_Juego_02, ON_Juego_21, ON_Juego_13, MI_17, NUEVO_RDR2_Paisaje, RDR2_01, MI_02 y MI_01. Y tres de esos son de la partida de GTA Online a 360p.
- **Tiempo en pantalla:** 413 s de 534 repetidos, 13 s de la misma escena, 29 s nuevos, 73 s de capturas y 6 s de cartelas.
- **Repetidos con cada vídeo:** V1 45, V2 45, **V3 115**, V4 48, **V6 82**, **V7 79**.
- **En cuántos vídeos anteriores sale cada repetido:** en 1 vídeo, 27 trozos; en 2, 17; en **3, 63**; en 4, 16; en 5, 14; en 6, 5.
- **Los más gastados:**
  - `Mirada_Atardecer` y su tramo (`VL_Atardecer_Final` y `VL_Lancha_Pareja` son los segundos 1569-1575 de Mirada): 11-16 apariciones en el canal;
  - `T1_Neones`: 11;
  - `Lanz_Paseo` y `Mirada_Skyline_Noche`: 9;
  - `T2_Cayos_Aereo`, `T2_Gimnasio_Playa`, `Mirada_Calles_1`, `Mirada_Mar_Atardecer` y `T1_Coches_Noche`: 8;
  - `Mirada_Logo`, `T1_Noche_Aerea` y `Mirada_Vista_Aerea`: 7.
- **Por qué pasa:**
  - `expandir_grupos()` baraja cada grupo con `random.Random(7)`, la misma semilla en todos los vídeos. Así, `@GTA_Online:4`, `@GTA5_2013:4` y `@Historia_GTA:8` dan **los mismos trozos en el mismo orden** en los vídeos 3, 5, 6 y 7. Por ejemplo, ON_Juego_22/06/16/30 salen en V3 p10, V6 p10-11 y V7 p11.
  - Los planos con nombre de `trozos.csv` (stock) son una lista corta, unos 62, que todos los guiones piden por nombre.
  - No hay ningún registro de lo usado en vídeos anteriores.
- **Dentro del propio vídeo 5:**
  - por nombre: `T1_Musica_Petty` ×2, `T1_Neones` ×2 y `Mirada_Skyline_Noche` ×2;
  - por escena (comprobado a ojo): la azotea ×3 (5:24, 5:46, 8:26), el coche en la avenida ×2 (3:04, 8:04), la carrera ×2 (5:50, 8:12), la playa aérea ×2 (5:22, 6:40), el logo de GTA VI ×3, «PRE-ORDER NOW» ×2 y «ROCKSTAR GAMES PRESENTS» ×2;
  - la nieve de GTA Online: 24 planos casi iguales de 0:55 a 2:17.
- **Material sin estrenar en las fuentes 4K** (tramos de 3 s o más que no ha usado ningún vídeo del canal):
  - tráiler 1: 57 de 90 s (4,9-12,9, 14,5-19,3, 41,2-51,2 y 56,2-90);
  - tráiler 2: 72 de 167 s (45,1-52,1, 66-81,2, 85-92,2, 105,9-111,5, 138-147,6 y 153,6-166,7);
  - tráiler de lanzamiento: 26 de 89 s (21-26,5, 27,8-40,5 y 42,2-47,2);
  - **Mirada / An Extended Look: 808 de 1608 s** (por ejemplo 46-114, 127-198, 330-365, 880-917 y 1119-1147);
  - RDR2: 38 de 60 s;
  - `ks18e7s9` (GTA Online PC): 32 de 40 s;
  - The Trilogy (GTA III y SA): unos 30 s cada uno;
  - sin usar nunca: Pre-Load Now (29 s), Cover Art Landscape (33 s), las 155 capturas oficiales 4K y los 9 vídeos de personaje de `GTAVI_Videos.zip`.

---

## E. Fuentes de mejor calidad (comprobadas)

Todo lo de esta lista está comprobado con `ffmpeg -i` sobre la URL. Para los zip, he leído el índice y las cabeceras de imagen con peticiones Range, sin bajarlos enteros.

| Fuente | URL | Resolución comprobada | Uso |
|---|---|---|---|
| Tráiler 1 de GTA VI | `https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Trailer_1/GTAVI_Trailer_1.mp4` | 3840x2160, 30 fps, MPEG-4 a 63 Mb/s, 1:30, **16:9 sin bandas** | p13 y gancho |
| Tráiler 2 de GTA VI | `…/GTAVI_Trailer_2/GTAVI_Trailer_2.mp4` | 3840x2160, 30 fps, 2:47, **letterbox ~2,2:1** | p14 y p17 (recortar las bandas) |
| Tráiler de lanzamiento | `…/GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4` | 3840x2160, 30 fps, 1:29, letterbox | p16 y p17 |
| An Extended Look | `…/GTAVI_An_Extended_Look/GTAVI_An_Extended_Look.mp4` (igual que `rk721912/flv/es-es-2160p.mp4`) | 3840x2160, 30 fps, 26:48, sin bandas en los planos medidos | Sustituto 4K de todos los `MI_*` (hoy salen de `es-es-1080p.mp4`) |
| Pre-Load Now | `…/GTAVI_Pre-Load_Now/GTAVI_Pre-Load_Now.mp4` | 3840x2160, 30 fps, 29 s | Planos nuevos 4-7 s, 10-16 s y 18-21 s; logo 22-24 s |
| Official Cover Art Landscape | `…/GTAVI_Official_Cover_Art_Landscape/GTAVI_Official_Cover_Art_Landscape.mp4` | 3840x2160, 30 fps, 33 s | VI animado 8-14 s y portada 15-20 s (p17 y cierre) |
| Capturas oficiales | `…/VI/downloads/screenshots/GTAVI_Screenshots.zip` (116 MB, 155 archivos) | 3840x2160 (comprobado en Boobie_Ike_01-04) | Carpetas People/* y Places/* (Ambrosia, Grassrivers, Leonida Keys, Mount Kalaga, Port Gellhorn, Vice City) |
| Fondos oficiales | `…/VI/downloads/artwork_wallpapers/GTAVI_Artwork_Wallpapers.zip` (246 MB) | *_landscape.jpg a 3840x2160 (comprobado en Boobie_Ike_landscape) | Fondos de las cartelas |
| Vídeos de personaje | `…/VI/downloads/videos/GTAVI_Videos.zip` (121 MB, 9 mp4) | Sin comprobar: haría falta bajar el zip | — |
| Tráiler GTA V / Online PC (Rockstar) | `https://videos-rockstargames-com.akamaized.net/v4/ks18e7s9/flv/en-us-2160p.mp4` | 3840x2160, 60 fps, 40 s, letterbox | p01-p04. Planos sin texto: 9-11,9 s, 16-18,9 s, 23-24 s y 28-30 s. Evitar 0-8 s (ESRB, logos, «FREE UPGRADE») y 12-15 s, 19-22 s y 24-27 s (textos) |
| Tráiler de RDR2 (Rockstar) | `…/v4/6c8k48rr/flv/en-us-2160p.mp4` | 3840x2160, 29,97 fps, 60 s, letterbox | p06 (hoy se usa la de 1080p) |
| The Trilogy DE (Rockstar) | `…/v4/8ta2r546/flv/en-us-2160p.mp4`, `…/v4/5r2a2o2k/flv/en-us-2160p.mp4`, `…/v4/rr54344t/flv/en-us-2160p.mp4` | 3840x2160, 30 fps, 58, 42 y 42 s | p10 (en lugar de `VCDE_Juego` a 480p) |
| Rockstar North (Commons) | `https://commons.wikimedia.org/wiki/File:20231022_Rockstar_North.jpg` | 3834x2324, CC0 | p06 y p08 |
| Southwark Crown Court (Commons) | `https://commons.wikimedia.org/wiki/File:London_Southwark_Crown_Court_(50604622932).jpg` | 4512x2708, CC BY 2.0 (citar al autor) | p12 |
| Strauss Zelnick (Commons) | `https://commons.wikimedia.org/wiki/File:Strauss_Zelnick,_2015_(16339090774).jpg` | 1368x2048, CC BY 2.0; vertical, para un panel lateral | p16 |
| Dundee waterfront (Commons) | `https://commons.wikimedia.org/wiki/File:Dundee_Waterfront_Redevelopment_Feb_2018_a_-_V%26A_Near_Completion.jpg` | 4928x2372, CC BY-SA 4.0 | p09 |
| Sam y Dan Houser (Commons) | `https://commons.wikimedia.org/wiki/File:Sam_Houser_and_Dan_Houser.png` | 1536x2048, CC BY-SA 4.0; vertical | p08 (panel lateral, nunca a pantalla completa) |
| Logo de Twitch (Commons) | `https://commons.wikimedia.org/wiki/File:Twitch_logo_2019.svg` | SVG, dominio público | p03 |

Notas:
- No he encontrado un vídeo oficial de GTA Online «de siempre» ni de Red Dead Online en las páginas descargables. La web de Rockstar es una aplicación JavaScript y no saca los ID de vídeo en el HTML. Para buscarlos se puede usar la API `graph.rockstargames.com` que ya usa `gta/fuentes.py` (operación `NewswirePost`): los artículos del Newswire llevan los ID de vídeo, y luego se prueba `…/v4/<id>/flv/en-us-2160p.mp4` con ffmpeg.
- Capturas web nuevas: Playwright con `channel="msedge"`, `viewport={"width":2560,"height":1440}`, `device_scale_factor=1`. Hay que ocultar las cabeceras fijas, los banners de cookies y la publicidad con CSS inyectado. No se debe mostrar ningún dato personal (nombres de usuario, avatares, comentarios).

---

## 5. Cambios de edición en montaje.py y prototipo.py (por prioridad)

### Prioridad 1: imagen limpia, 2K constante y sincronizada

1. **Salida a 2560x1440.** En `prototipo.py`, `W, H = 2560, 1440`.
   - Se puede dejar `PlayResX/PlayResY` del ASS en 1920x1080: libass escala todo al tamaño del vídeo (rótulos, subtítulos y dibujos `\p1`). Es el cambio más barato.
   - `crear_degradado()` ya usa `W`.
   - En `capa_linea` hay que escalar `LT.Y0` y el ancho de `linea.mov` (multiplicar por 4/3), o renderizar `linea_tiempo.py` a 2560.
   - En la codificación final: `-crf 16 -preset slow -x264-params aq-mode=3`, y para YouTube `-b:v` de unos 24 Mb/s si se quiere tope.

2. **`cortar()` sin pad y sin MARCO.**
   - Primero se quitan las bandas negras de la fuente: un `cropdetect` por vídeo, guardado en caché como `_ALTOS`, o un `RECORTE_BANDAS = {"Trailer_2": 0.10, "Lanzamiento": 0.10, "RDR2": 0.10, "V_PS5": 0.10}` (fracción arriba y abajo, medida: imagen entre las filas 27 y 242 de 270).
   - Después: `crop=iw:ih*(1-2*b):0:ih*b, scale=2816:1584:force_original_aspect_ratio=increase:flags=lanczos, crop=2560:1440:x=…:y=…`.
   - Hay que **borrar la rama `if MARCO …`** y **parar con error si `alto(fuente) < 1080`**. Lo que no llegue a 1080p no entra.
   - Para `Imagen:`, la captura tiene que ser de 2560x1440 de origen y se usa `scale=2560:1440` sin pad, con un zoom lento (ver el punto 7).
   - Para fotos verticales (Commons): composición con la foto en un panel a la derecha y fondo de color plano de la marca. Ni borroso ni negro.

3. **Fuentes.**
   - En `fuentes_jl.py`, `"MI": … "es-es-1080p.mp4"` pasa a `"es-es-2160p.mp4"`, y `"RDR2"` a `en-us-2160p.mp4`.
   - En `fuentes_sg.py`, `rs("ks18e7s9","1080p")`, `rs("5r2a2o2k","1080p60")` y `rs("rr54344t","1080p60")` pasan a `"2160p"`.
   - Fuera los grupos `GTA5_2013` (V_Juego), `GTA_Online` (ON_Juego), `Historia_GTA` (GTA_15) y `VC_DE` (VCDE_Juego) en todos los guiones nuevos.
   - Como las alturas de las fuentes van a cambiar, conviene borrar `_ALTOS` (la caché de alturas) y la carpeta `fuentes/`.

4. **Sincronía de vídeo y rótulos.**
   - En `cortar()`, cambiar `-t dur` por `-frames:v round(dur*FPS)`.
   - En `main()`, calcular `b["ini"]` y los demás tiempos a partir de los fotogramas acumulados (`n_frames/FPS`), no de los segundos planeados. Lo mismo para la cartela (`color=…:d=` → `-frames:v 48`).
   - Así desaparecen los 0,5 s de negro sin texto, la cartela que se queda encima del plano siguiente y el fotograma suelto de 4:07,25.

5. **Repeticiones.**
   - `expandir_grupos()`: semilla distinta por guion, por ejemplo `random.Random(hash(GUION))`, y una lista `USADOS_CANAL` (CSV con fuente, ini y fin de los vídeos ya publicados) que se excluye antes de elegir.
   - `comprobar_repetidos()`: comparar por `(alias de fuente, tramo)` con `ALIAS = {"MI": "Mirada", "T2": "Trailer_2", "LZ": "Lanzamiento"}` y un margen de 8 s, incluyendo `intro_original` y `original`. Con eso habría saltado `T1_Musica_Petty` (intro y ancla a la vez).
   - En el guion, quitar `{"en": "petty", "plano": "T1_Musica_Petty"}` de p13.

6. **Plano máximo de 6 s.** En `planificar()` y `planificar_anclado()`, si se acaban los planos no se debe alargar el último (`lista[-1][1] += resto`), porque se ve lo que viene después en la fuente (MI_51 de 16,6 s con la hamburguesa y el logo; GTA_15_01 de 8,7 s). Es mejor parar con un aviso de «faltan N s de material» o tomar otro tramo libre de la misma fuente.

### Prioridad 2: grafismo (es lo que más da la sensación de «cutre»)

7. **Movimiento de cámara.** Ahora es un barrido lateral lineal y siempre igual (`x=(in_w-out_w)*t/dur`, sobre un sobrante del 10 %), y las imágenes van quietas.
   - Cambiarlo por un zoom suave con aceleración y frenada: `zoompan` o `crop` con `x,y` en `0.5-0.5*cos(PI*t/dur)`, del 100 al 106 %, alternando entrada y salida y la dirección.
   - En capturas: zoom hacia el titular. Se puede guardar el rectángulo del titular por captura en `trozos_57.csv`.

8. **Rótulos de datos** (`anadir_rotulos`).
   - Fuera la caja negra centrada en y=440. En su lugar, un tercio inferior a la izquierda (x≈160, y≈700 en coordenadas 1080) con una barra de acento rosa de 8 px a la izquierda.
   - La línea 1 en Montserrat Black 64 en blanco y la línea 2 en Montserrat SemiBold 34 en rosa. El amarillo (`&H0000D7FF`), solo para cifras.
   - Entrada con `\move` de 40 px + `\fad(120,0)` + `\t(0,200,\fscx100)` desde `\fscx90`. Salida de 150 ms.
   - Si el plano en pantalla es `Imagen:` o un logo, el rótulo no se pone: la captura ya es el dato.
   - Ancla: para «mismo» en p04 usar `"n": 2`, y en general permitir `"despues_de"` para no engancharse a la primera aparición.

9. **Título del bloque** («02 /17 · 2013-2026 · EL DINERO»). Ahora está fijo todo el bloque, con el número a 132 px, el total y un título Bebas de 74 px, y pisa las capturas. Mejor que salga 3,5 s y luego se reduzca a una etiqueta pequeña (Bebas 34, `\t` de escala y posición) o que desaparezca. Con la línea de tiempo de abajo ya se sabe dónde se está.

10. **Cartelas de acto** (`anadir_cartelas`, DUR_CARTELA 1,6 s).
    - El negro plano con «golpe» sintético queda pobre. Para el vídeo 4 ya existe `cristal.fotograma_cartela()`, que pone de fondo un fotograma difuminado del primer plano del acto: activarlo también aquí, sin `CRISTAL=True` en todo el resto.
    - Duración de 2,2 s, el año contando hacia arriba (por ejemplo 2008 → 2013, con `\t` o 10 eventos) y el título con escritura letra a letra.
    - Tipografía: dejar una sola familia de display (Bebas para el año) y Montserrat para el resto.

11. **Degradado de abajo** (`ALTO_DEGRADADO = 380`, alfa hasta 165). Oscurece el tercio inferior de todo el vídeo, incluidos los planos 4K. Bajarlo a 260 px y alfa 120, y darle un poco de color de la marca (azul muy oscuro) en vez de negro puro.

12. **Subtítulos** (`escribir_ass`, Montserrat ExtraBold 60, karaoke rosa).
    - Una línea, de 32 caracteres como máximo y 2 palabras mínimo por línea. Ahora se quedan «que» o «en» solos en la segunda línea (1:56).
    - Altura fija: hoy saltan de una a dos líneas. Tamaño de 54 px (escalado a 2K).
    - Quitar el `\fad(…,130)` de salida de la última palabra, que se superpone a la frase siguiente durante 130 ms (1:56,25).

13. **Transiciones.** Todo son cortes secos con `concat -c copy`.
    - Dentro de un bloque: cortes en el ritmo de la voz (al inicio de palabra, con los tiempos de Whisper que ya se tienen).
    - Entre bloques: fundido de 8 fotogramas (`xfade=fade:duration=0.27`) y un *whoosh* suave en vez del «golpe».
    - Para hacerlo hay que pasar de `concat -c copy` a un filtro con `xfade` en los límites de bloque, o mezclar los 2 planos frontera en `cortar()`.

14. **Color y nitidez.** `eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.4` se aplica a todo. Con fuentes 4K bien escaladas no hace falta el `unsharp`: realza el ruido y hoy marca aún más los bloques de 360p. Quitarlo, o dejarlo en 0,2 solo para las capturas.

### Prioridad 3: sonido

15. **Voz por sonoridad, no por pico.** En `main()`, en vez de `b["audio"] / max|audio| * 0.9`, igualar el RMS de las tramas con voz (por ejemplo a −20 dBFS) y luego un limitador común. Así desaparecen los 5 dB de diferencia.

16. **Música.**
    - Quitar el `chiptune`: GTA V en 2013 no pide 8 bits, y la onda cuadrada es lo que más suena a casero. Usar una sola base (synthwave, `musica_estilo`) con variantes por acto.
    - Ganancia bajo la voz de 0,085 → 0,14. La ducking más lenta (`P.suavizar(..., 0.06, 0.5)` → ataque 0,25 s y suelta 0,9 s), y que no suba en pausas de menos de 1,2 s.
    - Si se puede, una pista con licencia clara comprada por el canal.

17. **Final.** Cambiar `tpad=stop_mode=clone:stop_duration=3` por una pantalla final propia de 12-20 s (fondo de Cover Art 15-20 s desenfocado y huecos para las tarjetas de YouTube).

### Prioridad 4: guion de planos (sin tocar código)

18. Cada bloque tiene que tener planos del tema que cuenta. El que no tenga material oficial va con capturas a 2560x1440 o gráficos propios (cifras y fechas), nunca con relleno de GTA VI:
    - p01-p04 (GTA V y Online): `ks18e7s9` en 4K + capturas;
    - p06 (RDR2): `6c8k48rr` en 4K + Rockstar North (CC0);
    - p07 (RDO): captura de la web de RDO + gráfico;
    - p08-p09 (Houser y Ruffian): capturas, fotos de Commons y Mirada en 4K desenfocada;
    - p10 (Trilogy): los tres tráileres oficiales en 4K;
    - p11-p12 (filtración y juicio): tarjeta de hechos en ASS + Southwark (CC BY 2.0);
    - p13-p17 (GTA VI): los tramos sin estrenar de los tráileres 1 y 2, el de lanzamiento, Pre-Load, Cover Art y Mirada en 4K.
