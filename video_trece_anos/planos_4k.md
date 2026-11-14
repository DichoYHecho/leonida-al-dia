# Planos 4K del vídeo 5 · «¿Por qué GTA VI ha tardado 13 años?»

Propuesta del 14 nov 2026 para rehacer los planos con material oficial de Rockstar en 2160p. Tabla de trozos: `para_github/trozos_13a_4k.csv` (prefijo `K5_`). Imágenes: `para_github/imagenes_4k/`. Hojas de contacto: `video_trece_anos/planos_4k_hojas/hoja_<bloque>.jpg`.

Cómo se ha comprobado:
- Cada URL se ha abierto con `ffmpeg -i` (resolución y fps de la tabla) y se han sacado fotogramas de los trozos elegidos sobre la propia URL 4K (inicio, centro y final de cada trozo).
- Cortes de plano: puntuación de escena de ffmpeg fotograma a fotograma sobre la versión 720p de la misma URL (misma línea de tiempo); ningún trozo tiene un corte con puntuación ≥ 0,10 dentro. Además se han mirado los tres fotogramas de cada trozo a ojo (se han quitado los que tenían texto, logos, interfaz, fundidos o cortes suaves).
- Repeticiones: se ha cruzado cada trozo con todo lo que usan los vídeos 1-4, 6 y 7 (guiones expandidos con las tablas de trozos; MI = Mirada, T1 = Trailer_1, T2 = Trailer_2, LZ = Lanzamiento, V_PS5 = ks18e7s9, VC_Tril = 8ta2r546, RDR2 = 6c8k48rr). Ningún trozo solapa con lo ya publicado. Dentro del vídeo no se repite ningún trozo ni ninguna imagen.
- Fuentes nuevas encontradas con la API de vídeos de Rockstar (`graph.rockstargames.com`, consulta `GET_VIDEO_DATA` del reproductor oficial; los artículos del Newswire enlazan `videoplayer/?id=…`). Las imágenes de GTA Online, GTA V y The Trilogy salen de los artículos del Newswire (`NewswirePost`, carpeta `tina-uploads` del CDN de Rockstar), todas a 3840x2160.
- `Lento` = factor de cámara lenta del montaje (duración en pantalla = duración del trozo × Lento). Se usa solo para llegar a 2,5 s en planos cortos de tráileres que cortan muy rápido; en `GTAV_PC_4K` (60 fps) la cámara lenta es fluida. Todos los trozos duran entre 2,5 y 6 s en pantalla.

## a) Fuentes

| Nombre corto | URL comprobada | Resolución | fps | Letterbox (fracción arriba y abajo) | Qué es |
|---|---|---|---|---|---|
| `GTAO_Bounties_4K` | `https://videos-rockstargames-com.akamaized.net/v4/oa46rs8r/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: Bottom Dollar Bounties (2024) |
| `GTAO_CE_4K` | `https://videos-rockstargames-com.akamaized.net/v4/8rakra67/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA Online: The Criminal Enterprises (2022) |
| `GTAO_Cluckin_4K` | `https://videos-rockstargames-com.akamaized.net/v4/r3175t5r/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: The Cluckin' Bell Farm Raid (2024) |
| `GTAO_Kanjo_4K` | `https://videos-rockstargames-com.akamaized.net/v4/3ra4t562/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA Online: Dinka Kanjo SJ y Postlude (2022) |
| `GTAO_Kortz_4K` | `https://videos-rockstargames-com.akamaized.net/v4/a0a0rre4/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: The Kortz Center Heist (2026) |
| `GTAO_Luiva_4K` | `https://videos-rockstargames-com.akamaized.net/v4/203as2rs/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: Progen Luiva (2025) |
| `GTAO_PS5_4K` | `https://videos-rockstargames-com.akamaized.net/v4/1s626s55/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA V y GTA Online: «Out Now on PlayStation 5 and Xbox Series X|S» (2022) |
| `GTAO_Pizza_4K` | `https://videos-rockstargames-com.akamaized.net/v4/aro34sg4/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA Online: Pizza Deliveries (2024) |
| `GTAO_Sabotage_4K` | `https://videos-rockstargames-com.akamaized.net/v4/r50k6mmg/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: Agents of Sabotage (2024) |
| `GTAO_Safehouse_4K` | `https://videos-rockstargames-com.akamaized.net/v4/to78rk1o/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA Online: A Safehouse in the Hills (2025) |
| `GTAO_Vigero_4K` | `https://videos-rockstargames-com.akamaized.net/v4/k1t75kk6/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA Online: Declasse Vigero ZX (2022) |
| `GTAO_Weevil_4K` | `https://videos-rockstargames-com.akamaized.net/v4/a9233r59/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA Online: BF Weevil Custom (2022) |
| `GTAV_PC_4K` | `https://videos-rockstargames-com.akamaized.net/v4/ks18e7s9/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 60 | 0.1 | GTA V/Online: tráiler de GTAV Enhanced para PC (2025) |
| `GTAV_PS5_4K` | `https://videos-rockstargames-com.akamaized.net/v4/r3too449/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | GTA V: «Coming March 2022 for PS5 and Xbox Series X|S» (2021) |
| `LANoire_4K` | `https://videos-rockstargames-com.akamaized.net/v4/3rr4o8so/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | L.A. Noire: 4K Trailer (2017, reedición hecha con Video Games Deluxe) |
| `Lanz` | `https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4` | 3840x2160 (h264) | 30 | 0.056 | GTA VI: Tráiler de lanzamiento |
| `Mirada4K` | `https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-2160p.mp4` | 3840x2160 (h264) | 30 | 0.0 | GTA VI: An Extended Look (es-es, 2160p) |
| `PreLoad` | `https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Pre-Load_Now/GTAVI_Pre-Load_Now.mp4` | 3840x2160 (h264) | 30 | 0.056 | GTA VI: Pre-Load Now |
| `RDO_Beta_4K` | `https://videos-rockstargames-com.akamaized.net/v4/r5tc99c3/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | Red Dead Online Beta Update (2019) |
| `RDO_BloodMoney_4K` | `https://videos-rockstargames-com.akamaized.net/v4/3a753kct/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | Red Dead Online: Blood Money (2021) |
| `RDO_Frontier_4K` | `https://videos-rockstargames-com.akamaized.net/v4/c686k8ok/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | Red Dead Online: Frontier Pursuits (2019) |
| `RDO_Lanz_4K` | `https://videos-rockstargames-com.akamaized.net/v4/5611kt7k/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | Red Dead Online: Launch Trailer (2019) |
| `RDO_Moonshiners_4K` | `https://videos-rockstargames-com.akamaized.net/v4/57s1k75o/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | Red Dead Online: Moonshiners (2019) |
| `RDO_Naturalist_4K` | `https://videos-rockstargames-com.akamaized.net/v4/k56k16rs/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | Red Dead Online: The Naturalist (2020) |
| `RDR2_4K` | `https://videos-rockstargames-com.akamaized.net/v4/6c8k48rr/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.1 | RDR2: Launch Trailer (2018) |
| `RDR2_Gameplay_4K` | `https://videos-rockstargames-com.akamaized.net/v4/1ook234t/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 29.97 | 0.0 | RDR2: Official Gameplay Video (2018, sin narración en el montaje) |
| `RDR2_PC_4K` | `https://videos-rockstargames-com.akamaized.net/v4/9krr33s1/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.1 | RDR2: PC Trailer (2019) |
| `T1` | `https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Trailer_1/GTAVI_Trailer_1.mp4` | 3840x2160 (mpeg4) | 30 | 0.0 | GTA VI: Tráiler 1 |
| `T2` | `https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Trailer_2/GTAVI_Trailer_2.mp4` | 3840x2160 (mpeg4) | 30 | 0.1 | GTA VI: Tráiler 2 |
| `Trilogy_4K` | `https://videos-rockstargames-com.akamaized.net/v4/8ta2r546/flv/en-us-2160p.mp4` | 3840x2160 (h264) | 30 | 0.096 | GTA: The Trilogy – The Definitive Edition Trailer (2021) |
| `Imagen:` | `media-rockstargames-com.akamaized.net/VI/downloads/screenshots/GTAVI_Screenshots.zip` y `…/tina-uploads/posts/<artículo>/<hash>.jpg` del Newswire | 3840x2160 (las dos de The Trilogy, recortadas sin el logo: 3072x1728) | — | 0 | Capturas oficiales; lista completa en el CSV |

Notas sobre las fuentes:
- Letterbox: el montaje ya lo recorta con cropdetect; la fracción se da para comprobarlo. Mirada, T1, RDR2_Gameplay y GTAO_PS5 no tienen bandas (en Mirada el cropdetect puede confundir planos muy oscuros con bandas: conviene fijarlo a 0).
- `GTAO_PS5_4K` (1s626s55) y `GTAV_PS5_4K` (r3too449) no los ha usado nunca el canal. Tampoco los de Red Dead Online, L.A. Noire, `RDR2_PC_4K`, `RDR2_PCLanz_4K`, `RDR2_Gameplay_4K` ni los de GTA Online de 2022-2026.
- `Trilogy_4K`: los planos de este tráiler tienen una barra de luz que pasa de la versión original a la remasterizada (no hay texto). Encaja con «remasterizados», pero se ve el barrido.
- Descartados: los vídeos comparativos de GTA III y San Andreas (5r2a2o2k, rr54344t) llevan los rótulos «original» / «the definitive edition» y barridos en todos los planos; `CoverArt` es solo logo y la portada; la mayoría de los tráileres de GTA Online cortan cada 1-2 s o llevan texto encima; los planos de RDR2 Gameplay con minimapa o con la interfaz del póker; los de Mirada con interfaz de vida/munición.

