from sqlalchemy.orm import Session
from app.cache.redis import RedisCacheBackend
from app.repository.task import  TaskRepository
from app.schemas.task import TaskSchema, CreateTaskSchema, UpdateTaskScheme


class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db:Session, redis_url:str, cache_ttl:int, cache_tasks_key: str):
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = RedisCacheBackend(redis_url, cache_ttl)
        self.cache_tasks_key = cache_tasks_key

    def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = self.cache.get(self.cache_tasks_key) 
        if cached_tasks:
            return [TaskSchema.model_validate(task) for task in cached_tasks] 
        
        task_orm = self.task_repository.get_all_tasks()
        
        tasks_read = [TaskSchema.model_validate(task) for task in task_orm]
        tasks_for_cache = [task.model_dump(mode="json") for task in tasks_read]
        self.cache.set(self.cache_tasks_key, tasks_for_cache)        
        
        return tasks_read

    def create_task(self, task_create:CreateTaskSchema):
        
        task_orm = self.task_repository.create_task(title=task_create.title)
        self.db.commit()
        self.cache.delete(self.cache_tasks_key)
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_update: UpdateTaskScheme, task_id: str) -> TaskSchema:
        task_to_update = self.task_repository.get_by_id(task_id = task_id)
        if not task_to_update:
                raise TaskNotFound("Задача не найдена")
        new_data = task_update.model_dump(exclude_unset=True)
        for field, value in new_data.items():
            setattr(task_to_update, field, value)
        self.db.commit()
        self.db.refresh(task_to_update)
        self.cache.delete(self.cache_tasks_key)
        return TaskSchema.model_validate(task_to_update)     

    def delete_task(self, task_id:str) -> None:
        task_to_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_to_delete:
                raise TaskNotFound("Задача не найдена")
        self.task_repository.delete_task(task_id)
        self.db.commit()
        self.cache.delete(self.cache_tasks_key)
     