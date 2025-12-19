import os
import json
from typing import Optional, Dict, Any, Union
from backend.app.core.config import settings

try:
    from redis import Redis
except Exception:
    Redis = None  # type: ignore

def get_redis() -> Optional["Redis"]:
    if Redis is None:
        return None
    try:
        return Redis.from_url(settings.REDIS_URL)
    except Exception:
        return None

def task_key(task_id: str) -> str:
    return f"task:{task_id}"

def flow_lock_key(flow_type: str) -> str:
    return f"flow_lock:{flow_type}"

def acquire_flow_lock(r: "Redis", flow_type: str, ttl: int = 60 * 60) -> bool:
    try:
        return bool(r.set(flow_lock_key(flow_type), "1", nx=True, ex=ttl))
    except Exception:
        return True  # be permissive if no redis

def release_flow_lock(r: Optional["Redis"], flow_type: str):
    if not r:
        return
    try:
        r.delete(flow_lock_key(flow_type))
    except Exception:
        pass
