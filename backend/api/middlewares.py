import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import UUID

from aiohttp import web
from pydantic import ValidationError

logger = logging.getLogger(__name__)


@web.middleware
async def logging_middleware(request: web.Request, handler: Callable) -> web.Response:
    response: web.Response = await handler(request)
    log_message = ' '.join([
        f'method={request.method}',
        f'uri={request.path}',
        f'status={response.status}'
    ])
    if response.status >= 500:
        logger.error(log_message)
    elif response.status >= 400:
        logger.info(log_message)
    return response


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return int(o.timestamp())
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


@web.middleware
async def encoding_middleware(request: web.Request, handler: Callable) -> web.Response:
    status, data = await handler(request)
    if data is not None:
        encoded_data = json.dumps(data, cls=Encoder)
        return web.Response(body=encoded_data, status=status, content_type='application/json')
    return web.Response(status=status)


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> tuple[int, Any | None]:
    try:
        return await handler(request)
    except ValidationError as e:
        return web.HTTPBadRequest.status_code, {'validation_error': e.errors()}
    except web.HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e, exc_info=True)
        return web.HTTPInternalServerError.status_code, None
