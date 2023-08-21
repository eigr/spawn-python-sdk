"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.eigr.functions.actors.api.reference import ActorRef
from spawn.eigr.functions.actors.api.sdk import Spawn
from example.joe import actor as joe_actor
from example.unnamed_actor import abstract
from example.domain.domain_pb2 import Request

if __name__ == "__main__":
    request = Request()
    request.language = "erlang"

    spawn = Spawn()
    spawn.port(8091).proxy_port(9003).actor_system(
        "spawn-system").add_actor(joe_actor).add_actor(abstract).start()

    # Get abstract actor reference called mike
    mike_actor: ActorRef = Spawn.create_actor_ref(
        system="spawn-system",
        actor_name="mike",
        parent="abs_actor",
        state_revision=1
    )

    # mike_actor.invoke(request)
