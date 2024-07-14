from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import Request, WebSocket

from utils import stack

CallbackFunctionType = Callable[[str, Union[Request, WebSocket]], Any]


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.callback: Optional[CallbackFunctionType] = None

    def __str__(self, level=0) -> str:
        result = []
        indent = ' ' * (level * 2)
        if self.callback:
            result.append(f'{indent}Callback: Yes')

        for key, child in self.children.items():
            result.append(f'{indent}{key}:')
            result.append(child.__str__(level + 1))

        return '\n'.join(result)


class URLRouter:
    def __init__(self) -> None:
        self.routes: Dict[str, Dict[str, TrieNode]] = {}

    def add_route(
        self,
        method: str,
        plugin_name: str,
        pattern: str,
        callback: CallbackFunctionType,
    ) -> None:
        parts = pattern.strip('/').split('/')
        node = self.routes.setdefault(
            method, {}).setdefault(plugin_name, TrieNode())

        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]

        # Replace the existing callback with the new one
        node.callback = callback

    def remove_route(self, method: str, plugin_name: str, pattern: str) -> bool:
        parts = pattern.strip('/').split('/')
        node = self.routes.get(method, {}).get(plugin_name)

        if not node:
            return False

        return self._remove_parts(node, parts, 0)

    def _remove_parts(self, node: TrieNode, parts: List[str], index: int) -> bool:
        if index == len(parts):
            if node.callback:
                node.callback = None
                return len(node.children) == 0
            return False

        part = parts[index]
        if part in node.children:
            should_delete_child = self._remove_parts(
                node.children[part], parts, index + 1)
            if should_delete_child:
                del node.children[part]
                return len(node.children) == 0 and node.callback is None
        return False

    def remove_plugin(self, plugin_name: str) -> None:
        self.routes = {method: {pn: pd for pn, pd in plugin_dict.items() if pn != plugin_name}
                       for method, plugin_dict in self.routes.items()
                       if any(pn != plugin_name for pn in plugin_dict)}

    def match(self, method: str, plugin_name: str, url: str) -> Optional[CallbackFunctionType]:
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

    def __str__(self) -> str:
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


def unsubscribe(endpoint: str, method: str) -> bool:
    module_name = stack.get_caller(depth=2)[0]
    if not module_name.startswith('plugins.plugins.'):
        return False
    return _ROUTER.remove_route(method, module_name.split('.')[2], endpoint)


# Do not allow plugins to use this
def unload_plugin(name: str) -> None:
    if stack.get_caller(depth=2)[0].startswith('plugins.plugins.'):
        return
    _ROUTER.remove_plugin(name)
