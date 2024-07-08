from fastapi.responses import FileResponse
import logging
import os

from utils import config, stack

_BUILD_PATH = None


async def page(path: str) -> FileResponse:
    _cache_buildpath()
    mname = stack.get_caller(depth=2)[0]
    if not mname.startswith('plugins.plugins.'):
        logging.error(f'Non-plugin called serve.page() API: "{mname}"')
        return FileResponse(f'{_BUILD_PATH}/plugins')
    pname = mname.split('.')[2]
    fpath = f'{_BUILD_PATH}/plugins/{pname}/{path}.html'
    if not os.path.exists(fpath):
        logging.error(f'Plugin page "{path}" for plugin "{pname}" does not exist')
        return FileResponse(f'{_BUILD_PATH}/dne.html')
    return FileResponse(fpath)


def _cache_buildpath() -> None:
    global _BUILD_PATH
    if _BUILD_PATH is None:
        _BUILD_PATH = config.fetch().get("frontend").get("build_path")
