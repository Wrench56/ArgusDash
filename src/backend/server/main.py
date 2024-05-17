from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
 
app = FastAPI()
app.mount('/assets', StaticFiles(directory='../public/assets'), name='static')

@app.get('/', response_class=FileResponse)
async def home():
    return '../public/login.html'

@app.get('/favicon.png', include_in_schema=False)
async def favicon():
    return FileResponse('../public/favicon.png')