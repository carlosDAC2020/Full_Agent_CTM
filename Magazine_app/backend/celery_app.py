import os
from celery import Celery
import sys

# Ensure sys path includes root for backend package resolution if run directly
_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.join(_CUR_DIR, '..')
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from backend.app.core.config import settings

celery_app = Celery(
    "magazine_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "backend.tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    worker_max_tasks_per_child=100,
    task_default_queue='magazine',
    task_routes={
        'backend.tasks.*': {'queue': 'magazine'},
    }
)

# Explicit import to ensure task registration when worker starts
try:
    import backend.tasks  # noqa: F401
except Exception:
    pass
