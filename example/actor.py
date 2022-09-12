
from dataclasses import dataclass, field

from entity import ActorEntity


@dataclass
class JoeActorEntity:

    entity = ActorEntity()

    @entity.command()
    def get():
        return ""