## b) Planos por bloque

Formato del guion: `planos` en el orden de montaje y `planos_en` con la palabra de anclaje (el montaje compara por inicio de palabra normalizada; entre paréntesis, qué aparición es). Las capturas `NUEVO_` son las que ya están en el guion y las prepara otra persona; se dejan en su sitio.

### hook

```python
"planos": ["NUEVO_Filtracion_Foro", "K5_Mir_Llegada_Noche", "NUEVO_Comunicado_Rockstar", "K5_GTAV_Coche_Atardecer", "K5_Img_VC_Skyline_Helicoptero", "K5_T2_Atardecer_Aereo", "K5_Img_Leonida_Keys_Avioneta", "K5_Img_Grassrivers_Hidrodeslizador"],
"planos_en": [{"en": "cincuenta", "plano": "K5_Mir_Llegada_Noche"},
              {"en": "noventa", "plano": "NUEVO_Filtracion_Foro"},
              {"en": "confirma", "plano": "NUEVO_Comunicado_Rockstar"},
              {"en": "trece", "plano": "K5_GTAV_Coche_Atardecer"},
              {"en": "noviembre", "plano": "K5_Img_VC_Skyline_Helicoptero"},
              {"en": "tiempo", "plano": "K5_T2_Atardecer_Aereo"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Filtracion_Foro` | captura (otra persona) | 4 s | «noventa» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Mir_Llegada_Noche` | Mirada4K 7.00-12.40 | 5.40 s | «cincuenta» (1.ª de 1) | Primeros segundos de partida de GTA VI: Jason y Lucía caminan de noche hacia un edificio |
| `NUEVO_Comunicado_Rockstar` | captura (otra persona) | 4 s | «confirma» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_GTAV_Coche_Atardecer` | GTAV_PS5_4K 39.25-40.95 ×1.5 | 2.55 s | «trece» (1.ª de 1) | GTA V: un coche por la costa al atardecer visto de lado |
| `K5_Img_VC_Skyline_Helicoptero` | Imagen:K5_VC_Skyline_Helicoptero.jpg | 4 s (imagen) | «noviembre» (1.ª de 1) | Captura oficial 4K: skyline de Vice City al atardecer con un helicóptero |
| `K5_T2_Atardecer_Aereo` | T2 153.70-155.90 ×1.15 | 2.53 s | «tiempo» (1.ª de 1) | Vuelo sobre un barrio de Vice City al atardecer |
| `K5_Img_Leonida_Keys_Avioneta` | Imagen:K5_Leonida_Keys_Avioneta.jpg | 4 s (imagen) | — | Captura oficial 4K: los Cayos de Leonida desde el aire con una avioneta |
| `K5_Img_Grassrivers_Hidrodeslizador` | Imagen:K5_Grassrivers_Hidrodeslizador.jpg | 4 s (imagen) | — | Captura oficial 4K: un hidrodeslizador por los pantanos de Grassrivers con un helicóptero |

GTA VI en bruto (partida del An Extended Look) para «vídeos de un juego que nadie había visto», GTA V para «trece años después de GTA V», Vice City al atardecer para la fecha y la pregunta final.

### p01

```python
"planos": ["K5_GTAV_Puesta_Cables", "K5_GTAV_Michael_Tenis", "K5_GTAV_Franklin_Puerta", "K5_GTAO_Chimeneas", "K5_GTAO_Edificio_Contrapicado", "K5_Img_GTAO_Laser", "K5_GTAV_Trevor_Trio", "K5_GTAV_Puente_Rio", "K5_GTAV_Coche_Costa", "K5_Img_GTAO_Camara_Kortz", "K5_GTAO_Rascacielos", "K5_Img_GTAO_Michael_Sofa", "K5_Img_GTAO_Coche_Verde"],
"planos_en": [{"en": "septiembre", "plano": "K5_GTAV_Puesta_Cables"},
              {"en": "Michael", "plano": "K5_GTAV_Michael_Tenis"},
              {"en": "Franklin", "plano": "K5_GTAV_Franklin_Puerta"},
              {"en": "cambiar", "plano": "K5_GTAV_Trevor_Trio"},
              {"en": "atraco", "plano": "K5_Img_GTAO_Camara_Kortz"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_GTAV_Puesta_Cables` | GTAV_PS5_4K 2.35-4.00 ×1.55 | 2.56 s | «septiembre» (1.ª de 1) | GTA V: puesta de sol entre cables y palmeras de Los Santos |
| `K5_GTAV_Michael_Tenis` | GTAV_PS5_4K 26.35-28.90 | 2.55 s | «Michael» (1.ª de 1) | GTA V: Michael en la pista de tenis de su mansión |
| `K5_GTAV_Franklin_Puerta` | GTAV_PS5_4K 7.40-9.00 ×1.6 | 2.56 s | «Franklin» (1.ª de 1) | GTA V: Franklin en la puerta de una casa |
| `K5_GTAO_Chimeneas` | GTAO_PS5_4K 29.45-30.95 ×1.7 | 2.55 s | — | Chimeneas de una fábrica al atardecer en Los Santos |
| `K5_GTAO_Edificio_Contrapicado` | GTAO_PS5_4K 33.45-35.20 ×1.45 | 2.54 s | — | Edificio de Los Santos en contrapicado |
| `K5_Img_GTAO_Laser` | Imagen:K5_GTAO_Atracador_Laser.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un atracador entre láseres de seguridad |
| `K5_GTAV_Trevor_Trio` | GTAV_PS5_4K 46.95-48.35 ×1.8 | 2.52 s | «cambiar» (1.ª de 1) | GTA V: Michael, Franklin y Trevor juntos en una cocina |
| `K5_GTAV_Puente_Rio` | GTAV_PS5_4K 17.10-18.85 ×1.45 | 2.54 s | — | GTA V: puente y río en las montañas del condado de Blaine |
| `K5_GTAV_Coche_Costa` | GTAV_PS5_4K 37.40-39.10 ×1.5 | 2.55 s | — | GTA V: coche rojo por la carretera de la costa |
| `K5_Img_GTAO_Camara_Kortz` | Imagen:K5_GTAO_Camara_Acorazada.jpg | 4 s (imagen) | «atraco» (1.ª de 1) | Imagen oficial 4K (Newswire): atracadores dentro de una cámara acorazada |
| `K5_GTAO_Rascacielos` | GTAO_PS5_4K 4.90-6.88 ×1.3 | 2.57 s | — | Rascacielos de Los Santos a contraluz |
| `K5_Img_GTAO_Michael_Sofa` | Imagen:K5_GTAO_Michael_Sofa.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): Michael De Santa en el sofá de su casa |
| `K5_Img_GTAO_Coche_Verde` | Imagen:K5_GTAO_Coche_Verde.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): coche verde entre palmeras de Los Santos |

Solo GTA V: la mansión de Michael, Franklin, los tres protagonistas juntos para «cambiar entre ellos», una cámara acorazada para «atraco». Las dos imágenes de GTA Online son de Los Santos (mismo mapa).

### p02

```python
"planos": ["K5_GTAO_Atico_Fiesta", "K5_GTAO_Atico_Ventanal", "K5_GTAO_Dos_Hombres_Casa", "K5_Img_GTAO_Derrape_Doble", "K5_GTAO_Garaje_Neon", "K5_Img_GTAO_Plan_Golpe", "K5_Img_GTAO_Vitrina_Oro", "K5_Img_GTAO_Banda", "K5_GTAO_Aereo_Kortz", "K5_GTAO_Tuning_Garaje", "K5_Img_GTAO_Coche_Neon", "NUEVO_Cuentas_TakeTwo", "K5_GTAO_Oficina_Agentes", "K5_Img_GTAO_Coches_Noche", "K5_GTAO_Dos_Personajes", "K5_Img_GTAO_Grupo_Camion"],
"planos_en": [{"en": "online", "plano": "K5_GTAO_Atico_Fiesta"},
              {"en": "ingresos", "plano": "NUEVO_Cuentas_TakeTwo"},
              {"en": "monedas", "plano": "K5_Img_GTAO_Vitrina_Oro"},
              {"en": "contenidos", "plano": "K5_Img_GTAO_Coche_Neon"},
              {"en": "motores", "plano": "K5_GTAO_Garaje_Neon"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_GTAO_Atico_Fiesta` | GTAV_PS5_4K 55.95-61.50 | 5.55 s | «online» (1.ª de 4) | GTA Online: fiesta en un ático con vistas a Los Santos |
