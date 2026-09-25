from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT
from app.api.dependencies import get_task_service
from app.schemas.task import CreateTaskSchema, TaskSchema, UpdateTaskScheme
from app.services.task import TaskNotFound, TaskService


router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service:TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()



@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_tasks(payload: CreateTaskSchema, task_service:TaskService = Depends(get_task_service)) -> TaskSchema:
    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}", response_model=TaskSchema)
def update_status(task_id: str, payload: UpdateTaskScheme, task_service:TaskService = Depends(get_task_service)) -> TaskSchema:
    try:
        return task_service.update_task(task_update=payload, task_id=task_id)
    except TaskNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service:TaskService = Depends(get_task_service)) -> None:
    try:
        return task_service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

