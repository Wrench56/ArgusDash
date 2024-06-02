import datetime
import logging

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, ORJSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from db import users
from utils import config, const, status

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


# Login
@app.get('/', response_class=FileResponse)
async def login_page() -> FileResponse:
    return FileResponse('../public/login.html')


@app.get('/login/status', response_class=ORJSONResponse)
async def login_info() -> ORJSONResponse:
    return ORJSONResponse(status.get())

@app.post('/auth', response_class=PlainTextResponse)
async def login(request: Request) -> PlainTextResponse:
    data = await request.json()
    response = PlainTextResponse()
    username = data.get('username')

    if not database.is_valid(username, data.get('password')):
        return response

    uuid = database.create_uuid(username)
    logging.info(f'Welcome user "{username}"!')
    expire_time = float(config.get('security').get('auth_cookie_expire_time') or 3600.0)
    response.set_cookie(key='auth_cookie', value=uuid, expires=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expire_time))
    return response


# Dashboard
@app.get('/dashboard', response_class=ORJSONResponse)
async def dashboard_page(request: Request) -> FileResponse:
    if database.uuid_exists(request.cookies.get('auth_cookie')):
        return FileResponse('../public/dashboard.html')
    return FileResponse('../public/blocked.html')
