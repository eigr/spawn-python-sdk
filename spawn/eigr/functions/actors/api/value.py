# pylint: disable=too-few-public-methods
# pylint: disable=arguments-differ
from dataclasses import dataclass
from enum import Enum

from spawn.eigr.functions.actors.api.metadata import Metadata
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast
from spawn.eigr.functions.actors.api.workflows.effect import Effect
from spawn.eigr.functions.actors.api.workflows.forward import Forward
from spawn.eigr.functions.actors.api.workflows.pipe import Pipe


class ReplyKind(str, Enum):
    REPLY = 'REPLY'
    NO_REPLY = 'NO_REPLY'


@dataclass
class Value():
    "The Concrete Builder."
    __state = None
    __response = None
    __metadata: Metadata = None
    __broadcast: Broadcast = None
    __effect: Effect = None
    __forward: Forward = None
    __pipe: Pipe = None
    __reply_kind: ReplyKind = ReplyKind.REPLY

    def get_state(self):
        return self.__state

    def get_response(self):
        return self.__response

    def get_metadata(self):
        return self.__metadata

    def get_broadcast(self):
        return self.__broadcast

    def get_broadcast(self):
        return self.__broadcast

    def get_effect(self):
        return self.__effect

    def get_forward(self):
        return self.__forward

    def get_pipe(self):
        return self.__pipe

    def get_reply_kind(self):
        return self.__reply_kind

    def of(self, value, state=None):
        self.__response = value
        self.__state = state
        return self

    def state(self, state):
        self.__state = state
        return self

    def metadata(self, metadata: Metadata):
        self.__metadata = metadata
        return self

    def value(self, value):
        self.__response = value
        return self

    def broadcast(self, broadcast: Broadcast):
        self.__broadcast = broadcast
        return self

    def effect(self, effect: Effect):
        self.__effect = effect
        return self

    def forward(self, forward: Forward):
        self.__forward = forward
        return self

    def pipe(self, pipe: Pipe):
        self.__pipe = pipe
        return self

    def reply(self):
        self.__reply_kind = ReplyKind.REPLY
        return self

    def noreply(self):
        self.__reply_kind = ReplyKind.NO_REPLY
        return self
