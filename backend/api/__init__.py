from aiohttp import web

from .handlers import TaskHandler
from .middlewares import logging_middleware, encoding_middleware, error_middleware

MIDDLEWARES = [logging_middleware, encoding_middleware, error_middleware]

PREFIX = '/api/tasks'


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PREFIX, TaskHandler)


__all__ = ('MIDDLEWARES', 'register_handlers')
