"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Flask, request, send_file

from dataclasses import dataclass, field
from typing import List

from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.internal.controller import ActorController

from spawn.eigr.functions.protocol.actors.protocol_pb2 import ActorInvocation, ActorInvocationResponse, Context
from google.protobuf.any_pb2 import Any as ProtoAny

import io
import os
import logging
import threading


def create_app(controller: ActorController):
    app = Flask(__name__)

    @app.route('/api/v1/actors/actions', methods=["POST"])
    def action():
        data = request.data
        logging.info('Received Actor action request: %s', data)

        # Decode request payload data here and call python real actors methods.
        databytes = bytes(data)
        actor_invocation = ActorInvocation()
        actor_invocation.ParseFromString(databytes)
        logging.debug('Actor invocation data: %s', actor_invocation)

        # Update Context
        updated_context = Context()

        # Then send ActorInvocationResponse back to the caller
        actor_invocation_response = ActorInvocationResponse()
        actor_invocation_response.actor_name = actor_invocation.actor_name
        actor_invocation_response.actor_system = actor_invocation.actor_system
        actor_invocation_response.updated_context.CopyFrom(updated_context)

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
    __host = os.environ.get("HOST", "0.0.0.0")
    __port = os.environ.get("PORT", "8091")
    __actor_entities: List[Actor] = field(default_factory=list)

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

    def port(self, port: str):
        """Set the Network Port address."""
        self.__port = port
        return self

    def register_actor(self, actor: Actor):
        """Registry the user Actor entity."""
        self.__actor_entities.append(actor)
        return self

    def start(self):
        """Start the user function and HTTP Server."""
        address = "{}:{}".format(self.__host, self.__port)
        self.__controller = ActorController(
            self.__host, self.__port, self.__actor_entities)

        self.__app = create_app(controller=self.__controller)

        server = threading.Thread(
            target=lambda: self.__start_server())
        logging.info("Starting Spawn on address %s", address)
        try:
            server.start()

            # Invoke proxy for register ActorsEntity using Spawn protobuf types
            self.__register()
        except IOError as e:
            logging.error("Error on start Spawn %s", e.__cause__)

    def __register(self):
        self.__controller.register()

    def __start_server(self):
        self.__app.run(
            host=self.__host,
            port=self.__port,
            use_reloader=False
        )
