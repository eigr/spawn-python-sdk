from enum import Enum
from typing import Generic, MutableMapping, TypeVar

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
            metadata: MutableMapping[str, str] = dict(),
            tags: MutableMapping[str, str] = dict(),
            deactivate_timeout: int = 30000,
            snapshot_timeout: int = 2000):
        self.name = name
        self.kind = kind
        self.stateful = stateful
        self.state_type = state_type
        self.channel = channel
        self.tags = tags
        self.deactivate_timeout = deactivate_timeout
        self.snapshot_timeout = snapshot_timeout
