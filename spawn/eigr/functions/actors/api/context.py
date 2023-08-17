from dataclasses import dataclass
from typing import Dict


@dataclass
class Context:
    state: object
    caller: str = None
    metadata: Dict[str, str] = None
    tags: Dict[str, str] = None
