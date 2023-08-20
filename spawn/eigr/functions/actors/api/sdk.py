"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Flask, request, send_file

from dataclasses import dataclass, field
from typing import MutableMapping

from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.internal.controller import ActorController

from google.protobuf.any_pb2 import Any as ProtoAny

import io
import os
import logging
import uvicorn
import threading


def create_app(controller: ActorController):
    app = Flask(__name__)

    @app.route('/api/v1/actors/actions', methods=["POST"])
    def action():
        data = request.data

        actor_invocation_response = controller.handle_invoke(data)

        return send_file(
            io.BytesIO(actor_invocation_response.SerializeToString()),
            mimetype='application/octet-stream'
        )

    return app


@dataclass
class Spawn:
    logging.basicConfig(
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
        level=logging.INFO,
    )
    logging.root.setLevel(logging.NOTSET)

    __app = None
    __controller = None
    __host = os.environ.get("USER_FUNCTION_HOST", "0.0.0.0")
    __port = os.environ.get("USER_FUNCTION_PORT", "8091")
    __proxy_host = os.environ.get("PROXY_HTTP_HOST", "0.0.0.0")
    __proxy_port = os.environ.get("PROXY_HTTP_PORT", "9001")
    __system: str = None
    __actor_entities: MutableMapping[str,
                                     Actor] = field(default_factory=dict)

    # @staticmethod
    # def invoke(name: str, command: str, arg: Any, output_type: Any) -> Any:
    #     actorController = ActorController(
    #         os.environ.get("PROXY_HOST", "localhost"),
    #         os.environ.get("PROXY_PORT", "9002"),
    #     )
    #     actorController.invoke(name, command, arg, output_type)

    def host(self, address: str):
        """Set the Network Host address."""
        self.__host = address
        return self

    def port(self, port: int):
        """Set the Network Port address."""
        self.__port = port
        return self

    def proxy_host(self, host: str):
        """Set the Spawn Proxy Host Address"""
        self.__proxy_host = host
        return self

    def proxy_port(self, port: int):
        self.__proxy_port = str(port)
        return self

    def actor_system(self, system: str = None):
        """Set the ActorSystem"""
        self.__system = system
        return self

    def add_actor(self, actor: Actor):
        """Registry the user Actor entity."""
        self.__actor_entities[actor.settings.name] = actor
        return self

    def start(self):
        """Start the user function and HTTP Server."""
        if not self.__system:
            raise Exception(
                "ActorSystem cannot be None. Use actor_system function to set an ActorSystem")

        address = "{}:{}".format(self.__host, self.__port)
        self.__controller = ActorController(
            self.__proxy_host, self.__proxy_port, self.__system, self.__actor_entities)

        self.__app = create_app(controller=self.__controller)

        server = threading.Thread(
            target=lambda: self.__start_server())
        client = threading.Thread(
            target=lambda: self.__register())
        logging.info("Starting Spawn on address %s", address)
        try:
            server.start()
            client.start()
            server.join()
            client.join()
        except IOError as e:
            logging.error("Error on start Spawn %s", e.__cause__)

    def __register(self):
        self.__controller.register()

    def __start_server(self):

        # uvicorn.run(self.__app, host=self.__host, port=self.__port)
        self.__app.run(
            host=self.__host,
            port=self.__port,
            use_reloader=False
        )
