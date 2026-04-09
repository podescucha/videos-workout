import re
import logging
import requests
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36"}
def limpiar_texto(texto):
    if not texto: return ""
    texto = re.sub(r"#\w+", "", texto)
    texto = re.sub(r"\b\d[\d.,]*[KkMm]?\s*(vistas|likes|me gusta|compartidos|comentarios|views|shares)\b", "", texto, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", texto).strip()
def extraer_metadatos(url: str):
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo = limpiar_texto(info.get("title") or "")
            descripcion = limpiar_texto(info.get("description") or "")
            if titulo == descripcion: descripcion = ""
            miniatura_url = info.get("thumbnail") or ""
            if titulo:
                return {"titulo": titulo, "descripcion": descripcion, "miniatura_url": miniatura_url}
    except ImportError:
        logger.warning("yt-dlp no instalado")
    except Exception as e:
        logger.warning(f"yt-dlp fallo: {e}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, "html.parser")
        t = soup.find("meta", property="og:title")
        d = soup.find("meta", property="og:description")
        m = soup.find("meta", property="og:image")
        titulo = limpiar_texto(t["content"] if t else "")
        descripcion = limpiar_texto(d["content"] if d else "")
        if titulo == descripcion: descripcion = ""
        if titulo:
            return {"titulo": titulo, "descripcion": descripcion, "miniatura_url": m["content"] if m else ""}
    except Exception as e:
        logger.error(f"HTTP fallo: {e}")
    return None
