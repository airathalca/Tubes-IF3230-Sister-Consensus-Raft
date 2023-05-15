from threading import Lock
from typing import Callable, Optional
from rpyc.utils.server import ThreadedServer
from . import ServerConfig, ServerService, Script


class ServerMeta(type):
    __instances = {}
    __lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
        return cls.__instances[cls]


class Server(metaclass=ServerMeta):
    # Utility
    __config = ServerConfig()
    __script = Script()

    # State
    __server = ThreadedServer(
        ServerService,
        port=__config.get("SERVER_ADDRESS").port,
    )

    def start(self, function: Optional[Callable[[], None]] = None) -> None:
        # Execute function if exists
        if function != None:
            function()

        # Start sequence
        self.__script.start()

        # Start service
        self.__server.start()

    def stop(self, function: Optional[Callable[[], None]] = None) -> None:
        # Execute function if exists
        if function != None:
            function()

        # Stop service
        self.__server.close()

        # Stop sequence
        self.__script.stop()