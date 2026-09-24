from pydantic import BaseModel

class TaskSchema(BaseModel):
     id: str
     title: str
     completed: bool

class CreateTaskSchema(BaseModel):
     title: str

class UpdateTaskScheme(BaseModel):
     title: str | None = None
     completed:bool | None = None
