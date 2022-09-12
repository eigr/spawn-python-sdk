"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import ActorEntity
from dataclasses import dataclass


@dataclass
class JoeActorEntity:

    entity = ActorEntity()

    @entity.command()
    def get():
        return ""
