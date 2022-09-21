"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Flask

from dataclasses import dataclass, field

from spawn.entity import ActorEntity
from spawn.handler import action_handler
from spawn.controller import SpawnActorController as ActorController

from typing import List, Callable, Any, Mapping, MutableMapping
import inspect

import json
import os
import logging
import time
import threading


@dataclass
class Spawn:
    logging.basicConfig(
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
        level=logging.INFO,
    )
    logging.root.setLevel(logging.NOTSET)

    __host = os.environ.get("HOST", "0.0.0.0")
    __port = os.environ.get("PORT", "8091")
    __actors: List[ActorEntity] = field(default_factory=list)
    __app = Flask(__name__)
    __is_debug_enable = json.loads(os.environ.get("SDK_DEBUG_ENABLE", "false").lower())
    __actorController = ActorController(
        os.environ.get("PROXY_HOST", "localhost"),
        os.environ.get("PROXY_PORT", "9002"),
    )

    @staticmethod
    def invoke(name: str, command: str, arg: Any, output_type: Any) -> Any:
        actorController = ActorController(
            os.environ.get("PROXY_HOST", "localhost"),
            os.environ.get("PROXY_PORT", "9002"),
        )
        actorController.invoke(name, command, arg, output_type)

    def host(self, address: str):
        """Set the Network Host address."""
        self.__host = address
        return self

    def port(self, port: str):
        """Set the Network Port address."""
        self.__port = port
        return self

    def register_actor(self, entity: ActorEntity):
        """Registry the user Actor entity."""
        self.__actors.append(entity)
        return self

    def start(self):
        """Start the user function and HTTP Server."""
        address = "{}:{}".format(self.__host, self.__port)

        server = threading.Thread(target=lambda: self.__start_server(action_handler))
        logging.info("Starting Spawn on address %s", address)
        try:
            server.start()

            # Invoke proxy for register ActorsEntity using Spawn protobuf types
            self.__register(self.__actors)
        except IOError as e:
            logging.error("Error on start Spawn %s", e.__cause__)

    def __register(self, actors: List[ActorEntity]):
        self.__actorController.register(actors)

    def __start_server(self, handler):
        self.__app.register_blueprint(handler, url_prefix="/api/v1")
        self.__app.run(
            host=self.__host,
            port=self.__port,
            use_reloader=False,
            debug=self.__is_debug_enable,
        )
