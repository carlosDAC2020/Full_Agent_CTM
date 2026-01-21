import os
from datetime import datetime, timezone
from urllib.parse import urlparse

from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.db.session import SessionLocal
from backend.app.db import models
from backend.app.core.config import settings

from ..state import AgentState
from ..tools import tools, search_all

# Configuración del LLM que usaremos (Gemini)
_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=_api_key)

INSTITUTIONAL_SOURCES = []


def _load_institutional_sources_db() -> list:
    """Carga las fuentes institucionales desde la base de datos (tabla sources).
    Devuelve solo las que tienen is_active = True.
    """
    db = SessionLocal()
    try:
        rows = db.query(models.Source).filter(models.Source.is_active == True).all()  # type: ignore
        return [
            {"id": s.id, "name": s.name, "type": s.type, "url": s.url}
            for s in rows
            if getattr(s, "url", None)
        ]
    except Exception:
        return []
    finally:
        db.close()


def is_future_date(date_str: str) -> bool:
    """Verifica si una fecha es futura. Acepta múltiples formatos."""
    if not date_str or date_str.lower() == 'no especificado':
        return True  # Si no hay fecha, asumimos que es futura

    from dateutil import parser

    try:
        # Intentar parsear la fecha
        date = parser.parse(date_str, fuzzy=True)
        # Si la fecha no tiene zona horaria, asumir UTC
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return date > datetime.now(timezone.utc)
    except Exception:
        # Si hay error al parsear, asumir que es futura
        return True
