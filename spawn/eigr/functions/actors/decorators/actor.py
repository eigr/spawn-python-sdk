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
    name: str = None
    settings: ActorSettings = None
    actions: List[ActionInfo] = None


class Actors:
    _instance = None
    actors = Dict[str, ActorInfo] = None

    def __init__(self):
        if not self.actors:
            self.actors = Dict()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance


class Context:
    pass


class Actor:
    def __init__(self, settings: ActorSettings):
        actor_info = ActorInfo(name=settings.name, settings=settings)
        Actors().actors.update(self.__module__, actor_info)
