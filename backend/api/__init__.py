from aiohttp import web

from .handlers import PingHandler, TaskHandler
from .middlewares import logging_middleware, error_middleware, auth_middleware, encoding_middleware

MIDDLEWARES = [logging_middleware, error_middleware, auth_middleware, encoding_middleware]


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PingHandler.PATH, PingHandler)
    router.add_view(TaskHandler.PATH, TaskHandler)


__all__ = ('MIDDLEWARES', 'register_handlers')
