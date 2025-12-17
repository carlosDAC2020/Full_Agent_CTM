import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Importar configuración de DB
from src.core.database import engine, Base
from src.models import history 

# Importar los routers nuevos
from src.routers import agent, tasks, views, sessions, auth

# Crear tablas en DB si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CTM Agent Platform")

# 1. Montar Archivos Estáticos (CSS/JS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# 2. Incluir Routers
app.include_router(views.router)      # Frontend "/"
app.include_router(auth.router)       # Auth "/api/me"
app.include_router(agent.router)      # API Agente "/api/agent/..."
app.include_router(tasks.router)      # API Tasks "/api/tasks/..."
app.include_router(sessions.router)   # API Sessions "/api/sessions/..."

# Mensaje de inicio
@app.on_event("startup")
async def startup_event():
    print("🚀 API Iniciada. Frontend disponible en /")