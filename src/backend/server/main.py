from fastapi import FastAPI
from fastapi.responses import FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles

from utils import status

app = FastAPI()
app.mount('/assets', StaticFiles(directory='../public/assets'), name='static')


@app.get('/', response_class=FileResponse)
async def home():
    return '../public/login.html'


@app.get('/favicon.png', include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse('../public/favicon.png')


@app.get('/login/status', response_class=ORJSONResponse)
async def login_info() -> ORJSONResponse:
    return ORJSONResponse(status.get())
