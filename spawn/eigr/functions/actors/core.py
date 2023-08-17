from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generic, List, TypeVar

T = TypeVar('T')


class Kind(str, Enum):
    NAMED = 'NAMED'
    UNNAMED = 'UNNAMED'
    POOLED = 'POOLED'


class ActorSettings:
    def __init__(
            self,
            name: str,
            kind: Kind = Kind.NAMED,
            stateful: bool = True,
            state_type: Generic[T] = None,
            channel: str = None,
            deactivate_timeout: int = 30,
            snapshot_timeout: int = 10):
        self.name = name
        self.kind = kind
        self.stateful = stateful
        self.state_type = state_type
        self.channel = channel
        self.deactivate_timeout = deactivate_timeout
        self.snapshot_timeout = snapshot_timeout


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


@dataclass
class Context:
    state: object
    caller: str = None
    metadata: Dict[str, str] = {}
    tags: Dict[str, str] = {}
