"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from dataclasses import dataclass
from domain.domain_pb2 import JoeState, Request
from spawn.entity import ActorEntity, ActorInit, ActorParams


@dataclass
class JoeActor(ActorInit):

    # TODO: Remove this because it´s a bad design. Correct is extract this to superior Class
    def init() -> ActorParams:
        return ActorParams(
            name='joe',
            state_type=JoeState,
            snapshot_timeout=10000,
            deactivate_timeout=120000
        )

    entity = ActorEntity(init)

    #@entity.command("get_actual_state")
    def get_actual_state():
        return ""

    #@entity.command("set_language")
    def set_language(self, req: Request):
        return ""
