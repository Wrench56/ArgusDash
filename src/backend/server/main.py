from fastapi import FastAPI
from fastapi.responses import FileResponse, ORJSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from utils import const, status

app = FastAPI()
app.mount('/assets', StaticFiles(directory='../public/assets'), name='static')


@app.get('/favicon', include_in_schema=False)
@app.get('/favicon.ico', include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse('../public/favicon.png')


@app.get('/version', response_class=PlainTextResponse)
async def version() -> PlainTextResponse:
    return PlainTextResponse(const.VERSION)


# Login
@app.get('/', response_class=FileResponse)
async def home():
    return '../public/login.html'


@app.get('/login/status', response_class=ORJSONResponse)
async def login_info() -> ORJSONResponse:
    return ORJSONResponse(status.get())
