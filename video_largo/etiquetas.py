"""Etiqueta los trozos automáticos con lo que se ve (CLIP, modelo libre que funciona en el procesador de GitHub).

Usa la miniatura de cada trozo en su hoja de contactos (no hace falta bajar los vídeos). Añade la columna
«Etiquetas» (p. ej. «coche|noche|ciudad») y el guion puede pedir planos así: "@Grupo#coche:3" o "@#playa:2".
"""
import numpy as np

VERSION = "2"  # al cambiar las frases o el criterio, los trozos ya preparados se vuelven a etiquetar
PLANTILLA = "a video game screenshot of {}"
ETIQUETAS = {
    "coche": "a car or truck driving on a road",
    "moto": "a person riding a motorcycle",
    "barco": "a boat on the water",
    "avion": "an airplane or helicopter flying",
    "persecucion": "police cars chasing someone",
    "tiroteo": "a person aiming or shooting a gun",
    "cara": "a close-up portrait of a person's face",
    "personas": "people standing and talking",
    "playa": "a beach with sand, sea and palm trees",
    "noche": "a city street at night",
    "ciudad": "city streets and buildings in daylight",
    "aerea": "an aerial view looking down on a city",
    "naturaleza": "a forest, swamp or countryside landscape",
    "interior": "the inside of a room or building",
    "texto": "a logo or title text on a plain background",
}
UMBRAL = 0.25  # además de la mejor, otras etiquetas solo si pasan este umbral y la mitad de la mejor

_MODELO = None


def _modelo():
    global _MODELO
    if _MODELO is None:
        import open_clip
        import torch
        m, _, pre = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
        tok = open_clip.get_tokenizer("ViT-B-32")
        with torch.no_grad():
            t = m.encode_text(tok([PLANTILLA.format(x) for x in ETIQUETAS.values()]))
            t /= t.norm(dim=-1, keepdim=True)
        _MODELO = (m.eval(), pre, t)
    return _MODELO


def etiquetar(imagenes):
    """imagenes: lista de PIL.Image -> lista de «a|b|c»."""
    if not imagenes:
        return []
    import torch
    m, pre, t = _modelo()
    claves = list(ETIQUETAS)
    salida = []
    with torch.no_grad():
        for i in range(0, len(imagenes), 32):
            x = torch.stack([pre(im.convert("RGB")) for im in imagenes[i:i + 32]])
            f = m.encode_image(x)
            f /= f.norm(dim=-1, keepdim=True)
            p = (100 * f @ t.T).softmax(dim=-1).numpy()
            for fila in p:
                orden = np.argsort(-fila)
                elegidas = [claves[orden[0]]] + [claves[k] for k in orden[1:3] if fila[k] >= max(UMBRAL, fila[orden[0]] / 2)]
                salida.append("|".join(elegidas))
    return salida


def recortes_de_hoja(hoja, n, cols=5):
    """Miniaturas 320x184 de una hoja de contactos de preparar_trozos (5 columnas, celdas de 320x200)."""
    return [hoja.crop(((k % cols) * 320, (k // cols) * 200, (k % cols) * 320 + 320, (k // cols) * 200 + 184))
            for k in range(n)]
