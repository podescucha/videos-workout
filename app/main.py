import logging
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from app.scraping import extraer_metadatos
from app.storage import (agregar_categoria, cargar_categorias, cargar_videos,
    editar_video, eliminar_video, existe_video_url, guardar_video)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI(title="Videos Workout API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
class VideoInput(BaseModel):
    url: str
    categorias: list[str] = []
    nueva_categoria: str = ""
    @field_validator("url")
    @classmethod
    def url_no_vacia(cls, v):
        v = v.strip()
        if not v: raise ValueError("URL no puede estar vacia")
        return v
    @field_validator("categorias")
    @classmethod
    def limpiar(cls, v): return [c.strip() for c in v if c.strip()]
class VideoEdit(BaseModel):
    titulo: str = ""
    descripcion: str = ""
    categorias: list[str] = []
    @field_validator("categorias")
    @classmethod
    def limpiar(cls, v): return [c.strip() for c in v if c.strip()]
@app.get("/")
def root(): return RedirectResponse(url="/static/index.html")
@app.post("/agregar_video", status_code=201)
def agregar_video(body: VideoInput):
    if existe_video_url(body.url):
        raise HTTPException(status_code=409, detail="Video ya registrado")
    if body.nueva_categoria:
        cat = body.nueva_categoria.strip()
        agregar_categoria(cat)
        if cat not in body.categorias: body.categorias.append(cat)
    metadatos = extraer_metadatos(body.url)
    if not metadatos:
        raise HTTPException(status_code=422, detail="No se pudieron extraer metadatos.")
    registro = {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "url": body.url,
        "titulo": metadatos["titulo"], "descripcion": metadatos["descripcion"],
        "miniatura_url": metadatos["miniatura_url"], "categorias": ",".join(body.categorias)}
    video = guardar_video(registro)
    return JSONResponse(content=video, status_code=201)
@app.get("/categorias")
def get_categorias(): return cargar_categorias()
@app.get("/videos")
def get_videos(page: int=Query(default=1,ge=1), limit: int=Query(default=20,ge=1,le=100),
    categoria: str=Query(default=""), busqueda: str=Query(default="")):
    return cargar_videos(page=page, limit=limit, categoria=categoria, busqueda=busqueda)
@app.put("/videos/{id}")
def put_editar_video(id: int, body: VideoEdit):
    r = editar_video(id, body.titulo, body.descripcion, body.categorias)
    if not r: raise HTTPException(status_code=404, detail="Video no encontrado")
    return r
@app.delete("/videos/{id}", status_code=204)
def delete_video(id: int):
    if not eliminar_video(id): raise HTTPException(status_code=404, detail="Video no encontrado")
