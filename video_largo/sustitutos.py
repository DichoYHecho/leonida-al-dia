"""Planos de juego que aún no tienen captura propia: su fila de trozos_57.csv pasa a un trozo libre del tráiler oficial
del mismo juego (libre = que ese guion no usa ni por nombre ni por grupo). Son provisionales: cuando exista la captura
real (menú de radio, etc.), se cambia otra vez la fila. Grupo «Sustitutos_57»."""
import csv, io
from pathlib import Path

AQUI = Path(__file__).parent
TABLAS = [AQUI / f for f in ("trozos_auto.csv", "trozos_auto_sg.csv", "trozos_auto_jl.csv", "trozos_vc.csv")]

# plano pendiente: (trozo libre del que se copia vídeo, inicio y duración  |  o (vídeo, inicio, duración), qué se ve)
SUSTITUTOS = {
    "NUEVO_Iggy_Liberty_Rock": ("G3_PS2a_10", "GTA III (tráiler oficial)"),
    "NUEVO_K_DST_Menu": ("SA_PS2a_10", "San Andreas (tráiler oficial)"),
    "NUEVO_Vladivostok_Menu": ("IV_PC_1_04", "GTA IV (tráiler oficial)"),
    "NUEVO_Radio_Menu_GTA5": ("V_Juego_1_04", "GTA V (tráiler oficial)"),
    "NUEVO_Interfaz_Trilogy": ("VCDE_Juego_06", "Vice City de la Definitive Edition (tráiler oficial)"),
    "NUEVO_Rueda_Radio_GTA6": ("T2_08", "GTA VI (tráiler 2)"),
    "NUEVO_Caja_Vice_CD": ("VC02_Trailer3_05", "Vice City (tráiler 3 de 2002)"),
    "NUEVO_RDR2_Paisaje": (("RDR2", 10.0, 3.0), "Red Dead Redemption 2 (tráiler oficial, sin revisar)"),
    "NUEVO_RDR2_Caballo": (("RDR2", 18.0, 3.0), "Red Dead Redemption 2 (tráiler oficial, sin revisar)"),
    "NUEVO_RDR2_Arthur": (("RDR2", 26.0, 3.0), "Red Dead Redemption 2 (tráiler oficial, sin revisar)"),
}

fuente = {}
for t in TABLAS:
    if t.exists():
        for r in csv.DictReader(io.StringIO(t.read_text(encoding="utf-8-sig"))):
            fuente[r["Trozo"]] = r

ruta = AQUI / "trozos_57.csv"
filas = list(csv.reader(io.StringIO(ruta.read_text(encoding="utf-8-sig"))))
cab, cuerpo = filas[0], filas[1:]
i = {k: cab.index(k) for k in ("Grupo", "Inicio (s)", "Duración (s)", "Qué se ve", "Foco (0 izquierda - 1 derecha)", "Notas", "Vídeo", "Lento")}
hechos = []
for f in cuerpo:
    if not f or f[0] not in SUSTITUTOS:
        continue
    origen, que = SUSTITUTOS[f[0]]
    if isinstance(origen, tuple):
        video, ini, dur = origen
        foco, lento, de = "0.5", "1", f"{video}@{ini}"
    else:
        r = fuente[origen]
        video, ini, dur = r["Vídeo"], r["Inicio (s)"], r["Duración (s)"]
        foco, lento, de = r.get("Foco (0 izquierda - 1 derecha)", "0.5"), r.get("Lento", "1") or "1", origen
    f[i["Grupo"]] = "Sustitutos_57"
    f[i["Inicio (s)"]], f[i["Duración (s)"]], f[i["Vídeo"]] = str(ini), str(dur), video
    f[i["Foco (0 izquierda - 1 derecha)"]], f[i["Lento"]] = foco, lento
    f[i["Qué se ve"]] = f"PROVISIONAL: {que}"
    f[i["Notas"]] = f"Copia de {de}; cambiar por la captura real"
    hechos.append(f[0])
out = io.StringIO()
csv.writer(out, lineterminator="\n").writerows([cab] + cuerpo)
ruta.write_text(out.getvalue(), encoding="utf-8")
print(len(hechos), "sustitutos:", ", ".join(hechos))
print("Sin fila en la tabla:", ", ".join(sorted(set(SUSTITUTOS) - set(hechos))) or "ninguno")
