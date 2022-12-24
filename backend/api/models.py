from pydantic import BaseModel

from backend.models import Task


class AddTasksRequest(BaseModel):
    list: list[Task]
    revision: int


class UpdateTasksRequest(BaseModel):
    list: list[Task]
    revision: int
