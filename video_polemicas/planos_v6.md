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

## Material ya preparado y subido (15 nov, commit 7ab74b8)
Todo está en `video_largo/imagenes_4k/` y `video_largo/imagenes_2k/`, con prefijo K6_. Se ha comprobado por huella visual (dHash) que no lo usa ningún otro vídeo del canal: ramas videos-5-7 y videos-8-10.

**Oficiales 4K, `imagenes_4k`:**
- **The Trilogy** (rockstargames.com/GTATrilogy), 12 imágenes:
  - GTA III: K6_Tril_GTA3_Policia, _Lanzallamas, _Persecucion_Lluvia y _Coche_Puente (este, 1080p).
  - Vice City: K6_Tril_VC_Tommy_OceanView, _Hotel_Lluvia (1080p), _Tommy_Moto y _Tommy_Lance.
  - San Andreas: K6_Tril_SA_Coche_Noche, _Grove, _CJ_Lancha (1080p) y _CJ_Moto.
- **GTA V y GTA Online** (rockstargames.com/gta-v): K6_GTAV_Helicoptero, K6_GTAV_Ciudad_Palmeras, K6_GTAO_Personajes, K6_GTAO_Coche_Garaje y K6_GTAO_Coche_Rayas.
- **GTA VI** (GTAVI_Screenshots.zip, sin usar en el canal): K6_VI_Descapotable, Buzo_Cayos, Hidrodeslizador, Playa, Fiesta_Piscina, Minigolf, Jason_Moto, Jason_Coche, Bar, Lucia_Coche, Raul, Conversacion, Estudio, Jason_Conduce y Bosque.
- **Otras:** K6_Bully_Fondo (fondo de cómic de la web de Bully; solo para tarjetas) y K6_GTA1_Caratula (va en K6_Panel_GTA1).

**Capturas a 2560x1440, `imagenes_2k`.** Solo titular, fecha y, a veces, entradilla. Las hace scratchpad\capt6\comp2k.py con objetivos6.py.

| Archivo | Fuente |
|---|---|
| K6_Clifford_Killscreen | Kill Screen, 22 oct 2012 |
| K6_Hansard_Lores | Hansard, HL Deb 20 may 1997 |
| K6_VC_Demanda | Game Developer, 28 ene 2004 |
| K6_ESRB_AO | ESRB, 20 jul 2005 |
| K6_FTC_Acuerdo | FTC, 8 jun 2006 |
| K6_Bully_Juez | The Register, 13 oct 2006 |
| K6_Bully_Profesores | The Escapist, 4 mar 2008 |
| K6_Thompson_Cargos | Engadget, 25 sep 2008 |
| K6_Lohan_Fortune | Game Informer, 29 mar 2018 (sin fecha visible) |
| K6_Target_AFP | Game Developer, 3 dic 2014 |
| K6_OpenIV | Game Developer, 15 jun 2017 |
| K6_SharkCards_GI | Game Informer, 23 oct 2017 |
| K6_Trilogy_NME | NME, 19 nov 2021 |
| K6_Hackeo_Guardian | The Guardian, sep 2022 |
| K6_Despidos_Register | The Register, 6 nov 2025 |
| K6_Juicio_Aftermath | Aftermath, 10 sep 2026 |
| K6_MiamiBeach_WLRN | WLRN, 24 sep 2026 |

Falta una captura para el bloque 8 (tortura, 2013): NBC News o CNBC.

**Tarjetas propias.** Las genera capt6\tarjetas6.py; cada una lleva su fuente en la tarjeta:
- K6_Tarjeta_Clifford, _Brasil, _11S, _HotCoffee, _Australia, _Bully_Juez, _Thompson, _Target, _OpenIV, _Despidos, _Miami y _Formula.
- K6_Panel_GTA1.

**Commons**, en `imagenes_2k`; autor y licencia comprobados por la API:

| Archivo | Original | Autor y licencia |
|---|---|---|
| K6_Foto_Supremo_Florida | «Florida-Supreme-Court-with-Bunting-2019.jpg» | Bruin79, CC0 |
| K6_Foto_Juzgado_MiamiDade | «The Miami Dade County Flagler Courthouse.jpg» | Rob Olivera, CC BY 2.0 |
| K6_Foto_MiamiBeach_Noche | «Marina and city skyline at night, Miami Beach, Florida.jpg» | Z3lvs, CC0 |

