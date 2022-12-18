from typing import Any

from aiohttp import web

from backend.app.errors import OutdatedRevisionError
from backend.interfaces import Service
from backend.models import Task
from .models import DeleteTaskRequest, UpdateTasksRequest

DEVICE_ID_HEADER = "X-Device-Id"
REVISION_HEADER = "X-Revision"


class BaseHandler(web.View):
    def __init__(self, request: web.Request):
        if request.headers.get(DEVICE_ID_HEADER) is None:
            raise web.HTTPForbidden(text=f'{DEVICE_ID_HEADER} header is not provided')
        self._device_id = request.headers[DEVICE_ID_HEADER]
        self._user_id = '3c719570-d434-4175-b9fe-278e08567fd5'
        super().__init__(request)

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def service(self) -> Service:
        return self.request.app['service']


class TaskHandler(BaseHandler):
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
