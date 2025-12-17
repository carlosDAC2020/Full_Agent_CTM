import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Path

from backend.app.core.config import settings
from backend.app.schemas.source import SourcesSearchRequest, SourcesAISearchRequest, SourceCreate, SourceUpdate
from backend.app.utils.files import load_json_list, save_json_list
from backend.app.services.agent_service import llm_invoke, search_web

router = APIRouter(prefix="/sources", tags=["sources"])

@router.get("")
async def get_sources() -> List[Dict[str, Any]]:
    return load_json_list(settings.SOURCES_FILE)

@router.post("")
async def create_source(src: SourceCreate):
    items = load_json_list(settings.SOURCES_FILE)
    
    def _next_id(items):
        if not items: return 1
        return max((int(x.get("id", 0)) for x in items), default=0) + 1
        
    new_obj = {"id": _next_id(items), "name": src.name, "type": src.type or "", "url": src.url, "hidden": False}
    items.append(new_obj)
    save_json_list(settings.SOURCES_FILE, items)
    return new_obj

@router.put("/{source_id}")
async def update_source(source_id: int = Path(...), patch: SourceUpdate = None):
    items = load_json_list(settings.SOURCES_FILE)
    for it in items:
        if int(it.get("id", -1)) == int(source_id):
            if patch.name is not None: it["name"] = patch.name
            if patch.type is not None: it["type"] = patch.type
            if patch.url is not None: it["url"] = patch.url
            if patch.hidden is not None: it["hidden"] = bool(patch.hidden)
            save_json_list(settings.SOURCES_FILE, items)
            return it
    raise HTTPException(status_code=404, detail="Source no encontrada")

@router.patch("/{source_id}/toggle")
async def toggle_source(source_id: int = Path(...)):
    items = load_json_list(settings.SOURCES_FILE)
    for it in items:
        if int(it.get("id", -1)) == int(source_id):
            it["hidden"] = not bool(it.get("hidden", False))
            save_json_list(settings.SOURCES_FILE, items)
            return it
    raise HTTPException(status_code=404, detail="Source no encontrada")

@router.delete("/{source_id}")
async def delete_source(source_id: int = Path(...)):
    items = load_json_list(settings.SOURCES_FILE)
    initial_len = len(items)
    items = [it for it in items if int(it.get("id", -1)) != int(source_id)]
    if len(items) == initial_len:
        raise HTTPException(status_code=404, detail="Source no encontrada")
    save_json_list(settings.SOURCES_FILE, items)
    return {"status": "success", "message": "Source eliminada"}

@router.post("/search")
async def search_sources(payload: SourcesSearchRequest):
    q = (payload.query or '').strip()
    if not q:
        return {"results": []}

    existing = load_json_list(settings.SOURCES_FILE)

    def _norm(u: str) -> str:
        try:
            p = urlparse(u)
            host = (p.netloc or '').lower().lstrip('www.')
            path = (p.path or '').rstrip('/')
            return f"{host}{path}"
        except Exception:
            return (u or '').lower().strip()

    existing_map = { _norm(s.get('url', '')): s for s in existing }

    hits = search_web(q, tavily_max=3, brave_max=1)

    results = []
    for h in hits:
        url = h.get('url') or ''
        title = h.get('title') or url
        key = _norm(url)
        matched = existing_map.get(key)
        results.append({
            "title": title,
            "url": url,
            "exists": matched is not None,
            "id": matched.get('id') if matched else None
        })

    results.sort(key=lambda x: (x.get('exists', False), (x.get('title') or '').lower()))
    return {"results": results}

@router.post("/ai_search")
async def ai_search_sources(payload: SourcesAISearchRequest | None = None):
    fixed_topics = ["inteligencia artificial", "ciencia", "tecnología", "naval"]
    
    # Generate queries with LLM
    try:
        prompt = f"""
        Eres un experto en OSINT. Devuelve SOLAMENTE 8 consultas de búsqueda (una por línea).
        Temas: {', '.join(fixed_topics)}.
        Enfócate en sitios gubernamentales, multilaterales, universidades.
        """
        raw = llm_invoke(prompt).strip()
        consultas = [c.strip() for c in raw.splitlines() if c.strip()][:8]
    except Exception:
        consultas = []
    
    if not consultas:
         consultas = [
            "portal convocatorias inteligencia artificial site:.gov OR site:.edu",
            "funding opportunities artificial intelligence grants database",
            "convocatorias ciencia universidad portal investigación",
            "portal convocatorias tecnología ministerio site:.gov"
        ]

    hits = []
    for q in consultas:
        hits.extend(search_web(q, tavily_max=2, brave_max=1))

    # Dedupe & Check existing
    def _norm(u: str) -> str:
        try:
            p = urlparse(u)
            host = (p.netloc or '').lower().lstrip('www.')
            path = (p.path or '').rstrip('/')
            return f"{host}{path}"
        except Exception:
            return (u or '').lower().strip()
            
    existing = load_json_list(settings.SOURCES_FILE)
    existing_map = { _norm(s.get('url', '')): s for s in existing }
    
    seen = set()
    unique = []
    for h in hits:
        url = h.get('url') or ''
        if not url: continue
        key = _norm(url)
        if key in seen: continue
        seen.add(key)
        unique.append({"title": h.get('title') or url, "url": url})
        
    results = []
    for it in unique:
        url = it['url']
        k = _norm(url)
        matched = existing_map.get(k)
        results.append({
            "title": it['title'],
            "url": url,
            "exists": matched is not None,
            "id": matched.get('id') if matched else None
        })
        
    results.sort(key=lambda x: (x.get('exists', False), (x.get('title') or '').lower()))
    return {"results": results, "queries": consultas}

# Requirements endpoint (was at root in main_api but logically relates to sources/convocatorias)
@router.get("/../requirements/{item_id}") # Wait, prefix is /sources. Should this be /sources/requirements/{id} or /requirements/{id}?
# User plan said "endpoints/sources.py" but didn't specify url structure. 
# main_api had /requirements. I will expose it on APIRouter but maybe with prefix or just standard router.
# Let's put it in a separate block or router without prefix in api_v1?
# It's better to group it. I'll make a separate router instance or just include it here but note the URL might change to /sources/requirements/..
# Or I can just define it as @router.get("/requirements/{item_id}") which becomes /sources/requirements/{item_id}.
# The original was /requirements/{item_id}.
# I will put it in a separate general router or here. 
# Let's add it here as /requirements/{item_id} (relative to this file, but exposed how?).
# I'll put it here.
async def get_requirements(item_id: int): 
    # Logic from main_api.py lines 674-768
    # ...
    # Wait, the decorator above is inside /sources prefix if I mount it that way.
    # I should place this in a generic "convocatorias" endpoint or keep it in utils? 
    # Or just api/endpoints/magazines.py if it relates to generation?
    # It relates to 'convocatorias.json' items.
    pass

# To avoid URL breaking, I should probably put it in magazines.py or a new convocatorias.py
# Using sources.py for now but I will mount it carefully.
