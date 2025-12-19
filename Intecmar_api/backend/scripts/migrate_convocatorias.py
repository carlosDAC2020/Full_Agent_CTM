import json
import os
from datetime import datetime, date

from backend.app.db.session import SessionLocal, engine
from backend.app.db import models
from backend.app.core.config import settings


def _parse_date(d: str | None) -> date | None:
    if not d or not isinstance(d, str):
        return None
    d = d.strip()
    if not d or d.lower().startswith("no especificado"):
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(d, fmt).date()
        except Exception:
            continue
    return None


def _parse_datetime(d: str | None) -> datetime | None:
    if not d or not isinstance(d, str):
        return None
    d = d.strip()
    if not d or d.lower().startswith("no especificado"):
        return None
    # Try ISO first
    try:
        return datetime.fromisoformat(d.replace("Z", "+00:00"))
    except Exception:
        pass
    # Fallback common formats
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(d, fmt)
        except Exception:
            continue
    return None


def migrate_convocatorias(json_path: str | None = None) -> None:
    if json_path is None:
        json_path = settings.CONVOCATORIAS_FILE

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"convocatorias.json no encontrado en: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f) or []

    if not isinstance(data, list):
        raise ValueError("El archivo convocatorias.json debe contener una lista de objetos")

    # Crear tablas si aún no existen
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    created = 0
    skipped = 0
    try:
        for it in data:
            if not isinstance(it, dict):
                continue

            url = (it.get("url") or it.get("source") or "").strip() or None
            title = (it.get("title") or "").strip() or None

            # Evitar duplicados por URL o por título si no hay URL
            q = db.query(models.Convocatoria)
            if url:
                q = q.filter(models.Convocatoria.url == url)
            elif title:
                q = q.filter(models.Convocatoria.title == title)
            existing = q.first()
            if existing:
                skipped += 1
                continue

            obj = models.Convocatoria(
                title=title or "Sin título",
                description=it.get("description"),
                keywords=it.get("keywords"),
                source=it.get("source"),
                type=it.get("type"),
                url=url,
                created_at=_parse_datetime(it.get("created_at")),
                fecha_inicio=_parse_date(it.get("fecha_inicio") or it.get("inicio")),
                deadline=_parse_datetime(it.get("deadline")),
                fecha_cierre=_parse_date(it.get("fecha_cierre")),
                type_financy=it.get("type_financy"),
                monto=it.get("monto"),
                requisitos=it.get("requisitos") if isinstance(it.get("requisitos"), (list, dict)) else [it.get("requisitos")] if it.get("requisitos") else None,
                beneficios=it.get("beneficios") if isinstance(it.get("beneficios"), (list, dict)) else [it.get("beneficios")] if it.get("beneficios") else None,
                lugar=it.get("lugar"),
            )
            db.add(obj)
            created += 1

        db.commit()
        print(f"Migración de convocatorias completada. Creadas: {created}, omitidas (duplicadas): {skipped}")
    finally:
        db.close()

def migrate_sources(json_path: str | None = None) -> None:
    """Migra las fuentes institucionales desde sources.json a la tabla 'sources'.

    Regla clave: is_active = NOT hidden.
    Evita duplicados por URL tanto dentro del JSON como contra la base de datos.
    """
    if json_path is None:
        json_path = settings.SOURCES_FILE

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"sources.json no encontrado en: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f) or []

    if not isinstance(data, list):
        raise ValueError("El archivo sources.json debe contener una lista de objetos")

    # Crear tablas si aún no existen (incluye la nueva tabla 'sources')
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    created = 0
    skipped = 0
    dupes_in_json = 0
    seen_urls: set[str] = set()
    try:
        for it in data:
            if not isinstance(it, dict):
                continue

            name = (it.get("name") or "").strip()
            type_ = (it.get("type") or "").strip()
            url = (it.get("url") or "").strip()

            if not url or not name:
                print("Omitiendo fuente sin nombre o URL válida")
                continue

            # Detectar duplicados dentro del propio JSON
            if url in seen_urls:
                dupes_in_json += 1
                print(f"URL duplicada en JSON, se omite: {url}")
                continue
            seen_urls.add(url)

            # Evitar duplicados contra la base de datos por URL
            existing = db.query(models.Source).filter(models.Source.url == url).first()
            if existing:
                skipped += 1
                print(f"URL ya existente en BD, se omite: {url}")
                continue

            hidden = bool(it.get("hidden", False))
            is_active = not hidden

            obj = models.Source(
                name=name,
                type=type_,
                url=url,
                is_active=is_active,
            )
            db.add(obj)
            created += 1

        db.commit()
        print(
            f"Migración de sources completada. Creadas: {created}, omitidas (ya en BD): {skipped}, duplicadas en JSON: {dupes_in_json}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    migrate_convocatorias()
    migrate_sources()
