from dataclasses import dataclass, field
from typing import MutableMapping


@dataclass
class Context:
    state: object
    caller: str = None
    metadata: MutableMapping[str, str] = field(default_factory=dict)
    tags: MutableMapping[str, str] = field(default_factory=dict)
