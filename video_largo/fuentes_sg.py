"""Vídeos de cada juego para el vídeo 3 («Toda la historia de GTA: de 1997 a GTA 6»).

Dos tipos de fuente:
  - Tráileres oficiales de Rockstar (rockstargames.com/videos), en 720p o 1080p.
  - Partidas completas subidas a archive.org con licencia libre (CC BY 4.0): hay que citarlas en la descripción
    (ver CREDITOS). Son de 360p: el montaje las pone en un marco sobre una copia borrosa (MARCO = True en el guion).
Las partidas de varias horas se usan por tramos («tramos»): solo se bajan esos minutos.
preparar_trozos.py (FUENTES_MOD=fuentes_sg) elige los trozos y los deja en la rama trozos-sg
(workflow «Preparar trozos de los juegos (vídeo 3, la saga)», que se lanza solo al cambiar este archivo)."""
from fuentes_vc import RS, ia


def rs(ident, calidad):
    return f"{RS}{ident}/flv/en-us-{calidad}.mp4"


_G1 = "grand-theft-auto-1-play-station-pal-gameplay-full-game-longplay-recorded-by-joe-"
_G1_PRE = "Grand Theft Auto 1 PlayStation PAL Gameplay (Full "
_G3 = "grand-theft-auto-3-play-station-2-pal-gameplay-full-game-longplay-walkthrough-free-roam-part-01"
_G3_PRE = "Grand Theft Auto 3 PlayStation 2 PAL Gameplay (Full Game Longplay Walkthrough Free Roam Part "
_SA = "grand-theft-auto-san-andreas-play-station-2-pal-gameplay-full-game-longplay-walk"
_SA_PRE = "Grand Theft Auto San Andreas PlayStation 2 PAL Gameplay (Full Game Longplay Walkthrough Free Roam Extended With Cheats Codes Part "
_IV = "grand-theft-auto-4-windows-pc-pal-gameplay-full-game-longplay-recorded-by-gta-se"
_V = "grand-theft-auto-5-play-station-5-pal-gameplay-full-game-longplay-recorded-by-yo"

