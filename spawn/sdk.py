"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Flask

from dataclasses import (dataclass, field)

from handler import action_handler
from internal.controller import SpawnActorController as ActorController

from typing import List, Callable, Any, Mapping, MutableMapping
import inspect

import os
import logging


@dataclass
class ActorEntity:

    def command(self, name: str):
        def register_command_handler(function):
            """
            Register the function to handle commands
            """
            # if name in self.command_handlers:
            #    raise Exception("Command handler function {} already defined for command {}".format(
            #        self.command_handlers[name], name))
            # if function.__code__.co_argcount > 3:
            #    raise Exception(
            #        "At most three parameters, the current state, the command and the context, should be accepted by the command_handler function")
            #self.command_handlers[name] = function
            return function

        return register_command_handler


@dataclass
class Spawn:
    actorController = ActorController(
        os.environ.get('PROXY_HOST', 'localhost'),
        os.environ.get('PROXY_PORT', '9001'),
    )

    logging.basicConfig(
        format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s', level=logging.INFO)
    logging.root.setLevel(logging.NOTSET)

    __host = '127.0.0.1'
    __port = '8090'
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
        address = '{}:{}'.format(os.environ.get(
            'HOST', self.__host), os.environ.get('PORT', self.__port))

        logging.info('Starting Spawn on address %s', address)
        try:
            app = Flask(__name__)
            app.register_blueprint(action_handler)
            app.run(host=self.__host, port=self.__port, threaded = True, debug=True)

            # Invoke proxy for register ActorsEntity using Spawn protobuf types
            self.__register(self.__actors)
        except IOError as e:
            logging.error('Error on start Spawn %s', e.__cause__)

    def __register(self, actors: List[ActorEntity]):
        self.actorController.register(actors)
