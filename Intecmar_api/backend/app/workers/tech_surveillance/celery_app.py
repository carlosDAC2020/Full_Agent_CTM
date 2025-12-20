from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://shared_redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://shared_redis:6379/0")

celery_app = Celery(
    "agent_worker",
    broker=broker_url,
    backend=result_backend,
    include=["backend.app.workers.tech_surveillance.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue='agent',
    task_routes={
        'backend.app.workers.tech_surveillance.tasks.*': {'queue': 'agent'},
    }
)

# Explicit import to ensure task registration when worker starts
try:
    import backend.app.workers.tech_surveillance.tasks  
except Exception:
    pass