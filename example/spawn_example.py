"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import Spawn
from example.joe import JoeActor
from example.domain.domain_pb2 import Reply, Request

if __name__ == "__main__":
    request = Request()
    request.language = "erlang"
    # Spawn.invoke("joe", "setLanguage", request, Reply)

    spawn = Spawn()
    spawn.port("8091").register_actor(JoeActor.entity).start()
    spawn.invoke("vijay", "setLanguage", request, Reply)
