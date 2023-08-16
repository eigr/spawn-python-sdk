import functools
from typing import Dict, List

from spawn.eigr.functions.actors.settings import ActorSettings


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
    actors = Dict[str, ActorInfo]

    def __init__(self):
        if not self.actors:
            self.actors = {}

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance


class Context:
    pass


def Actor(cls):

    @functools.wraps(cls)
    def wrapper_actor(*args, **kwargs):
        wrapper_actor.instance = cls(*args, **kwargs)

        print(type(wrapper_actor.instance).__name__)
        cls_name = type(wrapper_actor.instance).__name__
        settings = kwargs.get('settings')

        actor_info = ActorInfo(name=settings.name, settings=settings)
        Actors().actors.update({cls_name: actor_info})

    return wrapper_actor
