"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.

"""

from spawn.eigr.functions.actors.api.actor import Actor as ActorEntity

from spawn.eigr.functions.protocol.actors.actor_pb2 import (
    Actor,
    ActorId,
    ActorState,
    Metadata,
    ActorSettings,
    Action,
    FixedTimerAction,
    ActorSnapshotStrategy,
    ActorDeactivationStrategy,
    ActorSystem,
    Kind,
    Registry,
    TimeoutStrategy,
)

from spawn.eigr.functions.protocol.actors.protocol_pb2 import (
    RegistrationRequest,
    RegistrationResponse,
    ServiceInfo,
)


import logging
import platform
import requests

from typing import Any, List

_DEFAULT_HEADERS = {
    "Accept": "application/octet-stream",
    "Content-Type": "application/octet-stream",
}

_REGISTER_URI = "/api/v1/system"


class ActorController:
    _instance = None

    def __init__(self, host: str, port: str, actors: List[ActorEntity]):
        self.host = host
        self.port = port
        self.actors = actors

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def register(self):
        logging.info("Registering Actors on the Proxy %s", self.actors)
        try:

            proxy_url = "http://{}:{}{}".format(self.host,
                                                self.port, _REGISTER_URI)

            # Create actor params via ActorEntity
            deactivate_timeout_strategy = TimeoutStrategy()
            deactivate_timeout_strategy.timeout = 10000

            snaphot_timeout_strategy = TimeoutStrategy()
            snaphot_timeout_strategy.timeout = 120000

            actor_state = ActorState()

            deactivate_strategy = ActorDeactivationStrategy()
            deactivate_strategy.timeout.CopyFrom(deactivate_timeout_strategy)

            snaphot_strategy = ActorSnapshotStrategy()
            snaphot_strategy.timeout.CopyFrom(snaphot_timeout_strategy)

            actor_01 = Actor()

            actor_id = ActorId()
            actor_id.name = "user_actor_01"
            actor_id.system = "spawn-system"

            actor_01.id.CopyFrom(actor_id)

            actor_01.state.CopyFrom(actor_state)

            actor_metatdata = Metadata()
            actor_metatdata.channel_group = "spawn-python"
            actor_metatdata.tags["actor"] = "user_actor_01"

            actor_01.metadata.CopyFrom(actor_metatdata)

            actor_settings = ActorSettings()
            actor_settings.kind = Kind.UNAMED
            actor_settings.stateful = True
            actor_settings.snapshot_strategy.CopyFrom(snaphot_strategy)
            actor_settings.deactivation_strategy.CopyFrom(deactivate_strategy)

            actor_01.settings.CopyFrom(actor_settings)

            actor_action = actor_01.actions.add()
            actor_action.name = ""

            actor_fixed_timer_action = actor_01.timer_actions.add()

            actor_fixed_timer_action.seconds = 1
            actor_fixed_timer_action.action.CopyFrom(actor_action)

            registry = Registry()
            registry.actors.get_or_create("user_actor_01").CopyFrom(actor_01)

            actor_system = ActorSystem()
            actor_system.name = "spawn-system"
            actor_system.registry.CopyFrom(registry)

            service_info = ServiceInfo()
            service_info.service_name = "spawn-python-sdk"
            service_info.service_version = "0.1.0"
            service_info.service_runtime = (
                "Python "
                + platform.python_version()
                + " ["
                + platform.python_implementation()
                + " "
                + platform.python_compiler()
                + "]"
            )

            service_info.support_library_name = "spawn-python-sdk"
            service_info.support_library_version = "0.1.0"
            service_info.protocol_major_version = 1
            service_info.protocol_minor_version = 1

            response = RegistrationRequest()
            response.service_info.CopyFrom(service_info)
            response.actor_system.CopyFrom(actor_system)

            binary_payload = response.SerializeToString()

            resp = requests.post(
                proxy_url, data=binary_payload, headers=_DEFAULT_HEADERS
            )

            logging.info("Actors register response %s", resp)
        except Exception as e:
            logging.error("ERROR: %s", e)
            logging.error("Shit %s", e.__cause__)
