"""Capturas web de los planos nuevos de los vídeos 8-10 (Playwright + Edge del equipo, 1280x720 a escala 1,5 = 1920x1080).
Quita avisos de cookies y ventanas, baja hasta la frase citada y la resalta en amarillo. Sin datos personales:
se evitan comentarios y usuarios (si aparecen, revisar y recortar antes de subir).
Uso: python capturar_810.py DIR_SALIDA [nombre ...]"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
SOLO = set(sys.argv[2:])

GI = "https://www.gameinformer.com"
MAYO = "https://www.fool.com/earnings/call-transcripts/2026/05/21/take-two-ttwo-q4-2026-earnings-transcript/"
AGOSTO = "https://www.webull.com/news/15401384786732032"
NOV = "https://www.fool.com/earnings/call-transcripts/2026/11/10/take-two-ttwo-q2-2027-earnings-call-transcript/"

# nombre: (url, frase a la que bajar y resaltar o None, desplazamiento en px)
OBJETIVOS = {
    "N8_Captura_RockstarVI": ("https://www.rockstargames.com/VI", None, 0),
    "N8_Captura_GI_GTA3": (f"{GI}/feature/2023/01/02/20-years-of-liberty-city", "desperate to move GTA", -300),
    "N8_Captura_GTA4_Euphoria": ("https://www.mcvuk.com/development-news/rockstar-confirms-euphoria-use-in-gta-iv/", "Euphoria", "arriba"),
    "N8_Captura_GI_GTA5": (f"{GI}/games/grand_theft_auto_v/b/xbox360/archive/2012/11/12/what-we-know-about-grand-theft-auto-v-the-overview",
                           "bigger than the worlds", -300),
    "N8_Captura_Extended_GTA6": (f"{GI}/2026/08/27/grand-theft-auto-vi-trailer-provides-lengthy-first-look-at-gameplay-including-story", None, 0),
    "N9_Captura_GameInformer_Records": (f"{GI}/b/news/archive/2013/10/08/guinness-world-records-confirms-gta-v-s-astounding-launch.aspx", "815.7", -300),
    "N9_Captura_MCV_45M": ("https://www.mcvuk.com/development/gta-v-ships-45-million-units", "45 million", -200),
    "N9_Captura_Transcripcion_Sold_In": (MAYO, "nearly 230 million", "recorte"),
    "N9_Captura_Webull_230_Agosto": (AGOSTO, "over 230 million", -300),
    "N9_Captura_Transcripcion_Nov": (NOV, "nearly 235 million", "recorte"),
    "N10_Captura_PS_Store": ("https://store.playstation.com/en-ca/product/EP1004-PPSA01547_00-GTAVISTANDARD001", "single-player experience", "recorte"),
    "N10_Captura_Transcripcion_Q4": (MAYO, "premature", "recorte"),
    "N10_Captura_Transcripcion_Q1": (AGOSTO, "support GTA Online going forward", -300),
    "N10_Captura_Gameinformer_2015": (f"{GI}/b/news/archive/2015/02/24/online-heists-coming-to-gta-v-in-march-pc-version-delayed-to-april.aspx", "March 10", -300),
    "N10_Captura_Newswire_Cayo": ("https://www.rockstargames.com/newswire/article/1748koo9oo583k/out-now-the-cayo-perico-heist", None, 0),
    "N10_Captura_Newswire_Kortz": ("https://www.rockstargames.com/newswire/article/2525o93834o413/the-kortz-center-heist-now-available-in-gta-online", None, 0),
    "N10_Captura_Game_Informer_PS5": (f"{GI}/2022/02/04/grand-theft-auto-v-and-gta-online-come-to-ps5-and-xbox-series-xs-this-march", None, 0),
}

QUITAR = """
() => {
  const sel = ['#onetrust-consent-sdk','#onetrust-banner-sdk','[id*="cookie" i]','[class*="cookie" i]','[id*="consent" i]',
    '[class*="consent" i]','[id*="sp_message" i]','[class*="sp_message" i]','[class*="newsletter" i]','iframe[src*="consent"]',
    '[aria-label*="cookie" i]','[class*="modal" i]','[class*="popup" i]','[id*="popup" i]','[class*="overlay" i]','[class*="gdpr" i]',
    '[id*="gdpr" i]','[class*="paywall" i]','[class*="ad-slot" i]','[class*="comment" i]','[id*="comment" i]'];
  for (const s of sel) document.querySelectorAll(s).forEach(e => { if (e !== document.body && e !== document.documentElement) e.remove(); });
  for (const e of document.querySelectorAll('body *')) {
    const st = getComputedStyle(e);
    if ((st.position === 'fixed' || st.position === 'sticky') && e.getBoundingClientRect().top > 150) e.remove();
  }
  document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
}
"""

RESALTAR = """
(frase) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const i = n.data.indexOf(frase);
    if (i < 0) continue;
    const p = n.parentElement;  // solo texto visible: fuera scripts, estilos y bloques ocultos
    if (!p || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(p.tagName) || !p.getClientRects().length) continue;
    const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + frase.length);
    const m = document.createElement('mark'); m.style.background = '#ffe14d'; m.style.color = '#000';
    r.surroundContents(m);
    return m.getBoundingClientRect().top + window.scrollY;
  }
  return null;
}
"""

with sync_playwright() as p:
    nav = p.chromium.launch(channel="msedge", headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = nav.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5, locale="en-US",
                          user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0")
    for nombre, (url, frase, extra) in OBJETIVOS.items():
        if SOLO and nombre not in SOLO:
            continue
        pg = ctx.new_page()
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(6)
            pg.evaluate(QUITAR)
            if frase:
                time.sleep(6)  # webs que terminan de pintarse tarde (Motley Fool, PlayStation Store)
                pg.evaluate(QUITAR)
                y = pg.evaluate(RESALTAR, frase)
                if y is None:
                    raise RuntimeError(f"no aparece «{frase}»")
                pg.evaluate("document.querySelector('mark').scrollIntoView({block: 'center'})")
                if extra == "arriba":
                    pg.evaluate("window.scrollBy(0, 260)")
            time.sleep(2)
            pg.evaluate(QUITAR)
            if frase and not pg.evaluate("!!document.querySelector('mark')"):
                raise RuntimeError("la página se ha vuelto a pintar y se ha perdido el resaltado")
            if frase and extra == "recorte":  # webs que no se dejan desplazar: recorte de la página entera
                y = pg.evaluate("document.querySelector('mark').getBoundingClientRect().top + window.scrollY")
                pg.screenshot(path=str(OUT / f"{nombre}.png"), full_page=True,
                              clip={"x": 0, "y": max(0, y - 300), "width": 1280, "height": 720})
                print("OK", nombre, "| recorte en y =", int(y))
                pg.close()
                continue
            pg.screenshot(path=str(OUT / f"{nombre}.png"))
            print("OK", nombre, "|", pg.title()[:80])
        except Exception as e:  # noqa: BLE001
            print("FALLO", nombre, str(e)[:160])
        pg.close()
    nav.close()
