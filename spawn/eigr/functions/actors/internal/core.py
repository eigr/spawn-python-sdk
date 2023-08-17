from typing import List, MutableMapping

from spawn.eigr.functions.actors.api.settings import ActorSettings


class ActionInfo:
    def __init__(self, name, input=None, output=None):
        self.name = name
        self.input = input
        self.output = output


class ActorInfo:
    def __init__(self, name: str, settings: ActorSettings, actions: List[ActionInfo] = None) -> None:
        self.name = name
        self.settings = settings
        self.actions = actions


class Actors:
    _instance = None
    actors = MutableMapping[str, ActorInfo]

    def __init__(self):
        if not self.actors:
            self.actors = {}

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance
