from celery import Celery
from .config import settings

celery_app = Celery(
    "catalog_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.import_tasks",
        "app.tasks.export_tasks",
        "app.tasks.merge_tasks"
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Optional: Configure task routes
celery_app.conf.task_routes = {
    "app.tasks.import_tasks.*": {"queue": "imports"},
    "app.tasks.export_tasks.*": {"queue": "exports"},
    "app.tasks.merge_tasks.*": {"queue": "merges"},
}
