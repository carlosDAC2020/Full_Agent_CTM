import os
import sys

# Ensure backend package resolution
# When running as `python backend/app/main.py` or via uvicorn
_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_CUR_DIR, '..', '..')) # backend/app/ -> root (Magazine_app)
_BACKEND_DIR = os.path.join(_ROOT_DIR, 'backend')

if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

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

# Static Mounts
os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=settings.OUTPUTS_DIR), name="outputs")

# Frontend and other assets
# Assuming frontend is in root/frontend and img in root/img
frontend_dir = os.path.join(_ROOT_DIR, "frontend")
img_dir = os.path.join(_ROOT_DIR, "img")
assets_dir = os.path.join(_ROOT_DIR, "assets")

if os.path.exists(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")
if os.path.exists(img_dir):
    app.mount("/img", StaticFiles(directory=img_dir), name="img")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Include Router
app.include_router(api_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/frontend/landing.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
