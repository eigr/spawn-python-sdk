
from typing import Generic, TypeVar
from spawn.eigr.functions.actors.kind import Kind

T = TypeVar('T')


class ActorSettings:
    def __init__(self, name: str, kind: Kind = Kind.NAMED, stateful: bool = True, state_type: Generic[T] = None, deactivate_timeout: int = 30, snapshot_timeout: int = 10):
        self.name = name
        self.kind = kind
        self.stateful = stateful
        self.state_type = state_type
        self.deactivate_timeout = deactivate_timeout
        self.snapshot_timeout = snapshot_timeout
