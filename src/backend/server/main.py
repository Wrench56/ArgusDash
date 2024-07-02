from typing import Any

import datetime
import logging

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, ORJSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from api import expose
from db import users
from server import build
from utils import config, const, motd, settings, status

database = users.Database()

app = FastAPI()
app.mount('/assets', StaticFiles(directory='../public/assets'), name='static')


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
async def login_page() -> FileResponse:
    return FileResponse('../public/login.html')


@app.get('/login/motd', response_class=PlainTextResponse)
async def motd_text() -> PlainTextResponse:
    return PlainTextResponse(motd.format_(config.get('frontend').get('motd'), database))


@app.post('/auth', response_class=PlainTextResponse)
async def login(request: Request) -> PlainTextResponse:
    data = await request.json()
    response = PlainTextResponse()
    username = data.get('username')

    if not database.is_valid(username, data.get('password')):
        return response

    uuid = database.create_uuid(username)
    logging.info(f'Welcome user "{username}"!')
    expire_time = float(config.get('security').get(
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
@app.get('/plugins/{plugin}/{endpoint:path}')
@app.put('/plugins/{plugin}/{endpoint:path}')
@app.post('/plugins/{plugin}/{endpoint:path}')
@app.delete('/plugins/{plugin}/{endpoint:path}')
async def plugins(request: Request, plugin: str, endpoint: str) -> Any:
    response = PlainTextResponse()
    if not database.uuid_exists(request.cookies.get('auth_cookie')):
        response.status_code = 401
        return response

    # Remove sensitive cookie(s)
    request.cookies['auth_cookie'] = ''
    callback = expose.fetch_callback(plugin, endpoint, request.method)
    if callback:
        return callback(endpoint, request)
    return response
