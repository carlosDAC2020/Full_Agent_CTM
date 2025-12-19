import os
import sys

# Ensure backend package resolution
# When running as `python backend/app/main.py` or via uvicorn
_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_CUR_DIR, '..', '..')) # backend/app/ -> root (Magazine_app)
_BACKEND_DIR = os.path.join(_ROOT_DIR, 'backend')

if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.config import settings
from backend.app.api.api_v1 import api_router
from backend.app.db.session import engine, Base

# Create tables
# In production, use Alembic
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"DB init warning: {e}")

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de estáticos (static, img, assets)
static_dir = os.path.join(_ROOT_DIR, "static")
img_dir = os.path.join(_ROOT_DIR, "img")
assets_dir = os.path.join(_ROOT_DIR, "assets")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

if os.path.exists(img_dir):
    app.mount("/img", StaticFiles(directory=img_dir), name="img")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Montaje de carpeta de salidas (PDFs generados)
os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=settings.OUTPUTS_DIR), name="outputs")

# Configuración global de templates
templates = Jinja2Templates(directory=os.path.join(_ROOT_DIR, "templates"))

# Include Router
app.include_router(api_router)

# --- MAGAZINE FRONTEND ROUTES ---
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/landing")

@app.get("/landing", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("magazine/landing.html", {"request": request})

@app.get("/magazine", response_class=HTMLResponse)
async def magazine_index(request: Request):
    return templates.TemplateResponse("magazine/index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("magazine/login.html", {"request": request})

@app.get("/home_agent", response_class=HTMLResponse)
async def home_agent(request: Request):
    return templates.TemplateResponse("agent/views/home.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
