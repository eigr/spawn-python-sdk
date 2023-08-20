
from dataclasses import dataclass


@dataclass
class Broadcast:
    channel: str = None
    action_name: str = None
    value: any = None
