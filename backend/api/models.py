from pydantic import BaseModel, UUID4

from backend.models import Task

DEVICE_ID_HEADER = "X-Device-Id"


class DeleteTaskRequest(BaseModel):
    id: UUID4


class UpdateTasksRequest(BaseModel):
    list: list[Task]
    revision: int
