from fastapi.responses import FileResponse
import logging
import os

from utils import stack
from utils.const import BUILD_PATH


async def page(path: str) -> FileResponse:
    mname = stack.get_caller(depth=2)[0]
    if not mname.startswith('plugins.plugins.'):
        logging.error(f'Non-plugin called serve.page() API: "{mname}"')
        return FileResponse(f'{BUILD_PATH}/plugins')
    pname = mname.split('.')[2]
    fpath = f'{BUILD_PATH}/plugins/{pname}/{path}.html'
    if not os.path.exists(fpath):
        logging.error(f'Plugin page "{path}" for plugin "{pname}" does not exist')
        return FileResponse(f'{BUILD_PATH}/dne.html')
    return FileResponse(fpath)
