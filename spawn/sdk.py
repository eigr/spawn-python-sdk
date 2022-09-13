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

import os
import logging


@dataclass
class Spawn:
    actorController = ActorController(
        os.environ.get("PROXY_HOST", "localhost"),
        os.environ.get("PROXY_PORT", "9001"),
    )

    logging.basicConfig(
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
        level=logging.INFO,
    )
    logging.root.setLevel(logging.NOTSET)

    __host = "127.0.0.1"
    __port = "8090"
    __actors: List[ActorEntity] = field(default_factory=list)

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
        address = "{}:{}".format(
            os.environ.get("HOST", self.__host), os.environ.get("PORT", self.__port)
        )

        logging.info("Starting Spawn on address %s", address)
        try:
            app = Flask(__name__)
            app.register_blueprint(action_handler)
            app.run(host=self.__host, port=self.__port, threaded=True, debug=True)

            # Invoke proxy for register ActorsEntity using Spawn protobuf types
            self.__register(self.__actors)
        except IOError as e:
            logging.error("Error on start Spawn %s", e.__cause__)

    def __register(self, actors: List[ActorEntity]):
        self.actorController.register(actors)
