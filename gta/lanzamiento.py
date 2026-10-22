"""Especial de lanzamiento (decidido el 22 oct): «¡Hoy sale GTA 6!» a las 00:00 del jueves 19 de noviembre.

Se ejecuta el 18 de noviembre por la noche (23:17 en Madrid): monta el vídeo y lo deja PROGRAMADO en Buffer para
las 00:00:00 exactas (Buffer publica a su hora aunque GitHub vaya con retraso). Se publica solo, sin aprobación,
porque el texto está escrito aquí y comprobado:
- Fecha y plataformas: Rockstar (19 de noviembre de 2026, PS5 y Xbox Series X|S).
- Hora: según la ficha de la PlayStation Store (contado por Hipertextual el 8 sep 2026), se desbloquea a las 00:00
  hora local de cada país.
- GTA V salió el 17 de septiembre de 2013 (Rockstar).
Si GitHub llega tarde y ya han pasado las 00:00, se publica al momento.
Con PRUEBA = true monta el vídeo en salida_cuenta/ y no toca Airtable ni Buffer."""
import os, shutil, tempfile
from datetime import date, datetime, timezone
import airtable, medios, publicar, video
from config import MADRID, T_PUB, HASHTAGS_FIJOS, PIE_POST
from cuenta_atras import DIR_PRUEBA, SALIDA

TROZOS = ["¡Ya es 19 de noviembre: hoy sale GTA 6!",
          "Trece años después de GTA 5,",
          "llega Grand Theft Auto 6",
          "a PlayStation 5 y a Xbox Series X y S.",
          "Según la PlayStation Store,",
          "en España se desbloquea a medianoche.",
          "Vuelve Vice City, en el estado de Leónida,",
          "con Jason y Lucía como protagonistas.",
          "Aquí seguiremos con todas las novedades.",
          "¿Vas a empezar a jugar esta misma noche?"]
CAPTION = ("¡Hoy sale GTA 6! Grand Theft Auto VI llega este jueves 19 de noviembre a PS5 y Xbox Series X|S, "
           "trece años después de GTA V.\n\n"
           "Según la ficha de la PlayStation Store, se desbloquea a las 00:00 hora local de cada país.\n"
           "Fuente: Rockstar Games y PlayStation Store\n" + PIE_POST + "\n\n"
           + " ".join(HASHTAGS_FIJOS + ["#GTA6Lanzamiento"]))
TITULO_YT = "GTA 6 sale hoy, 19 de noviembre: ya es oficial"


def main():
    prueba = os.environ.get("PRUEBA") == "true"
    ahora = datetime.now(MADRID)
    dia = SALIDA.date()
    caps = medios.elegir("Jason_and_Lucia", "lanzamiento", 2) + medios.elegir("Vice_City", "lanzamiento", 2)
    f = {"Titular": "Especial: ¡hoy sale GTA 6! (00:00 del 19 de noviembre)", "Estado": "Por Revisar",
         "Tipo": "Noticia", "Info": "Oficial", "Guion": "\n".join(TROZOS), "Etiqueta": "¡HOY SALE!",
         "Personaje": False, "Capturas": ", ".join(caps), "Caption": CAPTION, "Título YouTube": TITULO_YT,
         "Fuente": "Rockstar Games", "Enlace": "https://www.rockstargames.com/VI",
         "Texto de la fuente": "Especial de lanzamiento (texto fijo comprobado en gta/lanzamiento.py)",
         "Creada": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "Avisos": "Especial de lanzamiento: se publica solo a las 00:00 del 19 de noviembre"}
    carpeta = tempfile.mkdtemp()
    ruta, info, cambios = video.montar(f, dia, "lanzamiento", carpeta)
    if info["voz"].startswith("Piper"):
        f["Caption"] = f["Caption"].replace("\n\n#", "\nVoz: sharvard (CC BY 3.0)\n\n#", 1)
    print(f"Especial de lanzamiento · capturas {caps} · vídeo {info}", flush=True)
    if prueba:
        os.makedirs(DIR_PRUEBA, exist_ok=True)
        shutil.copy(ruta, os.path.join(DIR_PRUEBA, "especial_lanzamiento.mp4"))
        open(os.path.join(DIR_PRUEBA, "especial_lanzamiento.txt"), "w").write(f["Guion"] + "\n\n" + f["Caption"])
        print("PRUEBA: no se crea nada en Airtable ni se programa en Buffer.")
        return
    if ahora.date() > date(2026, 11, 19):
        raise SystemExit("El especial de lanzamiento solo se publica el 18-19 de noviembre")
    rec = airtable.crear(T_PUB, [f])[0]
    try:
        adj = video.subir(rec["id"], ruta)
        if not adj or not adj.get("url"):
            raise RuntimeError("No se pudo subir el vídeo a Airtable")
        cuando = SALIDA.astimezone(timezone.utc)
        programar = datetime.now(timezone.utc) < cuando
        mut = publicar.mutacion(cuando.strftime("%Y-%m-%dT%H:%M:%S.000Z") if programar else None)
        datos = publicar.buffer(mut, publicar.variables(f["Caption"], f["Guion"], TITULO_YT, adj["url"]))
        res = datos.get("data") or {}
        bien = [k for k in ("reel", "tiktok", "youtube") if (res.get(k) or {}).get("post")]
        mal = {k: (res.get(k) or {}).get("message") or str(datos.get("errors"))[:200]
               for k in ("reel", "tiktok", "youtube") if k not in bien}
        print(f"Buffer ({'programado para las 00:00' if programar else 'publicado ya'}): bien {bien}; fallos {mal}", flush=True)
        if not bien:
            raise RuntimeError(f"Buffer no aceptó el especial: {mal}")
    except Exception as e:
        airtable.actualizar(T_PUB, [(rec["id"], {"Estado": "Descartado", "Avisos": f"Especial no publicado: {str(e)[:300]}"})])
        raise
    cambios.update({"Estado": "Publicado", "Publicada": cuando.isoformat(timespec="seconds") if programar
                    else datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "Vídeo": [{"id": adj["id"]}] if adj.get("id") else [],
                    "Avisos": ("Especial de lanzamiento" + (" programado en Buffer para las 00:00" if programar else "")
                               + (f" · Buffer no aceptó: {mal}" if mal else ""))[:400]})
    airtable.actualizar(T_PUB, [(rec["id"], cambios)])


if __name__ == "__main__":
    main()
