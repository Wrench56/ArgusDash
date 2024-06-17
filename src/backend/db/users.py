from typing import Dict, Optional

import datetime
import logging
from utils import config
import uuid

class User:
    def __init__(self, username: str, password: str) -> None:
        self._username: str = username
        self._password_hash: str = password
        self._uuid: Optional[str] = None
        self._expire_time = None

    def generate_uuid(self) -> str:
        self._uuid = uuid.uuid4().hex
        self._generate_expire_time()
        return self._uuid

    def _generate_expire_time(self):
        expire_time = float(config.get('security').get('auth_cookie_expire_time') or 3600.0)
        self._expire_time = datetime.datetime.now() + datetime.timedelta(seconds=expire_time)

    def uuid_has_expired(self) -> bool:
        if self._expire_time is None:
            return True
        return datetime.datetime.now() > self._expire_time

    def has_uuid(self) -> bool:
        return self._uuid is None

    def valid_password(self, password: str) -> bool:
        return self._password_hash == password


# Temporary solution
class Database:
    VALID_AUTHS: Dict[str, User] = {
        'admin': User('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
    }

    def __init__(self) -> None:
        self._valid_uuids: Dict[str, User] = {}

    def is_valid(self, username, password) -> bool:
        user = self.VALID_AUTHS.get(username)
        if user is None:
            return False
        return user.valid_password(password)

    def uuid_exists(self, uuid_: str) -> bool:
        user = self._valid_uuids.get(uuid_)
        if user is None:
            return False
        if user.uuid_has_expired():
            del self._valid_uuids[uuid_]
            return False
        return True

    def create_uuid(self, username: str) -> str:
        user = self.VALID_AUTHS.get(username)
        if user is None:
            logging.error(f'"{username}" is not a valid username')
            return 'INVALID'
        if user.has_uuid():
            logging.error(f'User "{username}" already has a UUID')

        uuid_ = user.generate_uuid()
        self._valid_uuids[uuid_] = user
        return uuid_

    def active_users(self) -> int:
        return len(self._valid_uuids)
