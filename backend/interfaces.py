from abc import ABC, abstractmethod

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncConnection

from .models import Task


class Service(ABC):
    @abstractmethod
    async def get_tasks(self, user_id: str) -> tuple[list[Task], int]:
        raise NotImplementedError()

    @abstractmethod
    async def add_task(self, user_id: str, task: Task) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, user_id: str, task_id: UUID4) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, user_id: str, task: Task):
        raise NotImplementedError()

    @abstractmethod
    async def update_tasks(self, user_id: str, tasks: list[Task], revision: int):
        raise NotImplementedError()


class Repository(ABC):
    @abstractmethod
    async def get_tasks(self, conn: AsyncConnection, user_id: str) -> list[Task]:
        raise NotImplementedError()

    @abstractmethod
    async def add_task(self, conn: AsyncConnection, user_id: str, task: Task) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get_revision(self, conn: AsyncConnection, user_id: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def set_init_revision(self, conn: AsyncConnection, user_id: str):
        raise NotImplementedError()

    @abstractmethod
    async def increment_revision(self, conn: AsyncConnection, user_id: str):
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, conn: AsyncConnection, user_id: str, task_id: UUID4) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, conn: AsyncConnection, user_id: str, task: Task) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_tasks(self, conn: AsyncConnection, user_id: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def add_tasks(self, conn: AsyncConnection, user_id: str, tasks: list[Task]):
        raise NotImplementedError()