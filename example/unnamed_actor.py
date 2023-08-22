"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from domain.domain_pb2 import State, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings, Kind
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value

abstract = Actor(settings=ActorSettings(
    name="abs_actor", stateful=True, kind=Kind.UNNAMED))


@abstract.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    print("Current State -> " + str(ctx.state))

    reply = Reply()
    reply.response = "erlang"
    new_state = State()
    new_state.languages.append("python")
    return Value().of(reply, new_state).reply()
