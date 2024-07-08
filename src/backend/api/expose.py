from typing import Any, Callable, List, Optional, Union

from fastapi import Request, WebSocket

from utils import stack

CallbackFunctionType = Callable[[str, Union[Request, WebSocket]], Any]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.callback: Optional[CallbackFunctionType] = None

    def __str__(self, level=0):
        result = []
        indent = ' ' * (level * 2)
        if self.callback:
            result.append(f'{indent}Callback: Yes')

        for key, child in self.children.items():
            result.append(f'{indent}{key}:')
            result.append(child.__str__(level + 1))

        return '\n'.join(result)


class URLRouter:
    def __init__(self):
        self.routes = {}

    def add_route(
        self,
        method: str,
        plugin_name: str,
        pattern: str,
        callback: CallbackFunctionType,
    ):
        parts = pattern.strip('/').split('/')
        node = self.routes.setdefault(method, {}).setdefault(plugin_name, TrieNode())

        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]

        # Replace the existing callback with the new one
        node.callback = callback

    def match(self, method: str, plugin_name: str, url: str):
        parts = url.strip('/').split('/')
        node = self.routes.get(method, {}).get(plugin_name, TrieNode())
        return self._match_parts(node, parts, 0)

    def _match_parts(
        self, node: TrieNode, parts: List[str], index: int
    ) -> Optional[CallbackFunctionType]:
        if index == len(parts):
            return node.callback

        part = parts[index]

        # Check direct match
        if part in node.children:
            result = self._match_parts(node.children[part], parts, index + 1)
            if result:
                return result

        # Check wildcard match
        if '*' in node.children:
            result = self._match_parts(node.children['*'], parts, index + 1)
            if result:
                return result

        # Check double wildcard match
        if '**' in node.children:
            return node.children['**'].callback

        return None

    def __str__(self):
        result = []
        for method, plugin_dict in self.routes.items():
            result.append(f'Method: {method}')
            for plugin_name, node in plugin_dict.items():
                result.append(f'  Plugin: {plugin_name}')
                result.append(node.__str__(2))
        return '\n'.join(result)


_ROUTER = URLRouter()


def subscribe_get(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, 'GET', callback)


def subscribe_put(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, 'PUT', callback)


def subscribe_post(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, 'POST', callback)


def subscribe_delete(endpoint: str, callback: Callable[[str, Request], Any]) -> None:
    _subscribe(endpoint, 'DELETE', callback)


def subscribe_websocket(
    endpoint: str, callback: Callable[[str, WebSocket], Any]
) -> None:
    _subscribe(endpoint, 'WEBSOCKET', callback)


def _subscribe(endpoint: str, method: str, callback: CallbackFunctionType) -> None:
    module_name = stack.get_caller(depth=3)[0]
    if not module_name.startswith('plugins.plugins.'):
        return

    plugin_name = module_name.split('.')[2]
    _ROUTER.add_route(method, plugin_name, endpoint, callback)


def fetch_callback(
    plugin: str, url: str, method: str
) -> Optional[CallbackFunctionType]:
    return _ROUTER.match(method.upper(), plugin, url)