## Tramos de vídeo 4K libres elegidos
Ninguno se solapa con los de otros vídeos del canal. Cortes medidos con escena ≥ 0,10 sobre el 720p.

| Fuente | Tramos (s) |
|---|---|
| Trilogy_4K (8ta2r546) | 20.25-21.38 Vinewood · 27.15-28.35 coche bajo la lluvia · 36.12-37.31 CJ y coche · 47.92-49.15 coche volando |
| Bully_Aniv (totcka8o, 1080p) | 0.82-5.52 tarjeta ESRB «Teen» · 10.10-11.83 logo de Bully |
| GTAV_PS5_4K (r3too449, bandas 0.1) | 4.2-7.2 logo de GTA V sobre la ciudad · 32.4-33.5 avión y montañas · 45.8-46.8 Trevor en casa |
| GTAO_CE_4K (8rakra67, sin bandas) | 0.1-6.0 Los Santos desde el aire · 6.2-8.0 skyline al atardecer · 10.4-12.2 autopista · 23.4-24.4 torre y palmera · 28.5-30.0 barcos y puente · 36.4-37.6 helicóptero y contenedor · 41.0-42.1 coche calavera |
| GTAO_PS5_4K (1s626s55, sin bandas) | 15.3-16.6 hangar · 26.6-27.6 lowriders · 32.1-33.3 faro · 46.3-48.0 puente y ciudad |
| GTAO_Safehouse_4K (to78rk1o) | 2.1-4.0 casa en las colinas · 6.3-7.4 villa · 25.6-26.8 barco al atardecer · 37.2-38.5 Michael · 41.5-44.5 calle de noche · 45.8-46.8 moto de agua · 50.0-51.1 taxis · 51.4-52.8 policía y camión |
| GTAO_Cluckin_4K (r3175t5r) | 7.7-9.1 policía hablando · 13.7-14.8 todoterreno · 15.0-16.6 fila de policías |
| GTAO_Vigero_4K (k1t75kk6) | 3.7-5.0 calle · 6.8-8.0 derrape · 11.3-12.9 túnel |
| GTAO_Kanjo_4K (3ra4t562) | 3.6-5.2 coche al atardecer · 9.8-11.8 derrape |
| GTAO_Bounties_4K (oa46rs8r) | 2.1-3.5 · 10.0-11.3 |
| GTAO_Sabotage_4K (r50k6mmg) | 5.5-6.7 conversación |
| GTAO_Pizza_4K (aro34sg4) | 7.6-8.8 calle con palmeras |
| GTAO_Luiva_4K (203as2rs) | 7.6-8.8 carretera del desierto |

## Siguiente paso
1. Escribir `trozos_pol_4k.csv` con el prefijo K6_ y añadirlo a la lista de CSV de montaje.py.
2. Poner los planos nuevos en guion_pol.py:
   - VIDEOS_EXTRA con las fuentes de arriba; FUENTES_REMOTAS, SIN_BANDAS y LENTO_MAX como en guion_13a.
   - Quitar el import de guion_vc, guion_sg y guion_jl, que traen las URL de archive.org.
   - Quitar intro_original G1_Demo1_01 y G3_DE_01.
3. Arreglar en el montaje el título del bloque cuando el primer plano es una captura web.
4. Previa con bloques=hook,p01,p02 (con voz provisional si las voces aún no están).

## Pendiente
- **Voces:** 16 voces nuevas: hook, p01, p02, p03, p06, p07, p08, p09, p10, p11, p12, p14, p14b, p15, p16 y cierre. Se pide desde las 9:00 de Madrid (8:00 UTC), con cola_voces.yml o voces_video.yml.
- **Despidos:** antes de publicar, comprobar si ya hay sentencia en el juicio de Glasgow (bloque 14b).
- **Música:** lista de 10-15 pistas libres por estilo (FreePD, Pixabay sin Content ID, Incompetech CC BY) para que el usuario elija.
- **Tarjeta de YouTube:** se pone en Studio, en el bloque 14, apuntando al vídeo 5.
