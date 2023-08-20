"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.eigr.functions.actors.api.sdk import Spawn
from example.joe import actor as joe_actor
from example.domain.domain_pb2 import Reply, Request

if __name__ == "__main__":
    request = Request()
    request.language = "erlang"

    spawn = Spawn()
    spawn.port(8091).proxy_port(9003).actor_system(
        "spawn-system").add_actor(joe_actor).start()
