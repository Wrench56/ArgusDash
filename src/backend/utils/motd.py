import psutil
import re

from db import users


_ALLOWED_COLORS = (
    'aqua',
    'black',
    'blue',
    'fuchsia',
    'gray',
    'green',
    'lime',
    'maroon',
    'navy',
    'olive',
    'purple',
    'red',
    'silver',
    'teal',
    'white',
    'yellow',
)


def format_(raw: str, database: users.Database) -> str:
    return _format_color(_format_data(_format_breaks(raw), database))


def _format_breaks(raw: str) -> str:
    return raw.replace('\\n', '\n')


def _format_data(raw: str, database: users.Database) -> str:
    return (
        raw.replace('{{memory_used}}', str(_b2mb(psutil.virtual_memory().used)))
        .replace('{{memory_total}}', str(_b2mb(psutil.virtual_memory().total)))
        .replace('{{memory_percent}}', str(psutil.virtual_memory().percent))
        .replace('{{cpu_percent}}', str(psutil.cpu_percent()))
        .replace('{{active_users}}', str(database.active_users()))
    )


def _format_color(raw: str) -> str:
    pattern = re.compile(r'{{(.*?)}}(.*?){{end}}')

    def replace_match(match):
        color = match.group(1).lower()
        if color not in _ALLOWED_COLORS:
            # Return original
            return match.group(0)
        content = match.group(2)
        return f'<span style="color:{color};">{content}</span>'

    return pattern.sub(replace_match, raw)


def _b2mb(byte: int) -> int:
    return round(byte / 1_048_576)
