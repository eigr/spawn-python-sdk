from entity import ActorEntity
from dataclasses import dataclass


@dataclass
class JoeActorEntity:

    entity = ActorEntity()

    @entity.command()
    def get():
        return ""
