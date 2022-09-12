"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import Spawn
from actor import entity as actor_entity


if __name__ == '__main__':
    Spawn()\
        .port('8080')\
        .register_actor(actor_entity)\
        .start()