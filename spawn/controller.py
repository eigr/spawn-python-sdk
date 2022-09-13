"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.entity import ActorEntity

from . import eigr as protocol_pb2

import logging
import platform
import requests

from typing import List


class SpawnActorController:

    register_uri = '/api/v1/system'

    default_headers = {
        "Accept": "application/octet-stream",
        "Content-Type": "application/octet-stream"
    }

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def register(self, actors: List[ActorEntity]):
        logging.info('Registering Actors on the Proxy %s', actors)
        proxy_url = '{}:{}{}'.format(self.host, self.port, self.register_uri)

        # Create actor params via ActorEntity
        deactivate_timeout_strategy = protocol_pb2.TimeoutStrategy()
        deactivate_timeout_strategy.timeout = 10000

        snaphot_timeout_strategy = protocol_pb2.TimeoutStrategy()
        snaphot_timeout_strategy.timeout = 30000

        actor_state = protocol_pb2.ActorState()

        deactivate_strategy = protocol_pb2.ActorDeactivateStrategy()
        deactivate_strategy.timeout = deactivate_timeout_strategy

        snaphot_strategy = protocol_pb2.ActorSnapshotStrategy()
        snaphot_strategy.timeout = snaphot_timeout_strategy

        actor_01 = protocol_pb2.Actor()
        actor_01.name = "user_actor_01"
        actor_01.persistent = True
        actor_01.state = actor_state
        actor_01.deactivate_strategy = deactivate_strategy
        actor_01.snapshot_strategy = snaphot_strategy

        actors_map = {"user_actor_01": actor_01}

        registry = protocol_pb2.Registry()
        registry.actors = actors_map

        actor_system = protocol_pb2.ActorSystem()
        actor_system.name = 'spawn_sys_test'
        actor_system.registry = registry

        service_info = protocol_pb2.ServiceInfo()
        service_info.service_name = 'spawn-python-sdk'
        service_info.service_version = '0.1.0'
        service_info.service_runtime = 'Python ' + platform.python_version() + \
            ' [' + platform.python_implementation() + ' ' + \
            platform.python_compiler() + ']'

        service_info.support_library_name = 'spawn-python-sdk'
        service_info.support_library_version = '0.1.0'
        service_info.protocol_major_version = 1
        service_info.protocol_minor_version = 1

        response = protocol_pb2.RegistrationRequest()
        response.service_info = service_info
        response.actor_system = actor_system

        binary_payload = response.SerializeToString()

        resp = requests.post(
            proxy_url,
            data=binary_payload,
            headers=self.default_headers
        )

        logging.info('Actors register response %s', resp)
