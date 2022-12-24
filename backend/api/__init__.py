from aiohttp import web

from .handlers import (
    PingHandler,
    GetTasksHandler, GetTaskHandler,
    AddTasksHandler, DeleteTaskHandler,
    UpdateTaskHandler, UpdateTasksHandler
)
from .middlewares import logging_middleware, error_middleware, auth_middleware, encoding_middleware

MIDDLEWARES = [logging_middleware, error_middleware, auth_middleware, encoding_middleware]


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PingHandler.PATH, PingHandler)
    router.add_view(GetTasksHandler.PATH, GetTaskHandler)
    router.add_view(GetTaskHandler.PATH, GetTasksHandler)
    router.add_view(AddTasksHandler.PATH, AddTasksHandler)
    router.add_view(DeleteTaskHandler.PATH, DeleteTaskHandler)
    router.add_view(UpdateTaskHandler.PATH, UpdateTaskHandler)
    router.add_view(UpdateTasksHandler.PATH, UpdateTasksHandler)


__all__ = ('MIDDLEWARES', 'register_handlers')
