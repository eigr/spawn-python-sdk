"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import ActorEntity, ActorInit, ActorParams

from eigr.state.joe_pb2 import JoeState
from eigr.messages.messages_pb2 import Request
from eigr.messages.messages_pb2 import Reply

from dataclasses import dataclass


@dataclass
class JoeActor(ActorInit):

    def init() -> ActorParams:
        return ActorParams(
            name='joe',
            state_type=JoeState,
            snapshot_timeout=10000,
            deactivate_timeout=30000
        )

    entity = ActorEntity(init)

    @entity.command()
    def get_actual_state():
        return ""

    @entity.command()
    def set_language(self, req: Request):
        return ""
