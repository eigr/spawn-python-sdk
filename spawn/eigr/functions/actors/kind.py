from enum import Enum


class Kind(str, Enum):
    NAMED = 'NAMED'
    UNNAMED = 'UNNAMED'
    POOLED = 'POOLED'
