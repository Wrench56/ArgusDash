from typing import Any, Callable, Dict, Optional

from fastapi import Request

from utils import stack

_SUBSCRIBERS: Dict[str, Dict[str,
                             Dict[str, Callable[[str, Request], Any]]]] = {
    'GET': {},
    'PUT': {},
    'POST': {},
    'DELETE': {}
}


def subscribe_get(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, _SUBSCRIBERS['GET'], callback)


def subscribe_put(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, _SUBSCRIBERS['PUT'], callback)


def subscribe_post(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, _SUBSCRIBERS['POST'], callback)


def subscribe_delete(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, _SUBSCRIBERS['DELETE'], callback)


def _subscribe(endpoint: str, structure: Dict, callback: Callable[[str, Request], Any]) -> None:
    module_name = stack.get_caller(depth=3)[0]
    if not module_name.startswith('plugins.plugins.'):
        return

    plugin_name = module_name.split('.')[2]
    if plugin_name not in structure:
        structure[plugin_name] = {}

    structure[plugin_name][endpoint] = callback


def fetch_callback(plugin: str, endpoint: str, method: str) -> Optional[Callable[[str, Request], Any]]:
    endpoints = _SUBSCRIBERS[method.upper()].get(plugin)
    if endpoints is None:
        return None
    if endpoint[-1] == '/':
        endpoint = endpoint[:-1]
    return endpoints.get(endpoint)
