"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from domain.domain_pb2 import State, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast

actor = Actor(settings=ActorSettings(
    name="joe", stateful=True, channel="test"))


@actor.timer_action(every=1000)
def hi(ctx: Context) -> Value:
    new_state = None
    request = Request()
    request.language = "python"
    broadcast = Broadcast()
    broadcast.channel = "test"
    broadcast.action_name = "setLanguage"
    broadcast.value = request

    if not ctx.state:
        new_state = State()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value()\
        .broadcast(broadcast)\
        .state(new_state)\
        .noreply()


@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    print("Request -> " + str(request))
    print("Current State -> " + str(ctx.state))

    reply = Reply()
    reply.response = "erlang"
    new_state = State()
    new_state.languages.append("erlang")
    return Value().response(reply).state(new_state).reply()
