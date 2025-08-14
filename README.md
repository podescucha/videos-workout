

# Gestor de Videos de Facebook para Rutinas de Ejercicio

Aplicación web desarrollada con FastAPI y frontend en HTML, CSS y JavaScript, diseñada para recopilar, clasificar y consultar videos de Facebook orientados a rutinas de ejercicio.

## Características principales

📥 **Captura de videos:** Pega la URL de un video de Facebook y extrae automáticamente título, miniatura y descripción limpia (sin hashtags ni métricas).

🗂 **Clasificación flexible:** Selecciona categorías predefinidas o agrega nuevas, las cuales quedan guardadas para usos futuros.

📑 **Almacenamiento incremental:** Guarda cada video en un archivo CSV con fecha, URL, título, descripción, miniatura y categorías.

🔍 **Consulta amigable:** Visualiza y filtra videos por categoría en una interfaz clara y responsiva.

✏ **Edición en línea:** Modifica directamente desde la interfaz web el título, descripción y categorías de cualquier video.

🎛 **Interfaz adaptable:** Botón para mostrar/ocultar el formulario de captura según preferencia.

## Tecnologías utilizadas

**Backend:** FastAPI (Python 3.10+), Requests, BeautifulSoup4, Pandas

**Frontend:** HTML5, CSS3, JavaScript (Fetch API), Bootstrap

**Datos:** CSV para videos, JSON para categorías

## Instalación local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   # Linux/Mac
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor:
   - Opción recomendada: haz doble clic en `iniciar-servidor.bat`.
   - Opción manual:
     ```bash
     venv\Scripts\activate
     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
     ```

5. Abrir en el navegador:
   - En la PC: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - En el móvil (misma red local): [http://IP_DE_TU_PC:8000/](http://IP_DE_TU_PC:8000/)
     (Ejemplo: http://192.168.1.10:8000/)


## Despliegue en Render

Puedes publicar tu aplicación web gratis y rápido usando [Render](https://render.com):

### Pasos generales:

1. **Sube tu proyecto a GitHub** (incluye todo el backend y la carpeta `static`).
2. **Crea una cuenta** en [https://render.com](https://render.com).
3. **Crea un “Web Service”** y conecta tu repositorio.
4. Configura:
    - **Runtime:** Python 3.10+
    - **Build command:**
       ```bash
       pip install -r requirements.txt
       ```
    - **Start command:**
       ```bash
       uvicorn app.main:app --host 0.0.0.0 --port 10000
       ```
5. **Deploy** y espera a que Render genere tu URL pública.

### Ventajas
- Rápido de configurar
- Gratis

### Desventajas
- Puede dormirse si no se usa
- Límite de CPU/RAM
