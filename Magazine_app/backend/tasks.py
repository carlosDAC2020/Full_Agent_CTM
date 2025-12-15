import os
import json
import time
from datetime import datetime
from typing import Any, Dict, Optional, List
from celery import states
from .celery_app import celery_app
import requests

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.db import models as db_models
from backend.app.services.redis_service import get_redis, task_key, release_flow_lock
from backend.app.services.email_service import send_smtp_email
from backend.app.services.agent_service import run_magazine_generation_stream, search_web, llm_invoke, agent_app

# Agent imports handled by agent_service, but we access agent_app directly in runs
# If agent_app is needed, we imported it above from agent_service

def _get_redis():
    return get_redis()


# Helpers
def _publish_event(event_type: str, payload: Dict[str, Any]):
    r = _get_redis()
    if not r: return
    data = {"type": event_type, **payload}
    r.publish("tasks_events", json.dumps(data))

def _post_flow_status(task_id: str, status: str, name: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
    try:
        base_url = os.getenv("API_INTERNAL_URL") or os.getenv("BACKEND_BASE_URL") or "http://localhost:8000"
        url = f"{base_url}/flows/{task_id}/status"
        headers = {"Content-Type": "application/json"}
        worker_token = settings.WORKER_TOKEN
        if worker_token:
            headers["X-Worker-Token"] = worker_token
        payload: Dict[str, Any] = {"status": status}
        if name: payload["name"] = name
        if meta is not None: payload["meta"] = meta
        requests.post(url, json=payload, headers=headers, timeout=5)
    except Exception:
        pass

def _set_task_status(task_id: str, data: Dict[str, Any]):
    r = _get_redis()
    if r:
        key = task_key(task_id)
        r.hset(key, mapping={k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()})
        r.sadd("active_tasks", task_id)

def _finish_task_status(task_id: str, status: str):
    r = _get_redis()
    if r:
        key = task_key(task_id)
        r.hset(key, mapping={"status": status, "updated": datetime.utcnow().isoformat()})
        r.srem("active_tasks", task_id)

def _release_flow_lock(flow_type: str):
    r = _get_redis()
    release_flow_lock(r, flow_type)


def _send_smtp(sender: str, to_list: List[str], subject: str, body: str, attachments: List[str]):
    # Wrapper to use the service
    try:
        send_smtp_email(sender, to_list, subject, body, attachments)
    except Exception as e:
        print(f"Email error: {e}")


@celery_app.task(bind=True, name="tasks.run_magazine", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2})
def run_magazine(self, payload: Dict[str, Any] | None = None):
    """
    Ejecuta el flujo de "Generar Magazine" en background y emite eventos.
    payload: { "tema": str }
    """
    task_id = self.request.id or f"mag_{int(time.time())}"
    _set_task_status(task_id, {"id": task_id, "type": "magazine", "status": "running", "created": datetime.utcnow().isoformat()})
    _post_flow_status(task_id, status="running", name="Generación de Magazine")
    _publish_event("task_started", {"id": task_id, "type": "magazine"})

    try:
        default_topic = os.getenv(
            "DEFAULT_TOPIC",
            "convocatorias de financiación nacionales e internacionales y eventos en ciencia, tecnología e inteligencia artificial para startups",
        )
        tema = (payload or {}).get("tema") or default_topic
        inputs = {"tema": tema}

        result: Dict[str, Any] = {}
        for output in agent_app.stream(inputs):
            # Emitir progreso básico cada iteración
            _publish_event("task_progress", {"id": task_id, "type": "magazine", "message": "procesando..."})
            for key, value in output.items():
                if key in ["contenido_curado", "pdf_path"]:
                    result[key] = value

        pdf_path = result.get("pdf_path")
        pdf_url = None
        if pdf_path:
            safe_path = str(pdf_path).replace("\\", "/")
            pdf_url = f"/{safe_path}"

        # Persist PDF metadata in DB if user_id present
        try:
            user_id = None
            try:
                user_id = int((payload or {}).get("user_id"))
            except Exception:
                user_id = None
            if pdf_url and user_id:
                filename = os.path.basename(safe_path)
                size_bytes = None
                try:
                    fpath = os.path.join("outputs", os.path.basename(filename))
                    if os.path.exists(fpath):
                        size_bytes = os.path.getsize(fpath)
                except Exception:
                    pass
                db = SessionLocal()
                try:
                    row = db_models.Magazine(user_id=user_id, filename=filename, title=None, size_bytes=size_bytes)
                    db.add(row)
                    db.commit()
                finally:
                    db.close()
        except Exception:
            pass

        _finish_task_status(task_id, "succeeded")
        # Persistir resultado para fallback de polling
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={
                    "result": json.dumps({"pdf_url": pdf_url, "contenido_curado": result.get("contenido_curado", [])}, ensure_ascii=False)
                })
        except Exception:
            pass
        _publish_event("task_succeeded", {"id": task_id, "type": "magazine", "result": {"pdf_url": pdf_url, "contenido_curado": result.get("contenido_curado", [])}})
        # Notificar API: completed + result_url para frontend
        try:
            meta = {"result_url": pdf_url, "contenido_curado": result.get("contenido_curado", [])}
            _post_flow_status(task_id, status="completed", name="Generación de Magazine", meta=meta)
        except Exception:
            pass
        # Enviar email al completar
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                body = "Flujo 'Generar Magazine' terminado exitosamente."
                attachments = []
                if pdf_url and pdf_url.startswith("/outputs/"):
                    attachments = [os.path.join("outputs", os.path.basename(pdf_url))]
                _send_smtp(sender, to, "Flujo magazine terminado exitosamente", body, attachments)
        except Exception:
            pass
        finally:
            try:
                uid = None
                try:
                    uid = int((payload or {}).get("user_id"))
                except Exception:
                    uid = None
                if uid:
                    _release_flow_lock(f"magazine:{uid}")
                else:
                    _release_flow_lock("magazine")
            except Exception:
                pass
        return {"status": "success", "pdf_url": pdf_url, "contenido_curado": result.get("contenido_curado", [])}

    except Exception as e:
        _finish_task_status(task_id, "failed")
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={"error": str(e)})
        except Exception:
            pass
        _publish_event("task_failed", {"id": task_id, "type": "magazine", "error": str(e)})
        # Notificar API: error
        try:
            _post_flow_status(task_id, status="error", name="Generación de Magazine", meta={"error": str(e)})
        except Exception:
            pass
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                _send_smtp(sender, to, "Flujo magazine falló", f"Error: {str(e)}", [])
        except Exception:
            pass
        finally:
            try:
                uid = None
                try:
                    uid = int((payload or {}).get("user_id"))
                except Exception:
                    uid = None
                if uid:
                    _release_flow_lock(f"magazine:{uid}")
                else:
                    _release_flow_lock("magazine")
            except Exception:
                pass
        self.update_state(state=states.FAILURE, meta={"exc": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.run_requisitos", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2})
def run_requisitos(self, payload: Dict[str, Any] | None = None):
    task_id = self.request.id or f"req_{int(time.time())}"
    _set_task_status(task_id, {"id": task_id, "type": "requisitos", "status": "running", "created": datetime.utcnow().isoformat()})
    _post_flow_status(task_id, status="running", name="Extracción de Requisitos")
    _publish_event("task_started", {"id": task_id, "type": "requisitos"})

    try:
        item_id = int((payload or {}).get("item_id"))
    except Exception:
        _finish_task_status(task_id, "failed")
        _publish_event("task_failed", {"id": task_id, "type": "requisitos", "error": "item_id requerido"})
        return

    try:
        import os, json, requests
        from bs4 import BeautifulSoup
        from datetime import datetime as _dt
        try:
            from backend.agent.nodes import llm as agent_llm  # type: ignore
        except Exception:
            agent_llm = None

        json_path = os.path.join("outputs", "convocatorias.json")
        items = []
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                items = json.load(f)
        except Exception:
            items = []
        item = next((it for it in items if int(it.get("id", -1)) == int(item_id)), None)
        if not item:
            raise RuntimeError("Convocatoria no encontrada")

        url = item.get("url") or item.get("source")
        if not url:
            reqs = ["No especificado"]
        else:
            try:
                resp = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                resp.raise_for_status()
                soup = BeautifulSoup(resp.content, 'html.parser')
                text = soup.get_text(" ", strip=True)
            except Exception as e:
                text = f"No se pudo acceder a la URL: {e}"

            prompt = f"""
            Devuelve SOLO JSON: {{"requirements": ["..."]}}
            Título: {item.get('title')}
            Tipo: {item.get('type')}
            Enlace: {url}
            Texto: {text[:6000]}
            """
            reqs = ["No especificado"]
            if agent_llm is not None:
                try:
                    raw = agent_llm.invoke(prompt).content
                    import re as _re, json as _json
                    m = _re.search(r"\{.*\}", raw, _re.DOTALL)
                    js = _json.loads(m.group(0) if m else raw)
                    r = js.get("requirements")
                    if isinstance(r, list) and r:
                        reqs = [str(x).strip() for x in r if str(x).strip()]
                except Exception:
                    pass

        try:
            changed = False
            for it in items:
                if int(it.get("id", -1)) == int(item_id):
                    it["requisitos"] = reqs or ["No especificado"]
                    changed = True
                    break
            if changed:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(items, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        _finish_task_status(task_id, "succeeded")
        # Persistir resultado para fallback de polling
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={
                    "result": json.dumps({"id": item_id, "requirements": reqs}, ensure_ascii=False)
                })
        except Exception:
            pass
        _publish_event("task_succeeded", {"id": task_id, "type": "requisitos", "result": {"id": item_id, "requirements": reqs}})
        # Notificar API: completed
        try:
            _post_flow_status(task_id, status="completed", name="Extracción de Requisitos", meta={"id": item_id, "requirements": reqs})
        except Exception:
            pass
        # Email éxito
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                body = f"Flujo 'Ver Requisitos' terminado. ID={item_id}. Total requisitos: {len(reqs or [])}."
                _send_smtp(sender, to, "Flujo requisitos terminado exitosamente", body, [])
        except Exception:
            pass
        return {"status": "success", "id": item_id, "requirements": reqs}
    except Exception as e:
        _finish_task_status(task_id, "failed")
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={"error": str(e)})
        except Exception:
            pass
        _publish_event("task_failed", {"id": task_id, "type": "requisitos", "error": str(e)})
        # Notificar API: error
        try:
            _post_flow_status(task_id, status="error", name="Extracción de Requisitos", meta={"error": str(e)})
        except Exception:
            pass
        # Email error
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                _send_smtp(sender, to, "Flujo requisitos falló", f"Error: {str(e)}", [])
        except Exception:
            pass
        self.update_state(state=states.FAILURE, meta={"exc": str(e)})
        raise
    finally:
        try:
            uid = None
            try:
                uid = int((payload or {}).get("user_id"))
            except Exception:
                uid = None
            if uid:
                _release_flow_lock(f"requisitos:{uid}")
            else:
                _release_flow_lock("requisitos")
        except Exception:
            pass


@celery_app.task(bind=True, name="tasks.run_fuentes", autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1})
def run_fuentes(self, payload: Dict[str, Any] | None = None):
    task_id = self.request.id or f"src_{int(time.time())}"
    _set_task_status(task_id, {"id": task_id, "type": "fuentes", "status": "running", "created": datetime.utcnow().isoformat()})
    _post_flow_status(task_id, status="running", name="Descubrimiento de Fuentes")
    _publish_event("task_started", {"id": task_id, "type": "fuentes"})

    try:
        try:
            from backend.agent.tools import search_all as web_search_all  # type: ignore
        except Exception:
            web_search_all = None

        tema = (payload or {}).get("tema") or os.getenv("DEFAULT_TOPIC", "convocatorias de financiación y eventos en ciencia y tecnología")
        queries = (payload or {}).get("queries")
        if web_search_all is None:
            results = []
        else:
            results = web_search_all(tema, custom_queries=queries) if queries else web_search_all(tema)

        _finish_task_status(task_id, "succeeded")
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={
                    "result": json.dumps({"tema": tema, "items": results[:10]}, ensure_ascii=False)
                })
        except Exception:
            pass
        _publish_event("task_succeeded", {"id": task_id, "type": "fuentes", "result": {"tema": tema, "items": results[:10]}})
        # Notificar API: completed
        try:
            _post_flow_status(task_id, status="completed", name="Descubrimiento de Fuentes", meta={"tema": tema, "items": results[:10]})
        except Exception:
            pass
        # Email éxito
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                body = f"Flujo 'Búsqueda de Fuentes' terminado. Tema='{tema}'. Items: {len(results or [])}."
                _send_smtp(sender, to, "Flujo fuentes terminado exitosamente", body, [])
        except Exception:
            pass
        return {"status": "success", "tema": tema, "items": results}
    except Exception as e:
        _finish_task_status(task_id, "failed")
        try:
            r = _get_redis()
            if r:
                r.hset(f"task:{task_id}", mapping={"error": str(e)})
        except Exception:
            pass
        _publish_event("task_failed", {"id": task_id, "type": "fuentes", "error": str(e)})
        # Notificar API: error
        try:
            _post_flow_status(task_id, status="error", name="Descubrimiento de Fuentes", meta={"error": str(e)})
        except Exception:
            pass
        # Email error
        try:
            sender = os.getenv("SMTP_USER") or ""
            user_email = (payload or {}).get("user_email")
            fallback = os.getenv("TEST_EMAIL") or ""
            to = [e for e in [user_email or fallback] if e]
            if sender and to:
                _send_smtp(sender, to, "Flujo fuentes falló", f"Error: {str(e)}", [])
        except Exception:
            pass
        self.update_state(state=states.FAILURE, meta={"exc": str(e)})
        raise
    finally:
        try:
            uid = None
            try:
                uid = int((payload or {}).get("user_id"))
            except Exception:
                uid = None
            if uid:
                _release_flow_lock(f"fuentes:{uid}")
            else:
                _release_flow_lock("fuentes")
        except Exception:
            pass
