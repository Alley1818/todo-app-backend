from sqlalchemy.orm import Session
from app.models.task import TaskORM
from sqlalchemy import select


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_tasks(self):
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id:str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    def create_task(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete_task(self, task_id: str):
        task = self.db.get(TaskORM, task_id)
        self.db.delete(task)