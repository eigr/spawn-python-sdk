"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from dataclasses import dataclass
from domain.domain_pb2 import JoeState, Request, Reply
from spawn.entity import ActorContext, ActorEntity, ActorInit, ActorParams, Value


@dataclass
class JoeActor(ActorInit):

    # TODO: Remove this because it´s a bad design. Correct is extract this to superior Class
    def init() -> ActorParams:
        return ActorParams(
            name="joe",
            state_type=JoeState,
            snapshot_timeout=10000,
            deactivate_timeout=120000,
        )

    entity = ActorEntity(init)

    @entity.command("getActualState")
    def get_actual_state(self, ctx: ActorContext) -> Value:
        current_state = ctx.state
        new_value = current_state
        return Value(current_state, new_value)

    @entity.command("setLanguage")
    def set_language(self, ctx: ActorContext) -> Value:
        reply = Reply()
        reply.response = "elf"

        new_state = ctx.state.languages.extend("elf")
        return Value(new_state, reply)