| `K5_GTAO_Atico_Ventanal` | GTAV_PS5_4K 61.50-65.00 | 3.50 s | — | GTA Online: el jugador mira la ciudad desde el ventanal (sigue el mismo plano) |
| `K5_GTAO_Dos_Hombres_Casa` | GTAO_Safehouse_4K 7.60-9.70 ×1.2 | 2.52 s | — | GTA Online: dos personajes conversan en una casa |
| `K5_Img_GTAO_Derrape_Doble` | Imagen:K5_GTAO_Derrape_Doble.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): dos coches derrapando |
| `K5_GTAO_Garaje_Neon` | GTAO_Luiva_4K 12.40-14.60 ×1.15 | 2.53 s | «motores» (1.ª de 1) | GTA Online: superdeportivo en un garaje con neones |
| `K5_Img_GTAO_Plan_Golpe` | Imagen:K5_GTAO_Plan_Golpe.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un equipo planea un golpe sobre una maqueta |
| `K5_Img_GTAO_Vitrina_Oro` | Imagen:K5_GTAO_Vitrina_Oro.jpg | 4 s (imagen) | «monedas» (1.ª de 1) | Imagen oficial 4K (Newswire): vitrinas con monedas y lingotes de oro |
| `K5_Img_GTAO_Banda` | Imagen:K5_GTAO_Banda.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): personajes de GTA Online posan con sus vehículos |
| `K5_GTAO_Aereo_Kortz` | GTAO_Kortz_4K 7.20-8.70 ×1.7 | 2.55 s | — | GTA Online: vista aérea de un edificio en las colinas |
| `K5_GTAO_Tuning_Garaje` | GTAO_Kanjo_4K 7.00-9.60 | 2.60 s | — | GTA Online: coches preparados en un garaje |
| `K5_Img_GTAO_Coche_Neon` | Imagen:K5_GTAO_Coche_Personaje.jpg | 4 s (imagen) | «contenidos» (1.ª de 1) | Imagen oficial 4K (Newswire): un personaje junto a su coche de contenido extra |
| `NUEVO_Cuentas_TakeTwo` | captura (otra persona) | 4 s | «ingresos» (1.ª de 2) | Captura web prevista en el guion (NUEVO_) |
| `K5_GTAO_Oficina_Agentes` | GTAO_Sabotage_4K 18.20-19.95 ×1.45 | 2.54 s | — | GTA Online: agentes en una oficina |
| `K5_Img_GTAO_Coches_Noche` | Imagen:K5_GTAO_Coches_Noche.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): dos coches preparados de noche |
| `K5_GTAO_Dos_Personajes` | GTAO_Bounties_4K 3.80-6.70 | 2.90 s | — | GTA Online: dos personajes hablan en un local |
| `K5_Img_GTAO_Grupo_Camion` | Imagen:K5_GTAO_Grupo_Camion.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un grupo de jugadores junto a un camión de noche |

GTA Online: el ático, garajes, coches de contenido extra, golpes en equipo y monedas/oro para «monedas virtuales». Nada de la partida de 360p ni de la nieve.

### p03

```python
"planos": ["K5_Img_GTAV_Skyline_Rol", "K5_GTAV_Persecucion_Policia", "K5_Img_GTAV_Rol_BurgerShot", "K5_GTAO_Pizza_Moto", "K5_GTAO_Pizza_Moto_2", "K5_GTAO_Lavadero", "K5_GTAV_Ruta68_Policia", "NUEVO_Twitch_Captura", "K5_Img_GTAO_Bicis", "K5_GTAO_Paso_Inferior", "K5_Img_GTAO_Policia_Comisaria", "K5_Img_GTAO_Desguace", "K5_GTAO_Carretera_Noche", "K5_GTAO_Carretera_Monte", "K5_Img_GTAO_Jugador_Noche", "K5_GTAO_Granja_Aerea", "NUEVO_Cfx_Comunicado", "K5_GTAO_Taller_Bennys", "K5_RDR2_Pueblo_Valentine", "K5_Img_GTAO_Coche_Policia", "K5_Img_GTAO_Coche_Neon_PS5"],
"planos_en": [{"en": "rol", "plano": "K5_Img_GTAV_Rol_BurgerShot"},
              {"en": "policía", "plano": "K5_GTAV_Persecucion_Policia"},
              {"en": "taxista", "plano": "K5_GTAO_Pizza_Moto"},
              {"en": "Twitch", "plano": "NUEVO_Twitch_Captura"},
              {"en": "prohibido", "plano": "K5_GTAV_Ruta68_Policia"},
              {"en": "Cfx", "plano": "NUEVO_Cfx_Comunicado"},
              {"en": "RedM", "plano": "K5_RDR2_Pueblo_Valentine"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Img_GTAV_Skyline_Rol` | Imagen:K5_GTAV_Skyline_Helicoptero.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire, «nopixel V»): Los Santos con un helicóptero |
| `K5_GTAV_Persecucion_Policia` | GTAV_PS5_4K 23.60-25.25 ×1.55 | 2.56 s | «policía» (1.ª de 1) | GTA V: persecución con la policía vista desde arriba |
| `K5_Img_GTAV_Rol_BurgerShot` | Imagen:K5_GTAV_Rol_BurgerShot.jpg | 4 s (imagen) | «rol» (1.ª de 1) | Imagen oficial 4K (Newswire, «nopixel V»): dos personajes con el uniforme de Burger Shot |
| `K5_GTAO_Pizza_Moto` | GTAO_Pizza_4K 3.50-5.35 ×1.35 | 2.50 s | «taxista» (1.ª de 1) | GTA Online: reparto de pizzas en moto |
| `K5_GTAO_Pizza_Moto_2` | GTAO_Pizza_4K 5.45-7.45 ×1.25 | 2.50 s | — | GTA Online: reparto de pizzas por la ciudad |
| `K5_GTAO_Lavadero` | GTAO_CE_4K 8.20-10.20 ×1.25 | 2.50 s | — | GTA Online: un lavadero de coches en Los Santos |
| `K5_GTAV_Ruta68_Policia` | GTAV_PC_4K 16.65-17.60 ×2.65 | 2.52 s | «prohibido» (1.ª de 1) | GTA V (60 fps): coche de policía por la Ruta 68 |
| `NUEVO_Twitch_Captura` | captura (otra persona) | 4 s | «Twitch» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Img_GTAO_Bicis` | Imagen:K5_GTAO_Bicis.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): jugadores con bicis bajo un puente |
| `K5_GTAO_Paso_Inferior` | GTAO_PS5_4K 41.75-43.70 ×1.3 | 2.54 s | — | Paso inferior de una autopista de Los Santos |
| `K5_Img_GTAO_Policia_Comisaria` | Imagen:K5_GTAO_Policia_Comisaria.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): coche patrulla frente a la comisaría |
| `K5_Img_GTAO_Desguace` | Imagen:K5_GTAO_Desguace.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): una calle con un desguace y una grúa |
| `K5_GTAO_Carretera_Noche` | GTAO_Weevil_4K 13.00-15.30 ×1.1 | 2.53 s | — | GTA Online: carretera de noche con un cartel |
| `K5_GTAO_Carretera_Monte` | GTAO_Vigero_4K 13.10-15.20 ×1.2 | 2.52 s | — | GTA Online: un coche por una carretera de montaña |
| `K5_Img_GTAO_Jugador_Noche` | Imagen:K5_GTAO_Jugador_Noche.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un personaje sentado sobre la ciudad de noche |
| `K5_GTAO_Granja_Aerea` | GTAO_Cluckin_4K 10.30-12.00 ×1.5 | 2.55 s | — | GTA Online: vista aérea de una granja |
| `NUEVO_Cfx_Comunicado` | captura (otra persona) | 4 s | «Cfx» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_GTAO_Taller_Bennys` | GTAO_PS5_4K 27.85-29.35 ×1.7 | 2.55 s | — | Taller de Benny's de noche |
| `K5_RDR2_Pueblo_Valentine` | RDR2_Gameplay_4K 20.15-22.60 ×1.05 | 2.57 s | «RedM» (1.ª de 1) | Red Dead Redemption 2 (para RedM): calle de Valentine |
| `K5_Img_GTAO_Coche_Policia` | Imagen:K5_GTAO_Coche_Policia.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): deportivo rojo con la policía detrás |
| `K5_Img_GTAO_Coche_Neon_PS5` | Imagen:K5_GTAO_Coche_Mojado.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): coche derrapando sobre asfalto mojado |

Rol: imágenes oficiales del artículo «Introducing nopixel V» del Newswire (Los Santos y dos personajes de Burger Shot), trabajos (reparto de pizza, lavadero), policía (persecución, Ruta 68, comisaría) y Valentine de RDR2 para RedM. Twitch y Cfx van con sus capturas.

### p04

