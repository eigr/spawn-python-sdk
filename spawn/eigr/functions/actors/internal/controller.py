"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.

"""

from spawn.eigr.functions.actors.api.actor import Actor as ActorEntity
from spawn.eigr.functions.actors.api.actor import ActorHandler
from spawn.eigr.functions.actors.api.context import Context as ActorContext
from spawn.eigr.functions.actors.api.value import Value, ReplyKind
from spawn.eigr.functions.actors.api.settings import Kind as ActorKind

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
    ActorInvocation,
    ActorInvocationResponse,
    Context,
    Noop,
    RegistrationRequest,
    RegistrationResponse,
    ServiceInfo,
)

from google.protobuf import symbol_database as _symbol_database
from google.protobuf.any_pb2 import Any as AnyProto

import logging
import platform
import requests

from typing import Any, MutableMapping

_sym_db = _symbol_database.Default()

_DEFAULT_HEADERS = {
    "Accept": "application/octet-stream",
    "Content-Type": "application/octet-stream",
}

_REGISTER_URI = "/api/v1/system"

TYPE_URL_PREFIX = 'type.googleapis.com/'


def get_payload(input):
    print(input)
    input_type: str = input.type_url
    if input_type.startswith(TYPE_URL_PREFIX):
        input_type = input_type[len(TYPE_URL_PREFIX):]
    input_class = _sym_db.GetSymbol(input_type)
    result = input_class()
    result.ParseFromString(input.value)
    return result


def pack(input):
    any = AnyProto()
    any.Pack(input)
    return any


def handle_response(system, actor_name, result):
    print("Result ----- {}".format(result))
    actor_invocation_response = ActorInvocationResponse()
    actor_invocation_response.actor_name = actor_name
    actor_invocation_response.actor_system = system

    updated_context = Context()

    if result.get_metadata() != None and len(result.get_metadata().get_metadata()) > 0:
        print("Metadata -----------".format(result.metadata))
        updated_context.metadata = result.get_metadata.get_metadata()

    if result.get_metadata() != None and len(result.get_metadata().get_tags()) > 0:
        updated_context.tags = result.get_metadata().get_tags()

    updated_context.state.CopyFrom(pack(result.get_state()))

    actor_invocation_response.updated_context.CopyFrom(updated_context)

    if result.get_reply_kind() == ReplyKind.NO_REPLY:
        actor_invocation_response.noop = Noop()
    elif result.get_reply_kind == ReplyKind.REPLY:
        actor_invocation_response.value = pack(result.get_response())

    return actor_invocation_response


class ActorController:
    _instance = None

    def __init__(self, host: str, port: str, system: str, actors: MutableMapping[str, ActorEntity]):
        self.host = host
        self.port = port
        self.system = system
        self.actors = actors

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def handle_invoke(self, data) -> ActorInvocationResponse:
        # Decode request payload data here and call python real actors methods.
        databytes = bytes(data)
        actor_invocation = ActorInvocation()
        actor_invocation.ParseFromString(databytes)
        logging.debug('Actor invocation data: %s', actor_invocation)
        actor_id = actor_invocation.actor
        actor_system = actor_id.system
        actor_name = actor_id.name
        actor_parent = actor_id.parent

        if actor_system != self.system:
            raise Exception("Invalid call this Actor from ActorSystem {} does not belong to current ActorSystem {}".format(
                actor_system, self.system))

        entity = self.actors[actor_name] if not actor_parent else self.actors[actor_parent]

        handler = ActorHandler(entity)
        current_context = actor_invocation.current_context

        state = None if current_context.state == None else get_payload(
            current_context.state)

        input = None if actor_invocation.WhichOneof(
            "payload") == "noop" else get_payload(actor_invocation.value)

        ctx = ActorContext(state=state, caller=actor_invocation.caller.name,
                           metadata=current_context.metadata, tags=current_context.tags)

        result = handler.handle_action(
            action_name=actor_invocation.action_name, input=input, ctx=ctx)

        if not isinstance(result, Value):
            raise Exception(
                "Action did not return a valid type in its response. Valid Value found {}".format(type(result)))

        # Handle result value
        return handle_response(actor_system, actor_name, result)

    def register(self):
        logging.info("Registering Actors on the Proxy %s", self.actors)
        try:

            proxy_url = "http://{}:{}{}".format(self.host,
                                                self.port, _REGISTER_URI)

            registry = Registry()
            actor_system = ActorSystem()
            actor_system.name = self.system

            for actor_name, entity in self.actors.items():
                logging.info("Registering Actor %s with Config %s",
                             actor_name, entity)

                # Create actor params via ActorEntity
                actor_template = Actor()

                actor_id = ActorId()
                actor_id.name = actor_name
                actor_id.system = self.system
                actor_template.id.CopyFrom(actor_id)

                actor_state = ActorState()
                actor_template.state.CopyFrom(actor_state)

                deactivate_timeout_strategy = TimeoutStrategy()
                deactivate_timeout_strategy.timeout = entity.settings.deactivate_timeout

                snaphot_timeout_strategy = TimeoutStrategy()
                snaphot_timeout_strategy.timeout = entity.settings.snapshot_timeout

                deactivate_strategy = ActorDeactivationStrategy()
                deactivate_strategy.timeout.CopyFrom(
                    deactivate_timeout_strategy)

                snaphot_strategy = ActorSnapshotStrategy()
                snaphot_strategy.timeout.CopyFrom(snaphot_timeout_strategy)

                actor_settings = ActorSettings()
                actor_settings.snapshot_strategy.CopyFrom(snaphot_strategy)
                actor_settings.deactivation_strategy.CopyFrom(
                    deactivate_strategy)

                # Set metadata
                actor_metatdata = Metadata()

                if (entity.settings.channel is not None and len(entity.settings.channel) > 0):
                    actor_metatdata.channel_group = entity.settings.channel

                # actor_metatdata.tags["actor"] = "user_actor_template"

                actor_template.metadata.CopyFrom(actor_metatdata)

                # Set settings
                if entity.settings.kind == ActorKind.NAMED:
                    actor_settings.kind = Kind.NAMED
                elif entity.settings.kind == ActorKind.UNNAMED:
                    actor_settings.kind = Kind.UNAMED
                elif entity.settings.kind == ActorKind.POOLED:
                    actor_settings.kind = Kind.POOLED
                else:
                    actor_settings.kind = Kind.UNKNOW_KIND

                actor_settings.stateful = entity.settings.stateful
                actor_template.settings.CopyFrom(actor_settings)

                # Set actions
                for action_name, action in entity.action_handlers.items():
                    action = Action()
                    action.name = action_name
                    actor_template.actions.append(action)

                for timer_action_name, timer_action in entity.timer_action_handlers.items():
                    action = Action()
                    action.name = timer_action_name

                    fixed_timer = FixedTimerAction()
                    fixed_timer.seconds = timer_action.every
                    fixed_timer.action.CopyFrom(action)

                    actor_template.timer_actions.append(fixed_timer)

                registry.actors.get_or_create(
                    actor_name).CopyFrom(actor_template)

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

            request = RegistrationRequest()
            request.service_info.CopyFrom(service_info)
            request.actor_system.CopyFrom(actor_system)

            binary_payload = request.SerializeToString()

            resp = requests.post(
                proxy_url, data=binary_payload, headers=_DEFAULT_HEADERS
            )

            logging.info("Actors register response %s", resp)
        except Exception as e:
            logging.error("ERROR: %s", e)
            logging.error("Shit %s", e.__cause__)
