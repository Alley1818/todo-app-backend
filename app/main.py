from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(_:FastAPI):
     Base.metadata.create_all(bind=engine)
     yield 

app = FastAPI(lifespan=lifespan)



app.add_middleware(
     CORSMiddleware,
     allow_origins=["http://localhost:3000",
        "http://127.0.0.1:3000"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)


def from_orm_to_model(task_orm:TaskORM) -> TaskSchema:
     task = TaskSchema(id=task_orm.id, title = task_orm.title, completed = task_orm.completed)
     return task

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
     tasks_from_db = db.scalars(select(TaskORM)).all()
     return [from_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_tasks(payload: CreateTaskSchema, db: Session = Depends(get_db)):
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_status(task_id: str, payload: UpdateTaskScheme, db: Session = Depends(get_db)):
    updated_task = db.get(TaskORM, task_id)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    if payload.title is not None:
        updated_task.title = payload.title
    if payload.completed is not None:
        updated_task.completed = payload.completed

    db.commit()
    db.refresh(updated_task)
    
    return updated_task


@app.delete("/tasks/{task_id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db:Session=Depends(get_db)):
     deleted_task = db.get(TaskORM, task_id)
     if not deleted_task:
          raise HTTPException (
               status_code = HTTP_404_NOT_FOUND,
               detail = "Error"
          )
     db.delete(deleted_task)
     db.commit()
