from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskService

from app.core.config import get_settings
from app.services.task import TaskService


def get_task_service(
    db=Depends(get_db), 
    settings=Depends(get_settings)
) -> TaskService:
    return TaskService(
        db=db,
        redis_url=settings.redis_url,
        cache_ttl=settings.cache_ttl,
        cache_tasks_key=settings.cache_tasks_key,
    )