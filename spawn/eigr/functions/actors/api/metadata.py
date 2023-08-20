
from dataclasses import dataclass, field
from typing import MutableMapping


@dataclass
class Metadata:
    __map: MutableMapping[str, str] = field(default_factory=dict)
    __tags: MutableMapping[str, str] = field(default_factory=dict)

    def put_metadata(self, key: str, value: str):
        self.__map[key] = value

    def put_tag(self, key: str, value: str):
        self.__tags[key] = value

    def get_metadata(self):
        return self.__map

    def get_tags(self):
        return self.__tags
