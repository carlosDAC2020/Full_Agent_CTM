import os
from celery import Celery
import sys

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


celery_app = Celery(
    "magazine_tasks",
    broker=broker_url,
    backend=result_backend,
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
    import Intecmar_api.backend.app.workers.magazine.tasks  # noqa: F401
except Exception:
    pass
