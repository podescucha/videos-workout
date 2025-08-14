import requests
from bs4 import BeautifulSoup
import re

def limpiar_texto(texto):
    if not texto:
        return ""
    texto = re.sub(r"#\w+", "", texto)  # Eliminar hashtags
    texto = re.sub(r"\b(vistas|likes|me gusta|compartidos|comentarios)\b", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\d+", "", texto)  # Eliminar números
    texto = re.sub(r"\s+", " ", texto)  # Espacios dobles y saltos extra
    texto = texto.strip()
    return texto

def extraer_metadatos(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        titulo = soup.find("meta", property="og:title")
        descripcion = soup.find("meta", property="og:description")
        miniatura = soup.find("meta", property="og:image")
        titulo = limpiar_texto(titulo["content"] if titulo else "")
        descripcion = limpiar_texto(descripcion["content"] if descripcion else "")
        if titulo == descripcion:
            descripcion = ""
        miniatura_url = miniatura["content"] if miniatura else ""
        return {"titulo": titulo, "descripcion": descripcion, "miniatura_url": miniatura_url}
    except Exception:
        return None