BASE = {
    # 1997 · Grand Theft Auto (PlayStation, partida y demostraciones de Joe Roberts, CC BY 4.0)
    "G1_PS": {"grupo": "GTA1_1997", "url": ia(_G1, _G1_PRE + "Game Longplay Recorded By Joe Roberts With Free Roam Liberty City Part 01).mp4"),
              "desde": 20, "max": 25},
    "G1_Demo1": {"grupo": "GTA1_1997", "url": ia(_G1, _G1_PRE + "Demostration Recorded By Joe Roberts Original Real SCPH-5502 Hardware Version).mp4"),
                 "max": 12},
    "G1_Demo2": {"grupo": "GTA1_1997", "url": ia(_G1, _G1_PRE + "Demostration Recorded By Joe Roberts Original Real SCPH-5552 Hardware Version).mp4"),
                 "max": 12},
    "G1_Intro": {"grupo": "GTA1_Intro", "url": ia(_G1, "Grand Theft Auto 1 Intro Sony Playstation PAL Version.mp4"), "max": 8},
    # 1999 · London 1969 (PC, CC BY 4.0) y GTA 2 (Dreamcast, demostración, CC BY 4.0)
    "LON_PC": {"grupo": "London_1969",
               "url": ia("grand-theft-auto-london-1969-windows-pc-pal-gameplay-full-game-longplay-recorded",
                         "Grand Theft Auto - London 1969 Windows PC PAL Gameplay (Full Game Longplay Recorded By GTA Series With Walkthrough Complete The Game).mp4"),
               "tramos": [(600, 840), (2400, 2640), (4800, 5040)], "max": 10},
    "G2_DC": {"grupo": "GTA2_1999", "url": ia("grand-theft-auto-2-sega-dreamcast-pal-gameplay-full-demostration-attract-mode",
                                              "Grand Theft Auto 2 Sega Dreamcast PAL Gameplay (Full Demostration Attract Mode).mp4"),
              "max": 22},
    # 2001 · GTA III: tráiler del 10.º aniversario y de la Definitive Edition (Rockstar) + partida de PS2 (CC BY 4.0)
    "G3_Aniv": {"grupo": "GTA3_2001", "url": rs("a1t1t316", "720p"), "max": 15},
    "G3_DE": {"grupo": "GTA3_DE", "url": rs("5r2a2o2k", "1080p60"), "max": 10},
    "G3_PS2a": {"grupo": "GTA3_2001", "url": ia(_G3, _G3_PRE + "01).MP4"), "desde": 20, "max": 25},
    "G3_PS2b": {"grupo": "GTA3_2001", "url": ia(_G3, _G3_PRE + "02).mp4"), "max": 25},
    # 2004 · San Andreas: tráiler de la Definitive Edition (Rockstar) + partida de PS2 (CC BY 4.0)
    "SA_DE": {"grupo": "SA_DE", "url": rs("rr54344t", "1080p60"), "max": 10},
    "SA_PS2a": {"grupo": "SA_2004", "url": ia(_SA, _SA_PRE + "01).MP4"), "desde": 20, "max": 25},
    "SA_PS2b": {"grupo": "SA_2004", "url": ia(_SA, _SA_PRE + "02).mp4"), "max": 25},
    # 2004-2009 · Portátiles: GTA Advance (anuncio en tiendas) y Liberty City Stories (PS2, CC BY 4.0)
    "ADV_T": {"grupo": "Advance_2004", "url": ia("gba_instores", "gba_instores.mp4"), "max": 6},
    "LCS_PS2": {"grupo": "LCS_2005", "url": ia("grand-theft-auto-liberty-city-stories-play-station-2-pal-gameplay-full-game-long",
                                               "Grand Theft Auto Liberty City Stories PlayStation 2 PAL Gameplay (Full Game Longplay Walkthrough Free Roam With Cheats Part 01).mp4"),
                "desde": 20, "max": 25},
    # 2008 · GTA IV: tráileres 2 y 4 y anuncio de TV (Rockstar) + partida de PC (CC BY 4.0)
    "IV_T2": {"grupo": "GTA4_2008", "url": rs("6r5r3k97", "720p"), "max": 15},
    "IV_T4": {"grupo": "GTA4_2008", "url": rs("16962ca8", "720p"), "max": 15},
    "IV_TV": {"grupo": "GTA4_2008", "url": rs("c2r6r87t", "720p"), "max": 15},
    "IV_PC": {"grupo": "GTA4_2008", "url": ia(_IV, "Grand Theft Auto 4 Windows PC PAL Gameplay (Full Game Longplay Recorded By GTA Series With Walkthrough in 4K).mp4"),
              "tramos": [(2400, 2640), (9000, 9240), (18000, 18240), (30000, 30240)], "max": 8},
    # 2009 · Episodios de Liberty City (PC, CC BY 4.0)
    "TLAD_PC": {"grupo": "TLAD_2009", "url": ia(_IV, "Grand Theft Auto 4 - The Lost and Damned Windows PC PAL Gameplay (Full Game Longplay Recorded By GTA Series Video Walkthrough in 4K).mp4"),
                "tramos": [(1500, 1740), (7000, 7240)], "max": 10},
    "TBOGT_PC": {"grupo": "TBOGT_2009", "url": ia(_IV, "Grand Theft Auto 4 - The Ballad of Gay Tony Windows PC PAL Gameplay (Full Game Longplay Recorded By GTA Series Video Walkthrough in 4K).mp4"),
                 "tramos": [(1500, 1740), (8000, 8240)], "max": 10},
    # 2013 · GTA V: tráiler de PS5 (Rockstar) + partida de PS5 (CC BY 4.0) y GTA Online
    "V_PS5": {"grupo": "GTA5_2013", "url": rs("ks18e7s9", "1080p"), "max": 12},
    "V_Juego": {"grupo": "GTA5_2013", "url": ia(_V, "Grand Theft Auto 5 PlayStation 5 PAL Gameplay (Full Game Longplay Recorded By YouTube In 4K UHD 60FPS).mp4"),
                "tramos": [(3000, 3240), (12000, 12240), (25000, 25240), (40000, 40240)], "max": 10},
    "ON_Juego": {"grupo": "GTA_Online", "url": ia(_V, "Grand Theft Auto 5 PlayStation 5 PAL Gameplay (Full Game Longplay Recorded By YouTube With GTA Online In 4K 60FPS).mp4"),
                 "desde": 30, "max": 30},
}

# Cada tramo es una fuente propia («V_Juego_2» = segundo tramo); su URL lleva «#t=inicio,fin».
FUENTES = {}
for _k, _f in BASE.items():
    if "tramos" in _f:
        for _i, (_a, _z) in enumerate(_f["tramos"], 1):
            FUENTES[f"{_k}_{_i}"] = {"grupo": _f["grupo"], "url": f"{_f['url']}#t={_a},{_z}", "max": _f["max"]}
    else:
        FUENTES[_k] = _f

# Para la descripción del vídeo (las partidas con CC BY 4.0 exigen citar autor, fuente y licencia)
CREDITOS = [
    "Tráileres: Rockstar Games (rockstargames.com/videos).",
    "Partidas de GTA 1 (PlayStation): Joe Roberts, archive.org/details/" + _G1 + " (CC BY 4.0).",
    "Partidas de London 1969, GTA III, San Andreas, Liberty City Stories, GTA IV, sus episodios y GTA V: "
    "colección «PAL Gameplay» de archive.org (CC BY 4.0): " + ", ".join(
        "archive.org/details/" + x for x in [
            "grand-theft-auto-london-1969-windows-pc-pal-gameplay-full-game-longplay-recorded",
            "grand-theft-auto-2-sega-dreamcast-pal-gameplay-full-demostration-attract-mode", _G3, _SA,
            "grand-theft-auto-liberty-city-stories-play-station-2-pal-gameplay-full-game-long", _IV, _V]) + ".",
]
