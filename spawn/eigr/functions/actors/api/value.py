# pylint: disable=too-few-public-methods
# pylint: disable=arguments-differ
from abc import ABCMeta, abstractmethod

from spawn.eigr.functions.actors.api.metadata import Metadata
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast
from spawn.eigr.functions.actors.api.workflows.effect import Effect
from spawn.eigr.functions.actors.api.workflows.forward import Forward
from spawn.eigr.functions.actors.api.workflows.pipe import Pipe


class IValue(metaclass=ABCMeta):
    "The Builder Interface"

    @staticmethod
    @abstractmethod
    def of(response, state=None):
        "Build value from response and state"

    @staticmethod
    @abstractmethod
    def state(state):
        "Build value only from state"

    @staticmethod
    @abstractmethod
    def metadata(metadata: Metadata):
        "Build value with metadata"

    @staticmethod
    @abstractmethod
    def value(response):
        "Build value from response"

    @staticmethod
    @abstractmethod
    def broadcast(broadcast: Broadcast):
        "Create Broadcast"

    @staticmethod
    @abstractmethod
    def effect(effect: Effect):
        "Create Effect"

    @staticmethod
    @abstractmethod
    def forward(forward: Forward):
        "Create Forward"

    @staticmethod
    @abstractmethod
    def pipe(pipe: Pipe):
        "Create Pipe"

    @staticmethod
    @abstractmethod
    def reply():
        "Create Value response"


class Value(IValue):
    "The Concrete Builder."

    def __init__(self):
        pass

    def of(response, state=None):
        pass

    def state(state):
        pass

    def metadata(metadata: Metadata):
        pass

    def value(response):
        pass

    def broadcast(broadcast: Broadcast):
        pass

    def effect(effect: Effect):
        pass

    def forward(forward: Forward):
        pass

    def pipe(pipe: Pipe):
        pass

    def reply():
        pass
