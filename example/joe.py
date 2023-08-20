"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from domain.domain_pb2 import JoeState, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.metadata import Metadata
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast
from spawn.eigr.functions.actors.api.workflows.effect import Effect

actor = Actor(settings=ActorSettings(name="joe", stateful=True))


@actor.timer_action(every=1000)
def hi(ctx: Context) -> Value:
    new_state = None
    if not ctx.state:
        new_state = JoeState()
        new_state.languages.append("portuguese")
    else:
        new_state = ctx.state

    return Value()\
        .of("test")\
        .state(new_state)\
        .reply()


@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    return Value()\
        .of("test")\
        .broadcast(Broadcast())\
        .effect(Effect())\
        .metada(Metadata())\
        .state({})\
        .reply()
