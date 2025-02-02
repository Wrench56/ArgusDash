from typing import Any, AsyncGenerator

import asyncio
import datetime
import inspect
import json
import logging

from fastapi import BackgroundTasks, FastAPI, Request, WebSocket
from fastapi.responses import FileResponse, ORJSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from api import expose
from db import users
from plugins import downloader, handler, widgets
from server import build
from server.endpoint_filter import EndpointFilter
from utils import cleanup, config, const, motd, settings, status

database = users.Database()

app = FastAPI()
app.mount('/assets', StaticFiles(directory='../public/assets'), name='static')

# Note: Put this after FastAPI init!
# cleanup.init(...) uses the previously
# set signal handler.
cleanup.init('server')

# Ignore /ping logs
uvicorn_logger = logging.getLogger('uvicorn.access')
uvicorn_logger.addFilter(EndpointFilter(path='/ping'))


@app.get('/favicon.png', include_in_schema=False)
@app.get('/favicon.ico', include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse('../public/favicon.png')


@app.get('/version', response_class=PlainTextResponse)
async def version() -> PlainTextResponse:
    if status.get().get('version') is None:
        return PlainTextResponse('')
    return PlainTextResponse(const.VERSION)


@app.get('/status', response_class=ORJSONResponse)
async def login_status(request: Request) -> ORJSONResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return ORJSONResponse(status.get())
    return ORJSONResponse(status.filter_login_disabled(status.get()))


@app.get('/ping', response_class=PlainTextResponse)
async def ping() -> PlainTextResponse:
    return PlainTextResponse('PONG')


@app.post('/rebuild', response_class=PlainTextResponse)
async def rebuild(request: Request) -> PlainTextResponse:
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        return PlainTextResponse('ERROR: AUTH')

    build_time = build.build_frontend()
    if build_time < 0:
        return PlainTextResponse('ERROR: BUILD')
    build_size, units = build.get_frontend_size()
    return PlainTextResponse(
        f'REBUILT: Rebuilt in {
            build_time}ms\nSize of build folder: {build_size}{units}'
    )


# Login
@app.get('/', response_class=FileResponse)
async def login_page(bg_tasks: BackgroundTasks) -> FileResponse:
    bg_tasks.add_task(handler.load_all)
    return FileResponse('../public/login.html')


@app.get('/login/motd', response_class=PlainTextResponse)
async def motd_text() -> PlainTextResponse:
    return PlainTextResponse(motd.format_(config.fetch().get('frontend').get('motd'), database))


@app.post('/auth', response_class=PlainTextResponse)
async def login(request: Request) -> PlainTextResponse:
    data = await request.json()
    response = PlainTextResponse()
    username = data.get('username')

    if not database.is_valid(username, data.get('password')):
        return response

    uuid = database.create_uuid(username)
    logging.info(f'Welcome user "{username}"!')
    expire_time = float(config.fetch().get('security').get(
        'auth_cookie_expire_time') or 3600.0)
    response.set_cookie(
        key='auth_cookie',
        value=uuid,
        expires=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=expire_time),
    )
    return response


# Dashboard
@app.get('/dashboard', response_class=FileResponse)
async def dashboard_page(request: Request) -> FileResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return FileResponse('../public/dashboard.html')
    return FileResponse('../public/blocked.html')


# Settings
@app.get('/settings', response_class=FileResponse)
async def settings_page(request: Request) -> FileResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return FileResponse('../public/settings.html')
    return FileResponse('../public/blocked.html')


@app.get('/settings/all', response_class=PlainTextResponse)
async def all_settings(request: Request) -> PlainTextResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return PlainTextResponse(','.join(settings.get_all()))
    return PlainTextResponse(','.join(settings.get_default()))


@app.post('/settings/{id_}', response_class=PlainTextResponse)
async def update_setting(request: Request, id_: str) -> PlainTextResponse:
    response = PlainTextResponse()
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        response.status_code = 401
        return response

    data = await request.body()
    settings.update_setting(id_, data.decode())

    return response


# Plugins
@app.get('/plugins', response_class=FileResponse)
async def plugins_page(request: Request) -> FileResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return FileResponse('../public/plugins.html')
    return FileResponse('../public/blocked.html')


@app.post('/plugins')
async def install_plugin(request: Request) -> PlainTextResponse:
    response = PlainTextResponse()
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        response.status_code = 401
        return response

    data = await request.json()
    if data.get('url'):
        if not downloader.from_url(data.get('url')):
            response.status_code = 501

    return response


@app.get('/plugins/api/{plugin}/{endpoint:path}')
@app.put('/plugins/api/{plugin}/{endpoint:path}')
@app.post('/plugins/api/{plugin}/{endpoint:path}')
@app.delete('/plugins/api/{plugin}/{endpoint:path}')
async def plugins(request: Request, plugin: str, endpoint: str) -> Any:
    response = PlainTextResponse()
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        response.status_code = 401
        return response

    # Remove sensitive cookie(s)
    request.cookies['auth_cookie'] = ''

    # Run callback in async
    callback = expose.fetch_callback(plugin, endpoint, request.method)
    if callback is None:
        logging.error(f'Callback for "{plugin}/{endpoint}" does not exist')
        response.status_code = 503
        return response
    return_value = None
    if inspect.iscoroutinefunction(callback):
        return_value = await callback(endpoint, request)
    else:
        # Sync function detected
        logging.error(
            f'Plugin "{plugin}" uses synchronous functions, request blocked')
        response.status_code = 503
    if return_value is not None:
        return return_value
    return response


@app.websocket('/plugins/wsapi/{plugin}/{endpoint}')
async def ws_plugins(websocket: WebSocket, plugin: str, endpoint: str) -> Any:
    response = PlainTextResponse()
    if not database.uuid_exists(websocket.cookies.get('auth_cookie')):
        response.status_code = 401
        return response

    # Remove sensitive cookie(s)
    websocket.cookies['auth_cookie'] = ''

    # Run callback in async
    callback = expose.fetch_callback(plugin, endpoint, 'WEBSOCKET')
    if callback is None:
        logging.error(f'Callback for "{plugin}/{endpoint}" does not exist')
        response.status_code = 503
        return response

    if inspect.iscoroutinefunction(callback):
        await callback(endpoint, websocket)
    else:
        # Sync function detected
        logging.error(
            f'Plugin "{plugin}" uses synchronous functions, request blocked')
        response.status_code = 503
        return response


@app.get('/plugins/status', response_class=EventSourceResponse)
async def plugin_status(request: Request) -> EventSourceResponse:
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        return EventSourceResponse(content=iter(('Authentication failed',)), status_code=401)
    handler.set_update_flag()

    async def event_generator() -> AsyncGenerator[str, None]:
        while not cleanup.get_flag():
            if await request.is_disconnected():
                break

            if handler.is_updated():
                yield json.dumps(
                    {'ok': True, 'plugins': handler.get_plugin_statuses()}
                )
            await asyncio.sleep(1.0)

    return EventSourceResponse(event_generator(), media_type='text/event-stream')


@app.get('/plugins/widgets', response_class=ORJSONResponse)
async def plugin_widgets(request: Request) -> ORJSONResponse:
    response = ORJSONResponse(content={})
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        response.status_code = 401
        return response
    return ORJSONResponse(content=widgets.get())
