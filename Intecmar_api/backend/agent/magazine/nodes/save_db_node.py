import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from backend.app.db.session import SessionLocal
from backend.app.db import models

from ..state import AgentState
from .common import _load_institutional_sources_db, is_future_date


def nodo_guardado_db(state: AgentState) -> AgentState:
    """Persiste cada convocatoria/evento en la tabla "convocatorias".
    Filtra eventos pasados y asegura que los datos tengan el formato correcto.
    """
    print("--- 💾 GUARDANDO EN BASE DE DATOS (convocatorias) ---")

    db = SessionLocal()

    # Cargar fuentes para inferir tipo por host si es necesario (desde BD)
    db_sources = []
    try:
        db_sources = _load_institutional_sources_db()
    except Exception:
        db_sources = []

    def _host(u: str) -> str:
        try:
            p = urlparse(u)
            h = (p.netloc or "").lower().lstrip("www.")
            return h
        except Exception:
            return ""

    def _normalize_tipo(tipo_raw: str, url_original: str) -> str:
        t = (tipo_raw or "").strip().lower()
        if "evento" in t:
            return "evento"
        if "internacional" in t:
            return "convocatoria_internacional"
        if "nacional" in t:
            return "convocatoria_nacional"
        # fallback por fuente
        h_item = _host(url_original)
        if h_item and db_sources:
            for s in db_sources:
                su = str(s.get("url") or "")
                hs = _host(su)
                if hs and hs == h_item:
                    st = (s.get("type") or "").strip().lower()
                    if st.startswith("nacion"):
                        return "convocatoria_nacional"
                    if "internacional" in st:
                        return "convocatoria_internacional"
        # default conservador
        return "convocatoria_nacional"

    def _normalize_kw(s: str) -> str:
        s = re.sub(r"\s+", " ", s.strip())
        s = re.sub(r"^[\-–—•·\s]+|[\-–—•·\s]+$", "", s)
        return s

    def _is_short_phrase(s: str) -> bool:
        if not s:
            return False
        if len(s) > 40:
            return False
        words = [w for w in re.split(r"\s+", s) if w]
        if len(words) == 0 or len(words) > 3:
            return False
        if re.search(r"[\.!?]", s):
            return False
        return True

    now_utc = datetime.now(timezone.utc)
    created = 0

    def _clean_date(value):
        """Normaliza valores de fecha tipo string, devolviendo None para valores no válidos."""
        if value is None:
            return None
        text = str(value).strip()
        if not text:
            return None
        lowered = text.lower()
        if lowered in {"no especificado", "no aplica", "n/a", "n.a.", "na"}:
            return None
        return value

    try:
        for item in state.get("contenido_curado", []):
            # Verificar fechas (filtro de eventos/convocatorias pasadas)
            fecha_cierre_raw = item.get("fecha_cierre") or item.get("deadline") or item.get("fecha_fin")
            if not is_future_date(fecha_cierre_raw):
                print(
                    f"⚠️  Omitiendo evento/convocatoria pasada: {item.get('titulo', 'Sin título')} - Fecha: {fecha_cierre_raw}"
                )
                continue

            titulo = item.get("titulo") or "Sin título"
            desc = (
                item.get("resumen_magazine")
                or item.get("objetivo")
                or item.get("descripcion")
                or "Sin descripción"
            )

            # Keywords
            kws: list[str] = []
            if "dirigido_a" in item and item["dirigido_a"]:
                dirigido_a = item["dirigido_a"]
                if isinstance(dirigido_a, list):
                    dirigido_a = ", ".join(str(x) for x in dirigido_a if x)
                for part in re.split(r"[,\n;]", str(dirigido_a)):
                    kw = _normalize_kw(part)
                    if not kw or kw.lower() == "no especificado":
                        continue
                    if _is_short_phrase(kw):
                        norm = kw.lower()
                        if norm not in [k.lower() for k in kws]:
                            kws.append(kw)

            url_original = item.get("url_original", "")
            tipo_norm = _normalize_tipo(item.get("tipo", ""), url_original)
            if tipo_norm and tipo_norm not in kws:
                kws.append(tipo_norm)

            if (
                "type_financy" in item
                and item["type_financy"]
                and str(item["type_financy"]).lower() != "no especificado"
            ):
                if item["type_financy"] not in kws:
                    kws.append(item["type_financy"])

            url = url_original or None

            # Evitar duplicados por URL o por título
            existe = db.query(models.Convocatoria).filter(
                (models.Convocatoria.url == url) |
                (models.Convocatoria.title == titulo)
            ).first()
            if existe:
                print(f"⚠️  Duplicado omitido: {titulo} ({url})")
                continue

            # Normalize type_financy to string (convert array to comma-separated string)
            type_financy_value = item.get("type_financy")
            if isinstance(type_financy_value, list):
                type_financy_str = ", ".join(str(x) for x in type_financy_value if x)
            elif type_financy_value:
                type_financy_str = str(type_financy_value)
            else:
                type_financy_str = None

            conv = models.Convocatoria(
                title=str(titulo),
                description=str(desc),
                keywords=kws,
                source=url_original or None,
                type=str(tipo_norm),
                url=url,
                created_at=now_utc,
                fecha_inicio=_clean_date(item.get("fecha_inicio") or item.get("inicio")),
                deadline=_clean_date(item.get("deadline")),
                fecha_cierre=_clean_date(item.get("fecha_cierre")),
                type_financy=type_financy_str,
                monto=item.get("monto"),
                requisitos=item.get("requisitos") or ["No especificado"],
                beneficios=item.get("beneficios") or ["No especificados"],
                lugar=item.get("lugar") or "No especificado",
            )
            db.add(conv)
            created += 1

        if created:
            db.commit()
        print(f"✅ Guardado en BD: {created} nuevas convocatorias")
    except Exception as e:
        print(f"⚠️ Error guardando convocatorias en BD: {e}")
        db.rollback()
    finally:
        db.close()

    # Importante: devolver una actualización válida del estado
    return {"contenido_curado": state.get("contenido_curado", [])}
