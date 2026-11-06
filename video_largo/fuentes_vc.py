"""Vídeos de cada juego para el vídeo 2 (Vice City): tráileres oficiales y gameplays guardados en archive.org.

Cada fuente: grupo (para usar «@grupo» en el guion), url, desde/hasta (segundos útiles) y máximo de trozos.
preparar_trozos.py elige los trozos y los deja en la rama trozos-vc (trozos_auto.csv + hojas de contactos)."""
from urllib.parse import quote


def ia(ident, archivo):
    return f"https://archive.org/download/{ident}/{quote(archivo)}"


RS = "https://videos-rockstargames-com.akamaized.net/v4/"

FUENTES = {
    # Vice City Stories (2006): tráileres oficiales de Rockstar
    "VCS_T1": {"grupo": "VCS_2006", "url": ia("vcstrl1", "vcstrl1.mp4"), "max": 12},
    "VCS_T2": {"grupo": "VCS_2006", "url": ia("vcstrl2hi", "vcstrl2hi.mp4"), "max": 12},
    "VCS_T3": {"grupo": "VCS_2006", "url": ia("vcstrl3hi", "vcstrl3hi.mp4"), "max": 12},
    "VCS_PS2": {"grupo": "VCS_2006", "url": ia("vcsps-2-master-cs-480x-270", "VCSPS2_MASTER_CS_480x270.mp4"), "max": 12},
    "VCS_Acrob": {"grupo": "VCS_2006", "url": ia("t_gtavcs_stunts", "t_gtavcs_stunts.mp4"), "max": 6},
    "VCS_MotoAgua": {"grupo": "VCS_2006", "url": ia("gtavcs-092006-jetski-jump", "gtavcs_092006_jetski jump.mp4"), "max": 5},
    "VCS_Policia": {"grupo": "VCS_2006", "url": ia("gtavcs-2-092006-police", "gtavcs2_092006_ police.mp4"), "max": 6},
    "VCS_Helis": {"grupo": "VCS_2006", "url": ia("gtavcs_trailers_helicopters", "gtavcs_trailers_helicopters.mp4"), "max": 6},
    "VCS_Jive": {"grupo": "VCS_2006", "url": ia("gtavcs_jive_ride_anglais", "gtavcs_jive_ride_anglais.mp4"), "max": 5},
    # Vice City Stories: gameplay de PS2
    "VCS_Juego": {"grupo": "VCS_2006", "url": ia("grand-theft-auto-vice-city-stories-play-station-2-pal-gameplay-full-game-longpla",
                  "Grand Theft Auto Vice City Stories PlayStation 2 PAL Gameplay (Full Game Longplay Walkthrough Free Roam With Cheats Part 01).ia.mp4"),
                  "desde": 30, "max": 15},
    # Vice City (2002): tráiler 3 original, tráiler del 10.º aniversario y comparativa oficial
    "VC02_Trailer3": {"grupo": "Vice_City_2002", "url": ia("vicecity480x360_ph3", "vicecity480x360_ph3.mp4"), "max": 15},
    "VC10_Aniv": {"grupo": "Vice_City_2002", "url": ia("youtube-Xn7ALwAQrno", "Xn7ALwAQrno.mp4"), "max": 15},
    "VC_Comp": {"grupo": "VC_Comparativa", "url": RS + "ao1c441c/flv/en-us-1080p60.mp4", "max": 15},
    # Vice City Definitive Edition: gameplay
    "VCDE_Juego": {"grupo": "VC_DE", "url": ia("youtube-R2CmKsMlGNM", "R2CmKsMlGNM.mp4"), "max": 15},
    # Historia de GTA desde 1997 (aquí sale el GTA original)
    "GTA_15": {"grupo": "Historia_GTA", "url": ia("youtube_mXRQJ1f9mhY", "Grand Theft Auto 15th Anniversary 1997-2012.mp4"),
               "hasta": 420, "max": 30},
}
