from threading import Lock
from typing import Any


class ThreadSafeSingletonMeta(type):
    _instances: dict[type, Any] = {}
    _locks: dict[type, Lock] = {}

    def __call__(cls, *args, **kwargs):
        # Create singleton lock if not exists
        if cls not in cls._locks:
            cls._locks[cls] = Lock()

        # Acquire lock for singleton
        with cls._locks[cls]:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]