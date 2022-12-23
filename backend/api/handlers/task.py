from typing import Any

from aiohttp import web

from backend.api.models import DeleteTaskRequest, UpdateTasksRequest
from backend.app.errors import OutdatedRevisionError
from backend.interfaces import TaskService
from backend.models import Task
from .base import ProtectedHandler


class TaskHandler(ProtectedHandler):
    PATH = '/api/tasks'

    @property
    def service(self) -> TaskService:
        return self.request.app['task_service']

    async def get(self) -> tuple[int, Any]:
        tasks, revision = await self.service.get_tasks(self.user_id)
        for i, task in enumerate(tasks):
            tasks[i] = task.dict()
        return web.HTTPOk.status_code, {'list': tasks, 'revision': revision}

    async def post(self) -> tuple[int, Any]:
        body = await self.request.json()
        task = Task(**body)
        revision = await self.service.add_task(self.user_id, task)
        return web.HTTPCreated.status_code, {'element': task.dict(), 'revision': revision}

    async def delete(self) -> tuple[int, Any]:
        body = await self.request.json()
        data = DeleteTaskRequest(**body)
        revision = await self.service.delete_task(self.user_id, data.id)
        return web.HTTPOk.status_code, {'revision': revision}

    async def patch(self) -> tuple[int, Any]:
        body = await self.request.json()
        task = Task(**body)
        revision = await self.service.update_task(self.user_id, task)
        return web.HTTPOk.status_code, {'revision': revision}

    async def put(self) -> tuple[int, Any]:
        body = await self.request.json()
        data = UpdateTasksRequest(**body)
        try:
            revision = await self.service.update_tasks(self.user_id, data.list, data.revision)
        except OutdatedRevisionError as e:
            return web.HTTPConflict.status_code, {'revision': e.actual}
        return web.HTTPOk.status_code, {'revision': revision}