```python
"planos": ["NUEVO_Reediciones_Logos", "K5_GTAO_Colinas_Amanecer", "K5_GTAO_Autopista_Bruma", "K5_GTAO_Avion_Contraluz", "K5_GTAO_Cartel_Licores", "K5_Img_GTAO_Todoterreno", "K5_Img_GTAO_Muscle", "K5_Img_GTAO_Derrape_PS5"],
"planos_en": [{"en": "catorce", "plano": "NUEVO_Reediciones_Logos"},
              {"en": "veintidós", "plano": "K5_Img_GTAO_Todoterreno"},
              {"en": "mapa", "plano": "K5_GTAO_Colinas_Amanecer"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Reediciones_Logos` | captura (otra persona) | 4 s | «catorce» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_GTAO_Colinas_Amanecer` | GTAO_PS5_4K 2.85-4.75 ×1.35 | 2.56 s | «mapa» (1.ª de 1) | Los Santos al amanecer desde las colinas (tráiler de PS5) |
| `K5_GTAO_Autopista_Bruma` | GTAO_PS5_4K 11.20-13.10 ×1.35 | 2.57 s | — | Autopista de Los Santos en la bruma (tráiler de PS5) |
| `K5_GTAO_Avion_Contraluz` | GTAO_PS5_4K 13.25-15.15 ×1.35 | 2.57 s | — | Un avión pasa a contraluz (tráiler de PS5) |
| `K5_GTAO_Cartel_Licores` | GTAO_PS5_4K 16.85-18.70 ×1.35 | 2.50 s | — | Cartel de una licorería (tráiler de PS5) |
| `K5_Img_GTAO_Todoterreno` | Imagen:K5_GTAO_Todoterreno.jpg | 4 s (imagen) | «veintidós» (1.ª de 1) | Imagen oficial 4K (Newswire, lanzamiento en PS5): todoterreno en un bosque |
| `K5_Img_GTAO_Muscle` | Imagen:K5_GTAO_Muscle_Car.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire, lanzamiento en PS5): coche quemando rueda |
| `K5_Img_GTAO_Derrape_PS5` | Imagen:K5_GTAO_Derrape.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire, precarga en PS5): coche derrapando |

Todo sale del lanzamiento de GTA V/Online en PS5 y Xbox Series (tráiler y artículo de marzo de 2022) y de su precarga. «Mapa» va anclado al plano de Los Santos desde las colinas.

### p05

```python
"planos": ["NUEVO_GTAPlus_Captura", "K5_Img_GTAPlus_Quedada", "K5_Img_GTAPlus_Superdeportivo", "K5_Img_GTAO_Pareja_Helicoptero", "K5_Img_GTAPlus_Oficina", "K5_Img_GTAO_Garaje_Deportivo", "K5_Img_GTAO_Hombre_Coche", "K5_Img_GTAO_Ruleta", "K5_Img_GTAO_Exposicion", "K5_Img_GTAO_Hidroavion", "K5_Img_GTAO_Deportivo_Noche"],
"planos_en": [{"en": "marzo", "plano": "NUEVO_GTAPlus_Captura"},
              {"en": "suscripción", "plano": "K5_Img_GTAPlus_Quedada"},
              {"en": "cuota", "plano": "K5_Img_GTAPlus_Superdeportivo"},
              {"en": "recompensas", "plano": "K5_Img_GTAO_Ruleta"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_GTAPlus_Captura` | captura (otra persona) | 4 s | «marzo» (1.ª de 2) | Captura web prevista en el guion (NUEVO_) |
| `K5_Img_GTAPlus_Quedada` | Imagen:K5_GTAPlus_Quedada.jpg | 4 s (imagen) | «suscripción» (1.ª de 1) | Imagen oficial 4K (Newswire, «Introducing GTA+»): quedada de coches en un garaje |
| `K5_Img_GTAPlus_Superdeportivo` | Imagen:K5_GTAPlus_Superdeportivo.jpg | 4 s (imagen) | «cuota» (1.ª de 1) | Imagen oficial 4K (Newswire, «Introducing GTA+»): superdeportivo rojo |
| `K5_Img_GTAO_Pareja_Helicoptero` | Imagen:K5_GTAO_Pareja_Helicoptero.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): una pareja junto a su helicóptero |
| `K5_Img_GTAPlus_Oficina` | Imagen:K5_GTAPlus_Oficina.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire, «Introducing GTA+»): un ejecutivo en su oficina |
| `K5_Img_GTAO_Garaje_Deportivo` | Imagen:K5_GTAO_Garaje_Deportivo.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un deportivo en un garaje iluminado |
| `K5_Img_GTAO_Hombre_Coche` | Imagen:K5_GTAO_Hombre_Coche.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un personaje junto a su deportivo |
| `K5_Img_GTAO_Ruleta` | Imagen:K5_GTAO_Ruleta_Casino.jpg | 4 s (imagen) | «recompensas» (1.ª de 1) | Imagen oficial 4K (Newswire): un personaje al teléfono junto a la ruleta del casino |
| `K5_Img_GTAO_Exposicion` | Imagen:K5_GTAO_Exposicion.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): un coche en una sala de exposición |
| `K5_Img_GTAO_Hidroavion` | Imagen:K5_GTAO_Hidroavion.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): hidroavión sobre la bahía |
| `K5_Img_GTAO_Deportivo_Noche` | Imagen:K5_GTAO_Deportivo_Noche.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire): deportivo de noche con una explosión al fondo |

Imágenes oficiales del artículo «Introducing GTA+ for GTA Online» y de ventajas de miembros (garaje, coches, ruleta). No hay vídeo de GTA+ sin logo: van imágenes con zoom lento.

### p06

```python
"planos": ["K5_RDR2_Campamento", "K5_RDR2_Desierto_Cactus", "K5_RDR2_Bosque", "K5_RDR2_Pueblo_Ocaso", "K5_RDR2_Tren_Puente", "K5_RDR2_Pantano_Garza", "K5_RDR2_Puente_Cuerda", "K5_RDR2_Paisaje_Amanecer", "K5_RDR2_Pueblo_Atardecer", "K5_RDR2_Arthur_Caballo", "K5_RDR2_Ciervo_Bosque", "K5_RDR2_Pueblo_Caballo", "K5_RDR2_Bosque_Niebla", "K5_RDR2_Saint_Denis", "K5_RDR2_Arbol_Noche", "K5_RDR2_Valle_Lago"],
"planos_en": [{"en": "Redemption", "plano": "K5_RDR2_Campamento"},
              {"en": "western", "plano": "K5_RDR2_Desierto_Cactus"},
              {"en": "Morgan", "plano": "K5_RDR2_Arthur_Caballo"},
              {"en": "banda", "plano": "K5_RDR2_Arbol_Noche"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_RDR2_Campamento` | RDR2_4K 0.15-3.85 | 3.70 s | «Redemption» (1.ª de 1) | RDR2: el campamento de la banda bajo los árboles |
| `K5_RDR2_Desierto_Cactus` | RDR2_PC_4K 3.60-7.65 | 4.05 s | «western» (1.ª de 1) | RDR2: desierto con cactus |
| `K5_RDR2_Bosque` | RDR2_PC_4K 14.95-17.40 ×1.05 | 2.57 s | — | RDR2: bosque con montañas al fondo |
| `K5_RDR2_Pueblo_Ocaso` | RDR2_PC_4K 37.90-39.55 ×1.55 | 2.56 s | — | RDR2: un pueblo al ocaso |
| `K5_RDR2_Tren_Puente` | RDR2_Gameplay_4K 22.90-25.28 ×1.1 | 2.62 s | — | RDR2: un tren cruza un puente |
| `K5_RDR2_Pantano_Garza` | RDR2_PC_4K 20.05-22.45 ×1.05 | 2.52 s | — | RDR2: una garza en el pantano |
| `K5_RDR2_Puente_Cuerda` | RDR2_PC_4K 22.60-25.00 ×1.05 | 2.52 s | — | RDR2: un jinete cruza un puente colgante |
| `K5_RDR2_Paisaje_Amanecer` | RDR2_Gameplay_4K 30.44-34.40 | 3.96 s | — | RDR2: paisaje al amanecer |
| `K5_RDR2_Pueblo_Atardecer` | RDR2_PC_4K 46.10-48.85 | 2.75 s | — | RDR2: un pueblo del oeste a contraluz |
| `K5_RDR2_Arthur_Caballo` | RDR2_Gameplay_4K 35.00-36.86 ×1.35 | 2.51 s | «Morgan» (1.ª de 1) | RDR2: Arthur Morgan a caballo en la montaña |
| `K5_RDR2_Ciervo_Bosque` | RDR2_Gameplay_4K 78.50-80.70 ×1.15 | 2.53 s | — | RDR2: un ciervo en el bosque |
| `K5_RDR2_Pueblo_Caballo` | RDR2_Gameplay_4K 25.45-27.80 ×1.1 | 2.59 s | — | RDR2: un jinete por la calle de un pueblo |
| `K5_RDR2_Bosque_Niebla` | RDR2_PC_4K 17.55-19.85 ×1.1 | 2.53 s | — | RDR2: bosque con niebla |
| `K5_RDR2_Saint_Denis` | RDR2_Gameplay_4K 100.75-103.36 | 2.61 s | — | RDR2: Saint Denis de noche |
| `K5_RDR2_Arbol_Noche` | RDR2_PC_4K 49.00-52.40 | 3.40 s | «banda» (1.ª de 1) | RDR2: un caballo junto a una hoguera bajo un árbol de noche |
| `K5_RDR2_Valle_Lago` | RDR2_Gameplay_4K 90.00-92.45 ×1.05 | 2.57 s | — | RDR2: valle con lago y montañas nevadas |

RDR2: campamento de la banda, paisajes del oeste (desierto, bosque, pantano, Saint Denis) y Arthur Morgan a caballo para «Morgan».

### p07

```python
"planos": ["K5_RDO_Jinetes_Silueta", "K5_RDO_Jinetes_Galope", "NUEVO_RDO_Captura", "K5_RDO_Cabana", "K5_RDO_Jinete_Ocaso", "K5_RDO_Ruedas_Carro", "K5_RDO_Jinete_Nieve", "K5_RDO_Bosque_Nevado", "K5_RDO_Mirador", "K5_RDO_Tren_Ocaso", "K5_RDO_Canon_Jinetes", "K5_RDO_Contrabajo", "K5_RDO_Casa_Grupo", "K5_RDO_Noche_Luna"],
"planos_en": [{"en": "beta", "plano": "K5_RDO_Jinetes_Silueta"},
              {"en": "online", "plano": "NUEVO_RDO_Captura"},
              {"en": "lugar", "plano": "K5_RDO_Mirador"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_RDO_Jinetes_Silueta` | RDO_Lanz_4K 2.75-4.50 ×1.45 | 2.54 s | «beta» (1.ª de 1) | Red Dead Online: jinetes a contraluz al atardecer |
| `K5_RDO_Jinetes_Galope` | RDO_Lanz_4K 4.65-6.50 ×1.35 | 2.50 s | — | Red Dead Online: jinetes al galope |
| `NUEVO_RDO_Captura` | captura (otra persona) | 4 s | «online» (1.ª de 3) | Captura web prevista en el guion (NUEVO_) |
| `K5_RDO_Cabana` | RDO_Lanz_4K 21.40-23.70 ×1.1 | 2.53 s | — | Red Dead Online: un hombre frente a una cabaña |
| `K5_RDO_Jinete_Ocaso` | RDO_Beta_4K 4.10-5.80 ×1.5 | 2.55 s | — | Red Dead Online: un jinete al ocaso |
| `K5_RDO_Ruedas_Carro` | RDO_Beta_4K 7.15-9.15 ×1.25 | 2.50 s | — | Red Dead Online: ruedas de un carro a contraluz |
| `K5_RDO_Jinete_Nieve` | RDO_Beta_4K 17.00-18.60 ×1.6 | 2.56 s | — | Red Dead Online: un jinete por la nieve |
| `K5_RDO_Bosque_Nevado` | RDO_Naturalist_4K 9.20-11.40 ×1.15 | 2.53 s | — | Red Dead Online: bosque nevado |
| `K5_RDO_Mirador` | RDO_Naturalist_4K 27.00-28.80 ×1.4 | 2.52 s | «lugar» (1.ª de 1) | Red Dead Online: jinetes en un mirador |
| `K5_RDO_Tren_Ocaso` | RDO_BloodMoney_4K 6.70-8.50 ×1.4 | 2.52 s | — | Red Dead Online: un tren y jinetes al ocaso |
| `K5_RDO_Canon_Jinetes` | RDO_BloodMoney_4K 22.60-24.50 ×1.35 | 2.56 s | — | Red Dead Online: jinetes en un cañón |
| `K5_RDO_Contrabajo` | RDO_Moonshiners_4K 26.00-28.80 | 2.80 s | — | Red Dead Online: músicos en un bar clandestino |
| `K5_RDO_Casa_Grupo` | RDO_Frontier_4K 4.60-7.00 ×1.05 | 2.52 s | — | Red Dead Online: un grupo frente a una casa |
| `K5_RDO_Noche_Luna` | RDO_Naturalist_4K 33.90-35.60 ×1.5 | 2.55 s | — | Red Dead Online: paisaje de noche con luna |

Red Dead Online: jinetes y carros al ocaso, un mirador para «un lugar al que volver», el bar de Moonshiners.

### p08

```python
"planos": ["NUEVO_Houser_Captura", "K5_GTAV_Lester_Plan", "K5_RDR2_Dutch_Arthur", "K5_RDR2_Hoguera_Guitarra", "K5_RDR2_Banda_Baile", "NUEVO_Absurd_Logo", "K5_RDR2_Campamento_Hoguera", "K5_RDR2_Campamento_Charla", "K5_RDR2_Arthur_Pueblo", "K5_RDR2_Torre_Silueta", "K5_RDR2_Lago_Chimeneas", "K5_RDR2_Banda_Pueblo", "K5_Img_JL_Abrazo_Skyline"],
"planos_en": [{"en": "Houser", "plano": "NUEVO_Houser_Captura"},
              {"en": "guionista", "plano": "K5_GTAV_Lester_Plan"},
              {"en": "Redemption", "plano": "K5_RDR2_Dutch_Arthur"},
              {"en": "Absurd", "plano": "NUEVO_Absurd_Logo"},
              {"en": "Sam", "plano": "K5_Img_JL_Abrazo_Skyline"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Houser_Captura` | captura (otra persona) | 4 s | «Houser» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_GTAV_Lester_Plan` | GTAV_PS5_4K 9.15-10.50 ×1.9 | 2.56 s | «guionista» (1.ª de 1) | GTA V: Michael y Franklin en casa de Lester (escena de la historia) |
| `K5_RDR2_Dutch_Arthur` | RDR2_4K 4.00-5.80 ×1.4 | 2.52 s | «Redemption» (1.ª de 1) | RDR2: Dutch y Arthur hablan en el bosque |
| `K5_RDR2_Hoguera_Guitarra` | RDR2_Gameplay_4K 152.10-155.00 | 2.90 s | — | RDR2: la banda canta con una guitarra junto a la hoguera |
| `K5_RDR2_Banda_Baile` | RDR2_4K 31.45-33.00 ×1.65 | 2.56 s | — | RDR2: la banda baila junto a la hoguera |
| `NUEVO_Absurd_Logo` | captura (otra persona) | 4 s | «Absurd» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_RDR2_Campamento_Hoguera` | RDR2_Gameplay_4K 126.30-130.50 | 4.20 s | — | RDR2: la banda alrededor de la hoguera del campamento |
| `K5_RDR2_Campamento_Charla` | RDR2_Gameplay_4K 108.50-113.30 | 4.80 s | — | RDR2: conversación en el campamento |
| `K5_RDR2_Arthur_Pueblo` | RDR2_Gameplay_4K 116.00-118.30 ×1.1 | 2.53 s | — | RDR2: Arthur en la calle de un pueblo |
| `K5_RDR2_Torre_Silueta` | RDR2_Gameplay_4K 105.02-106.60 ×1.6 | 2.53 s | — | RDR2: un hombre a contraluz junto a una torre |
| `K5_RDR2_Lago_Chimeneas` | RDR2_Gameplay_4K 82.95-85.60 | 2.65 s | — | RDR2: un lago con chimeneas humeando al fondo |
| `K5_RDR2_Banda_Pueblo` | RDR2_Gameplay_4K 64.60-67.20 | 2.60 s | — | RDR2: la banda camina por un pueblo |
| `K5_Img_JL_Abrazo_Skyline` | Imagen:K5_JL_Abrazo_Skyline.jpg | 4 s (imagen) | «Sam» (1.ª de 1) | Captura oficial 4K: Jason y Lucía con el skyline de Vice City (lo que hace hoy Rockstar) |

Bloque de capturas (Houser y Absurd). De apoyo, escenas de historia de los dos juegos que escribió Dan Houser: Lester con Michael y Franklin (GTA V) y la banda de Dutch (RDR2). Para «Sam sigue al frente», Jason y Lucía. Faltan las fotos de Commons que prepara otra persona (Sam y Dan Houser en panel lateral, Rockstar North).

### p09

```python
"planos": ["NUEVO_Ruffian_Captura", "K5_Lanz_Barco_Manos", "K5_Img_VC_Ciudad_Aerea", "K5_Img_Port_Gellhorn_Ocaso", "K5_Img_Grassrivers_Skyline", "K5_Img_VC_Persecucion_Noche", "K5_Img_Kalaga_Canon", "K5_Img_VC_Concierto", "K5_Img_Ambrosia_Moteros"],
"planos_en": [{"en": "crece", "plano": "K5_Img_VC_Ciudad_Aerea"},
              {"en": "octubre", "plano": "NUEVO_Ruffian_Captura"},
              {"en": "manos", "plano": "K5_Lanz_Barco_Manos"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Ruffian_Captura` | captura (otra persona) | 4 s | «octubre» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Lanz_Barco_Manos` | Lanz 10.05-11.85 ×1.4 | 2.52 s | «manos» (1.ª de 1) | GTA VI: dos hombres trabajan en un barco en el taller |
| `K5_Img_VC_Ciudad_Aerea` | Imagen:K5_VC_Ciudad_Aerea.jpg | 4 s (imagen) | «crece» (1.ª de 1) | Captura oficial 4K: Vice City desde el aire |
| `K5_Img_Port_Gellhorn_Ocaso` | Imagen:K5_Port_Gellhorn_Ocaso.jpg | 4 s (imagen) | — | Captura oficial 4K: Port Gellhorn al ocaso |
| `K5_Img_Grassrivers_Skyline` | Imagen:K5_Grassrivers_Skyline.jpg | 4 s (imagen) | — | Captura oficial 4K: los pantanos de Grassrivers con Vice City al fondo |
| `K5_Img_VC_Persecucion_Noche` | Imagen:K5_VC_Persecucion_Noche.jpg | 4 s (imagen) | — | Captura oficial 4K: persecución de noche por Vice City |
| `K5_Img_Kalaga_Canon` | Imagen:K5_Kalaga_Canon.jpg | 4 s (imagen) | — | Captura oficial 4K: cañón del parque nacional Mount Kalaga |
| `K5_Img_VC_Concierto` | Imagen:K5_VC_Concierto.jpg | 4 s (imagen) | — | Captura oficial 4K: un concierto multitudinario |
| `K5_Img_Ambrosia_Moteros` | Imagen:K5_Ambrosia_Moteros.jpg | 4 s (imagen) | — | Captura oficial 4K: moteros por Ambrosia |

Bloque de capturas (Ruffian/Dundee). Apoyo: dos hombres trabajando en un barco para «hacen falta manos» y capturas oficiales de la escala del mapa de GTA VI. Si llegan las fotos de Dundee de Commons, pueden sustituir a las dos últimas imágenes.

### p10

```python
"planos": ["K5_Tril_SA_Desierto", "K5_Tril_GTA3_Tren", "K5_Img_Tril_VC_Calle", "K5_Tril_SA_Grove", "K5_Img_Tril_SA_Ciudad", "K5_Tril_SA_Casinos", "K5_Tril_GTA3_Lluvia", "K5_Tril_SA_Casa"],
"planos_en": [{"en": "Trilogy", "plano": "K5_Tril_SA_Desierto"},
              {"en": "Vice", "plano": "K5_Img_Tril_VC_Calle"},
              {"en": "veinte", "plano": "K5_Tril_GTA3_Lluvia"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Tril_SA_Desierto` | Trilogy_4K 3.00-6.20 | 3.20 s | «Trilogy» (1.ª de 1) | The Trilogy: San Andreas, desierto al atardecer |
| `K5_Tril_GTA3_Tren` | Trilogy_4K 11.95-14.70 | 2.75 s | — | The Trilogy: GTA III, tren elevado de Liberty City |
| `K5_Img_Tril_VC_Calle` | Imagen:K5_Trilogy_VC_Calle.jpg | 4 s (imagen) | «Vice» (1.ª de 1) | Imagen oficial 4K (Newswire, The Trilogy), recortada sin el logo: Ocean Drive de Vice City de noche |
| `K5_Tril_SA_Grove` | Trilogy_4K 21.60-23.50 ×1.35 | 2.56 s | — | The Trilogy: San Andreas, Grove Street |
| `K5_Img_Tril_SA_Ciudad` | Imagen:K5_Trilogy_SA_Ciudad.jpg | 4 s (imagen) | — | Imagen oficial 4K (Newswire, The Trilogy), recortada sin el logo: Los Santos de San Andreas al atardecer |
| `K5_Tril_SA_Casinos` | Trilogy_4K 23.65-26.95 | 3.30 s | — | The Trilogy: San Andreas, casinos de Las Venturas |
| `K5_Tril_GTA3_Lluvia` | Trilogy_4K 28.55-31.40 | 2.85 s | «veinte» (1.ª de 1) | The Trilogy: GTA III, coche bajo la lluvia |
| `K5_Tril_SA_Casa` | Trilogy_4K 46.15-47.75 ×1.6 | 2.56 s | — | The Trilogy: San Andreas, CJ en casa |

Los tres juegos de la trilogía en su versión remasterizada: desierto de San Andreas, tren de Liberty City, Grove Street, casinos de Las Venturas, lluvia en GTA III y dos imágenes oficiales del lanzamiento recortadas sin el logo.

### p11

```python
"planos": ["K5_Mir_Monitores", "K5_Mir_Vestibulo", "NUEVO_Texto_Hechos", "K5_Img_Motel_Noche", "K5_Img_Lucia_Esposada", "K5_Mir_Telefono", "K5_Mir_Pasillo", "K5_Mir_Coche_Oscuro"],
"planos_en": [{"en": "sistemas", "plano": "K5_Mir_Monitores"},
              {"en": "fianza", "plano": "NUEVO_Texto_Hechos"},
              {"en": "hotel", "plano": "K5_Img_Motel_Noche"},
              {"en": "teléfono", "plano": "K5_Mir_Telefono"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Mir_Monitores` | Mirada4K 1333.00-1338.50 | 5.50 s | «sistemas» (1.ª de 1) | GTA VI: una sala de seguridad con monitores, a oscuras |
| `K5_Mir_Vestibulo` | Mirada4K 24.50-30.00 | 5.50 s | — | GTA VI: un grupo en un vestíbulo (partida en bruto) |
| `NUEVO_Texto_Hechos` | captura (otra persona) | 4 s | «fianza» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Img_Motel_Noche` | Imagen:K5_Motel_Noche.jpg | 4 s (imagen) | «hotel» (1.ª de 1) | Captura oficial 4K: un motel de noche |
| `K5_Img_Lucia_Esposada` | Imagen:K5_Lucia_Esposada.jpg | 4 s (imagen) | — | Captura oficial 4K: Lucía esposada con el uniforme de presa |
| `K5_Mir_Telefono` | Mirada4K 222.75-225.42 | 2.67 s | «teléfono» (1.ª de 1) | GTA VI: un teléfono sobre una mesa |
| `K5_Mir_Pasillo` | Mirada4K 55.00-59.50 | 4.50 s | — | GTA VI: un pasillo de un edificio (partida en bruto) |
| `K5_Mir_Coche_Oscuro` | Mirada4K 894.48-897.95 | 3.47 s | — | GTA VI: dentro de un coche a oscuras |

Sin material de la filtración (no se enseña lo robado). GTA VI «en bruto» del An Extended Look (vestíbulo, pasillo, coche) y tres objetos de la frase: sala de seguridad con monitores («sistemas»), motel de noche («hotel») y teléfono («teléfono»). Lucía esposada para «libertad bajo fianza».

### p12

```python
"planos": ["K5_Mir_Calle_Club", "K5_Img_VC_Noria_Noche", "K5_Lanz_Preparativos", "NUEVO_Juicio_Southwark", "K5_Mir_Coche_Pista", "K5_Img_JL_Conduce_Noche", "K5_Img_VC_Peluqueria", "K5_Img_VC_Gasolinera_Noche", "K5_Mir_Pista_Avion", "K5_Img_Ambrosia_Noche", "K5_Img_VC_Skyline_Noche"],
"planos_en": [{"en": "confirma", "plano": "K5_Img_VC_Noria_Noche"},
              {"en": "trabajo", "plano": "K5_Mir_Calle_Club"},
              {"en": "Londres", "plano": "NUEVO_Juicio_Southwark"},
              {"en": "millones", "plano": "K5_Img_VC_Skyline_Noche"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Mir_Calle_Club` | Mirada4K 1241.00-1243.69 | 2.69 s | «trabajo» (1.ª de 2) | GTA VI: calle con un club de noche |
| `K5_Img_VC_Noria_Noche` | Imagen:K5_VC_Noria_Noche.jpg | 4 s (imagen) | «confirma» (1.ª de 1) | Captura oficial 4K: Vice City de noche con la noria |
| `K5_Lanz_Preparativos` | Lanz 30.90-32.70 ×1.4 | 2.52 s | — | GTA VI: preparativos a oscuras |
| `NUEVO_Juicio_Southwark` | captura (otra persona) | 4 s | «Londres» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Mir_Coche_Pista` | Mirada4K 1202.98-1207.00 | 4.02 s | — | GTA VI: dentro de un coche de noche |
| `K5_Img_JL_Conduce_Noche` | Imagen:K5_JL_Conduce_Noche.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason conduce de noche con Lucía |
| `K5_Img_VC_Peluqueria` | Imagen:K5_VC_Barberia.jpg | 4 s (imagen) | — | Captura oficial 4K: una barbería de Vice City |
| `K5_Img_VC_Gasolinera_Noche` | Imagen:K5_VC_Gasolinera_Noche.jpg | 4 s (imagen) | — | Captura oficial 4K: gasolinera de noche |
| `K5_Mir_Pista_Avion` | Mirada4K 1185.71-1191.00 | 5.29 s | — | GTA VI: un avión privado en la pista de noche |
| `K5_Img_Ambrosia_Noche` | Imagen:K5_Ambrosia_Noche.jpg | 4 s (imagen) | — | Captura oficial 4K: Ambrosia de noche |
| `K5_Img_VC_Skyline_Noche` | Imagen:K5_VC_Skyline_Noche.jpg | 4 s (imagen) | «millones» (1.ª de 1) | Captura oficial 4K: skyline de Vice City de noche |

GTA VI de noche como fondo de la nota de Rockstar y del juicio; la foto de Southwark (Commons) va con `NUEVO_Juicio_Southwark`.

### p13

```python
"planos": ["K5_T1_Lucia_Ventana", "K5_Img_VC_Letras", "K5_T1_Playa_Paseo", "K5_Img_Lucia_Calle", "K5_Img_VC_Neones_Policia", "K5_Img_JL_Baile_Neon", "K5_PreLoad_Club_Neon", "K5_Img_VC_Coche_Rosa"],
"planos_en": [{"en": "diciembre", "plano": "K5_T1_Lucia_Ventana"},
              {"en": "Vice", "plano": "K5_Img_VC_Letras"},
              {"en": "Petty", "plano": "K5_Img_VC_Neones_Policia"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_T1_Lucia_Ventana` | T1 6.60-8.40 ×1.4 | 2.52 s | «diciembre» (1.ª de 1) | Tráiler 1: Lucía mira por la ventana |
| `K5_Img_VC_Letras` | Imagen:K5_VC_Letras.jpg | 4 s (imagen) | «Vice» (1.ª de 1) | Captura oficial 4K: las letras de VICE CITY con una avioneta |
| `K5_T1_Playa_Paseo` | T1 21.80-23.20 ×1.8 | 2.52 s | — | Tráiler 1: paseo por la playa |
| `K5_Img_Lucia_Calle` | Imagen:K5_Lucia_Calle.jpg | 4 s (imagen) | — | Captura oficial 4K: Lucía por una calle de Vice City |
| `K5_Img_VC_Neones_Policia` | Imagen:K5_VC_Neones_Policia.jpg | 4 s (imagen) | «Petty» (1.ª de 1) | Captura oficial 4K: neones de Ocean Drive de noche |
| `K5_Img_JL_Baile_Neon` | Imagen:K5_JL_Baile_Neon.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason y Lucía bailan entre neones |
| `K5_PreLoad_Club_Neon` | PreLoad 2.75-5.15 ×1.05 | 2.52 s | — | Pre-Load Now: luces de neón en un club |
| `K5_Img_VC_Coche_Rosa` | Imagen:K5_VC_Coche_Rosa.jpg | 4 s (imagen) | — | Captura oficial 4K: un coche rosa entre palmeras |

Tráiler 1 (Lucía en prisión, la playa) y Vice City: las letras de VICE CITY para «Vuelve Vice City» y los neones de Ocean Drive para Tom Petty. Hay que quitar `intro_original: T1_Musica_Petty` y el ancla `petty → T1_Musica_Petty` (ya usados en otros vídeos).

### p14

```python
"planos": ["K5_T2_Jason_Noche", "K5_T2_Torre_Prision", "K5_T2_Reencuentro", "K5_T2_Moto_Avioneta", "K5_Img_JL_Moto_Helicoptero", "K5_Img_Jason_Noche", "K5_Img_VC_Puerto"],
"planos_en": [{"en": "mayo", "plano": "K5_T2_Jason_Noche"},
              {"en": "Pointer", "plano": "K5_T2_Reencuentro"},
              {"en": "diecinueve", "plano": "K5_Img_VC_Puerto"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_T2_Jason_Noche` | T2 45.35-49.75 | 4.40 s | «mayo» (1.ª de 2) | Tráiler 2: Jason conduce de noche entre coches de policía |
| `K5_T2_Torre_Prision` | T2 49.90-51.80 ×1.35 | 2.56 s | — | Tráiler 2: torre de vigilancia de la prisión |
| `K5_T2_Reencuentro` | T2 66.30-69.60 | 3.30 s | «Pointer» (1.ª de 1) | Tráiler 2: Lucía y Jason junto al coche |
| `K5_T2_Moto_Avioneta` | T2 141.90-143.65 ×1.45 | 2.54 s | — | Tráiler 2: un motorista y una avioneta |
| `K5_Img_JL_Moto_Helicoptero` | Imagen:K5_JL_Huida_Moto.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason y Lucía huyen en moto con un helicóptero detrás |
| `K5_Img_Jason_Noche` | Imagen:K5_Jason_Noche.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason de noche junto a un bar con neones |
| `K5_Img_VC_Puerto` | Imagen:K5_VC_Puerto.jpg | 4 s (imagen) | «diecinueve» (1.ª de 1) | Captura oficial 4K: el puerto deportivo de Vice City |

Tráiler 2 sin estrenar: Jason conduciendo entre la policía, la prisión, el reencuentro de Lucía y Jason (para The Pointer Sisters, que suenan en ese tráiler) y el motorista con la avioneta.

### p15

```python
"planos": ["NUEVO_Schreier_Bluesky", "K5_Img_Brian_Papeles", "K5_Mir_Sofa", "K5_Img_Boobie_Despacho", "K5_Img_DreQuan_Estudio", "K5_Img_Raul_Telefono", "K5_Img_Jason_Mesa", "K5_Img_Cal_Billar"],
"planos_en": [{"en": "Schreier", "plano": "NUEVO_Schreier_Bluesky"},
              {"en": "crunch", "plano": "K5_Mir_Sofa"},
              {"en": "oficina", "plano": "K5_Img_Boobie_Despacho"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Schreier_Bluesky` | captura (otra persona) | 4 s | «Schreier» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Img_Brian_Papeles` | Imagen:K5_Brian_Papeles.jpg | 4 s (imagen) | — | Captura oficial 4K: Brian lee unos papeles |
| `K5_Mir_Sofa` | Mirada4K 1144.50-1147.25 | 2.75 s | «crunch» (1.ª de 1) | GTA VI: dos hombres sentados en un sofá |
| `K5_Img_Boobie_Despacho` | Imagen:K5_Boobie_Despacho.jpg | 4 s (imagen) | «oficina» (1.ª de 1) | Captura oficial 4K: Boobie en su despacho |
| `K5_Img_DreQuan_Estudio` | Imagen:K5_DreQuan_Estudio.jpg | 4 s (imagen) | — | Captura oficial 4K: DreQuan en un estudio de grabación |
| `K5_Img_Raul_Telefono` | Imagen:K5_Raul_Telefono.jpg | 4 s (imagen) | — | Captura oficial 4K: Raúl habla por teléfono de noche |
| `K5_Img_Jason_Mesa` | Imagen:K5_Jason_Mesa.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason en una mesa de un bar |
| `K5_Img_Cal_Billar` | Imagen:K5_Cal_Billar.jpg | 4 s (imagen) | — | Captura oficial 4K: Cal juega al billar |

Bloque de capturas (Schreier). Apoyo: personajes de GTA VI en interiores de trabajo (despacho, papeles, estudio, teléfono) para «crunch» y «oficina».

### p16

```python
"planos": ["NUEVO_Zelnick_Captura", "K5_Img_VC_Torres_Bahia", "K5_Img_Raul_Barco", "K5_PreLoad_Yate", "K5_Img_VC_Piscina_Aerea", "K5_T2_Moto_Agua", "K5_Img_Keys_Barcos", "K5_Img_JL_Coche", "K5_Img_Jason_Pesca", "K5_Img_Lucia_Piscina"],
"planos_en": [{"en": "Zelnick", "plano": "NUEVO_Zelnick_Captura"},
              {"en": "perfección", "plano": "K5_Img_VC_Torres_Bahia"},
              {"en": "diecinueve", "plano": "K5_Img_JL_Coche"},
              {"en": "récords", "plano": "K5_Img_Keys_Barcos"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `NUEVO_Zelnick_Captura` | captura (otra persona) | 4 s | «Zelnick» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_Img_VC_Torres_Bahia` | Imagen:K5_VC_Torres_Bahia.jpg | 4 s (imagen) | «perfección» (1.ª de 1) | Captura oficial 4K: torres sobre la bahía de Vice City |
| `K5_Img_Raul_Barco` | Imagen:K5_Raul_Barco.jpg | 4 s (imagen) | — | Captura oficial 4K: Raúl en la cubierta de un barco al atardecer |
| `K5_PreLoad_Yate` | PreLoad 11.25-12.60 ×1.85 | 2.50 s | — | Pre-Load Now: un yate en la bahía |
| `K5_Img_VC_Piscina_Aerea` | Imagen:K5_VC_Piscina_Aerea.jpg | 4 s (imagen) | — | Captura oficial 4K: piscina de un hotel desde el aire |
| `K5_T2_Moto_Agua` | T2 140.10-141.80 ×1.5 | 2.55 s | — | Tráiler 2: una moto de agua |
| `K5_Img_Keys_Barcos` | Imagen:K5_Keys_Barcos.jpg | 4 s (imagen) | «récords» (1.ª de 1) | Captura oficial 4K: fiesta de barcos en los Cayos |
| `K5_Img_JL_Coche` | Imagen:K5_JL_Coche.jpg | 4 s (imagen) | «diecinueve» (1.ª de 1) | Captura oficial 4K: Jason y Lucía en el coche |
| `K5_Img_Jason_Pesca` | Imagen:K5_Jason_Pesca.jpg | 4 s (imagen) | — | Captura oficial 4K: Jason pesca desde un barco |
| `K5_Img_Lucia_Piscina` | Imagen:K5_Lucia_Piscina.jpg | 4 s (imagen) | — | Captura oficial 4K: Lucía en una piscina |

Bloque de capturas (Zelnick). Apoyo: las imágenes más pulidas de GTA VI para «perfección» y «récords», Jason y Lucía para la fecha.

### p17

```python
"planos": ["K5_Img_JL_Atardecer_Bolsas", "K5_PreLoad_Breakdance", "K5_Img_GTAO_Coche_Explosion", "K5_Img_Kalaga_Fauna", "K5_Lanz_Pantano_Siluetas", "K5_Img_Keys_Iguana", "NUEVO_VGD_Captura", "K5_LANoire_Phelps", "K5_Img_Kalaga_Helicoptero", "K5_Img_JL_Silueta_Atardecer", "K5_Img_VC_Grafiti", "K5_Img_Keys_Calle", "K5_Img_Port_Gellhorn_Coche", "K5_Img_Keys_Bar"],
"planos_en": [{"en": "diecinueve", "plano": "K5_Img_JL_Atardecer_Bolsas"},
              {"en": "Trece", "plano": "K5_Img_GTAO_Coche_Explosion"},
              {"en": "Sídney", "plano": "NUEVO_VGD_Captura"},
              {"en": "Bondi", "plano": "K5_LANoire_Phelps"},
              {"en": "espera", "plano": "K5_Img_JL_Silueta_Atardecer"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Img_JL_Atardecer_Bolsas` | Imagen:K5_JL_Atardecer_Bolsas.jpg | 4 s (imagen) | «diecinueve» (1.ª de 1) | Captura oficial 4K: Jason y Lucía al atardecer |
| `K5_PreLoad_Breakdance` | PreLoad 5.25-6.75 ×1.7 | 2.55 s | — | Pre-Load Now: breakdance en el paseo marítimo |
| `K5_Img_GTAO_Coche_Explosion` | Imagen:K5_GTAV_Deportivo.jpg | 4 s (imagen) | «Trece» (1.ª de 2) | Imagen oficial 4K (Newswire): deportivo en Los Santos (para GTA V) |
| `K5_Img_Kalaga_Fauna` | Imagen:K5_Kalaga_Fauna.jpg | 4 s (imagen) | — | Captura oficial 4K: fauna junto al río en Mount Kalaga |
| `K5_Lanz_Pantano_Siluetas` | Lanz 27.90-29.35 ×1.75 | 2.54 s | — | Lanzamiento: siluetas en el pantano al atardecer |
| `K5_Img_Keys_Iguana` | Imagen:K5_Keys_Iguana.jpg | 4 s (imagen) | — | Captura oficial 4K: una iguana en los Cayos |
| `NUEVO_VGD_Captura` | captura (otra persona) | 4 s | «Sídney» (1.ª de 1) | Captura web prevista en el guion (NUEVO_) |
| `K5_LANoire_Phelps` | LANoire_4K 16.90-19.00 ×1.2 | 2.52 s | «Bondi» (1.ª de 1) | L.A. Noire 4K (reedición de 2017): Cole Phelps en comisaría |
| `K5_Img_Kalaga_Helicoptero` | Imagen:K5_Kalaga_Helicoptero.jpg | 4 s (imagen) | — | Captura oficial 4K: un helicóptero en Mount Kalaga |
| `K5_Img_JL_Silueta_Atardecer` | Imagen:K5_JL_Silueta_Atardecer.jpg | 4 s (imagen) | «espera» (1.ª de 1) | Captura oficial 4K: Jason y Lucía a contraluz al atardecer |
| `K5_Img_VC_Grafiti` | Imagen:K5_VC_Calle_Grafiti.jpg | 4 s (imagen) | — | Captura oficial 4K: calle con grafitis |
| `K5_Img_Keys_Calle` | Imagen:K5_Keys_Calle.jpg | 4 s (imagen) | — | Captura oficial 4K: una calle de los Cayos con un caimán |
| `K5_Img_Port_Gellhorn_Coche` | Imagen:K5_Port_Gellhorn_Coche.jpg | 4 s (imagen) | — | Captura oficial 4K: dos personajes en un coche en Port Gellhorn |
| `K5_Img_Keys_Bar` | Imagen:K5_Keys_Bar.jpg | 4 s (imagen) | — | Captura oficial 4K: un bar de playa en los Cayos |

GTA VI para el lanzamiento, una imagen de GTA V/Online para «Trece años después de GTA V», L.A. Noire 4K para Team Bondi y la reedición en la que trabajó Video Games Deluxe.

### cierre

```python
"planos": ["K5_Img_JL_Arbol_Atardecer", "K5_Img_JL_Lucia_Coche", "K5_Img_Kalaga_Kayak", "K5_Img_Grassrivers_Aldea", "K5_Img_Ambrosia_Ocaso", "K5_Img_Keys_Fondo", "K5_Img_VC_Rascacielos_Bahia"],
"planos_en": [{"en": "Trece", "plano": "K5_Img_JL_Arbol_Atardecer"},
              {"en": "comentarios", "plano": "K5_Img_JL_Lucia_Coche"}],
```

| Trozo | Fuente y tramo | En pantalla | Ancla | Por qué encaja |
|---|---|---|---|---|
| `K5_Img_JL_Arbol_Atardecer` | Imagen:K5_Arbol_Atardecer.jpg | 4 s (imagen) | «Trece» (1.ª de 1) | Captura oficial 4K: un árbol solo al atardecer |
| `K5_Img_JL_Lucia_Coche` | Imagen:K5_JL_Lucia_Coche.jpg | 4 s (imagen) | «comentarios» (1.ª de 1) | Captura oficial 4K: Lucía sonríe apoyada en el coche |
| `K5_Img_Kalaga_Kayak` | Imagen:K5_Kalaga_Kayak.jpg | 4 s (imagen) | — | Captura oficial 4K: un kayak por el río |
| `K5_Img_Grassrivers_Aldea` | Imagen:K5_Grassrivers_Aldea.jpg | 4 s (imagen) | — | Captura oficial 4K: casas sobre el agua en Grassrivers |
| `K5_Img_Ambrosia_Ocaso` | Imagen:K5_Ambrosia_Ocaso.jpg | 4 s (imagen) | — | Captura oficial 4K: torre eléctrica al ocaso en Ambrosia |
| `K5_Img_Keys_Fondo` | Imagen:K5_Keys_Fondo_Mar.jpg | 4 s (imagen) | — | Captura oficial 4K: fondo del mar en los Cayos |
| `K5_Img_VC_Rascacielos_Bahia` | Imagen:K5_VC_Azotea_Pareja.jpg | 4 s (imagen) | — | Captura oficial 4K: una pareja en una azotea sobre Vice City |

Capturas oficiales tranquilas de Leonida y de Jason y Lucía; ninguna escena violenta bajo «¿fue una espera justa?».

## c) Segundos de material por bloque

Voz estimada a 3,4 palabras/s. El montaje ya no alarga planos: se pide material ≥ 1,3 × voz. Las capturas `NUEVO_` cuentan 4 s (como en `trozos_57.csv`); las imágenes `K5_Img_*`, 4 s; el vídeo, lo que dura en pantalla (con `Lento`).

| Bloque | Palabras | Voz (s) | 1,3 × voz | Material (s) | Del cual capturas NUEVO_ | Margen |
|---|---|---|---|---|---|---|
| hook | 77 | 22.6 | 29.4 | 30.5 | 8 | 1.35 × |
| p01 | 87 | 25.6 | 33.3 | 38.9 | 0 | 1.52 × |
| p02 | 141 | 41.5 | 53.9 | 56.7 | 4 | 1.37 × |
| p03 | 161 | 47.4 | 61.6 | 67.8 | 8 | 1.43 × |
| p04 | 60 | 17.6 | 22.9 | 26.2 | 4 | 1.48 × |
| p05 | 107 | 31.5 | 40.9 | 44.0 | 4 | 1.40 × |
| p06 | 118 | 34.7 | 45.1 | 46.0 | 0 | 1.33 × |
| p07 | 81 | 23.8 | 31.0 | 37.2 | 4 | 1.56 × |
| p08 | 104 | 30.6 | 39.8 | 41.9 | 8 | 1.37 × |
| p09 | 89 | 26.2 | 34.0 | 34.5 | 4 | 1.32 × |
| p10 | 50 | 14.7 | 19.1 | 25.2 | 0 | 1.71 × |
| p11 | 86 | 25.3 | 32.9 | 33.6 | 4 | 1.33 × |
| p12 | 105 | 30.9 | 40.1 | 42.5 | 4 | 1.38 × |
| p13 | 61 | 17.9 | 23.3 | 27.6 | 0 | 1.54 × |
| p14 | 60 | 17.6 | 22.9 | 24.8 | 0 | 1.41 × |
| p15 | 70 | 20.6 | 26.8 | 30.8 | 4 | 1.49 × |
| p16 | 86 | 25.3 | 32.9 | 37.0 | 4 | 1.46 × |
| p17 | 125 | 36.8 | 47.8 | 51.6 | 4 | 1.40 × |
| cierre | 70 | 20.6 | 26.8 | 28.0 | 0 | 1.36 × |
| **Total** | | **511** | **665** | **725** | | **1.42 ×** |

Si alguna captura `NUEVO_` no llega, los bloques p08, p09, p11 y p15 son los que más dependen de ellas (8, 4, 4 y 4 s).

## d) Hojas de contacto

- `video_trece_anos/planos_4k_hojas/hoja_hook.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p01.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p02.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p03.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p04.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p05.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p06.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p07.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p08.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p09.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p10.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p11.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p12.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p13.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p14.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p15.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p16.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_p17.jpg`
- `video_trece_anos/planos_4k_hojas/hoja_cierre.jpg`

Cada hoja enseña el fotograma central de cada trozo de vídeo (sacado de la URL 4K) o la imagen, con el nombre del trozo. En bloques largos hay más de 8 miniaturas porque hace falta ese material para cubrir 1,3 × la voz.

## Cambios que necesita el guion o el montaje

- Sustituir `planos`/`planos_en` de cada bloque por los de la sección b; quitar todos los grupos `@GTA5_2013`, `@GTA_Online`, `@Historia_GTA`, `@VC_DE`, `@GTA6_*` y los planos de stock ya usados.
- p13: quitar `"intro_original": "T1_Musica_Petty"` y el ancla de «petty».
- p14: el ancla de «diecinueve» ya no va a `VL_Fecha` (texto «PRE-ORDER NOW»).
- Añadir las fuentes nuevas de la tabla a al diccionario de vídeos del montaje con su nombre corto (columna `Vídeo` del CSV).