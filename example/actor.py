"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import ActorEntity, ActorInit, ActorParams
from dataclasses import dataclass, field


@dataclass
class JoeActor(ActorInit):

    def init() -> ActorParams:
        return ActorParams('joe', "", 10000, 30000)

    entity = ActorEntity(init)

    @entity.command()
    def get():
        return ""
