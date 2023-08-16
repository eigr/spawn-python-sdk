import dataclasses
from typing import Dict, List

from spawn.eigr.functions.actors.settings import ActorSettings


class ActionInfo:
    def __init__(self, name, input=None, output=None):
        self.name = name
        self.input = input
        self.output = output


@dataclasses
class ActorInfo:
    settings: ActorSettings = None
    actions: List[ActionInfo] = None


@dataclasses
class Actors:
    actors = Dict[str, ActorInfo]


class Context:
    pass


class Actor:

    def __init__(self, settings: ActorSettings):
        actor_info = ActorInfo(settings=settings)
        Actors.actors.update(self.__module__, actor_info)
