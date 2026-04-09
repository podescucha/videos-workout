import os
import logging
import json
from datetime import datetime
from contextlib import contextmanager
import sqlite3
logger = logging.getLogger(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "videos.db")
CATEGORIAS_PATH = os.path.join(os.path.dirname(__file__), "categorias.json")
def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE, titulo TEXT DEFAULT '',
            descripcion TEXT DEFAULT '', miniatura_url TEXT DEFAULT '',
            categorias TEXT DEFAULT '')""")
        conn.commit()
@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try: yield conn
    finally: conn.close()
def row_to_dict(row):
    d = dict(row); d["categorias"] = d.get("categorias") or ""; return d
init_db()
def cargar_categorias():
    if not os.path.exists(CATEGORIAS_PATH): return []
    with open(CATEGORIAS_PATH, "r", encoding="utf-8") as f: return json.load(f)
def agregar_categoria(cat: str):
    cats = cargar_categorias(); cat = cat.strip()
    if cat and cat not in cats:
        cats.append(cat)
        with open(CATEGORIAS_PATH, "w", encoding="utf-8") as f: json.dump(cats, f, ensure_ascii=False, indent=2)
def existe_video_url(url: str):
    with get_conn() as conn:
        return conn.execute("SELECT 1 FROM videos WHERE url = ?", (url,)).fetchone() is not None
def guardar_video(registro: dict):
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO videos (fecha,url,titulo,descripcion,miniatura_url,categorias) VALUES (:fecha,:url,:titulo,:descripcion,:miniatura_url,:categorias)", registro)
        conn.commit()
        return row_to_dict(conn.execute("SELECT * FROM videos WHERE id = ?", (cur.lastrowid,)).fetchone())
def cargar_videos(page=1, limit=20, categoria="", busqueda=""):
    offset = (page - 1) * limit; conditions, params = [], []
    if categoria:
        conditions.append("(categorias = ? OR categorias LIKE ? OR categorias LIKE ? OR categorias LIKE ?)")
        params += [categoria, f"{categoria},%", f"%,{categoria}", f"%,{categoria},%"]
    if busqueda:
        conditions.append("(titulo LIKE ? OR descripcion LIKE ?)")
        q = f"%{busqueda}%"; params += [q, q]
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    with get_conn() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM videos {where}", params).fetchone()[0]
        rows = conn.execute(f"SELECT * FROM videos {where} ORDER BY id DESC LIMIT ? OFFSET ?", params + [limit, offset]).fetchall()
    return {"total": total, "page": page, "limit": limit, "pages": max(1, -(-total // limit)), "videos": [row_to_dict(r) for r in rows]}
def editar_video(id: int, titulo: str, descripcion: str, categorias: list):
    cats = ",".join(c.strip() for c in categorias if c.strip())
    with get_conn() as conn:
        cur = conn.execute("UPDATE videos SET titulo=?,descripcion=?,categorias=? WHERE id=?", (titulo, descripcion, cats, id))
        conn.commit()
        if cur.rowcount == 0: return None
        return row_to_dict(conn.execute("SELECT * FROM videos WHERE id = ?", (id,)).fetchone())
def eliminar_video(id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM videos WHERE id = ?", (id,)); conn.commit(); return cur.rowcount > 0
def migrar_desde_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "videos.csv")
    if not os.path.exists(csv_path): return
    try:
        import csv
        with get_conn() as conn:
            if conn.execute("SELECT COUNT(*) FROM videos").fetchone()[0] > 0: return
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    r = {"fecha": row.get("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "url": row.get("url",""),
                        "titulo": row.get("titulo",""), "descripcion": row.get("descripcion",""),
                        "miniatura_url": row.get("miniatura_url",""), "categorias": row.get("categorias","")}
                    if r["url"]: guardar_video(r)
                except: pass
        logger.info("Migracion CSV completada")
    except Exception as e: logger.error(f"Error: {e}")
migrar_desde_csv()
