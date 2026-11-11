"""Etiqueta los trozos automáticos con lo que se ve (CLIP, modelo libre que funciona en el procesador de GitHub).

Usa la miniatura de cada trozo en su hoja de contactos (no hace falta bajar los vídeos). Añade la columna
«Etiquetas» (p. ej. «coche|noche|ciudad») y el guion puede pedir planos así: "@Grupo#coche:3" o "@#playa:2".
"""
import numpy as np

ETIQUETAS = {
    "coche": "a car driving in a video game",
    "moto": "a motorcycle in a video game",
    "barco": "a boat or speedboat on the water",
    "avion": "a plane or helicopter in the sky",
    "persecucion": "a police chase with police cars",
    "tiroteo": "a shootout with guns",
    "cara": "a close-up of a character's face",
    "personas": "a group of people",
    "playa": "a sunny beach with palm trees",
    "noche": "a city at night with neon lights",
    "ciudad": "city streets and buildings",
    "aerea": "an aerial view of a city",
    "naturaleza": "swamp, forest or countryside",
    "interior": "inside a building or room",
    "texto": "a logo or text on screen",
}
UMBRAL = 0.18  # probabilidad mínima; siempre se queda con la mejor si ninguna llega

_MODELO = None


def _modelo():
    global _MODELO
    if _MODELO is None:
        import open_clip
        import torch
        m, _, pre = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
        tok = open_clip.get_tokenizer("ViT-B-32")
        with torch.no_grad():
            t = m.encode_text(tok(list(ETIQUETAS.values())))
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
                elegidas = [claves[k] for k in orden[:3] if fila[k] >= UMBRAL] or [claves[orden[0]]]
                salida.append("|".join(elegidas))
    return salida


def recortes_de_hoja(hoja, n, cols=5):
    """Miniaturas 320x184 de una hoja de contactos de preparar_trozos (5 columnas, celdas de 320x200)."""
    return [hoja.crop(((k % cols) * 320, (k // cols) * 200, (k % cols) * 320 + 320, (k // cols) * 200 + 184))
            for k in range(n)]
