"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from domain.domain_pb2 import Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings, Kind
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value

abstract = Actor(settings=ActorSettings(
    name="abs_actor", stateful=True, kind=Kind.UNNAMED))


@abstract.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    reply = Reply()
    reply.response = "erlang"
    return Value().of(reply, ctx.state).reply()
