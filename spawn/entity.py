"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from dataclasses import dataclass, field

from typing import Any, Callable, MutableMapping, TypeVar, Generic

S = TypeVar("S")
V = TypeVar("V")

@dataclass
class ActorContext:
    state: Generic[S]

@dataclass
class Value:
    state: Generic[S]
    value: Generic[V]

@dataclass
class ActorParams:
    name: str
    state_type: Any
    snapshot_timeout: int
    deactivate_timeout: int


class ActorInit:
    def init(self) -> ActorParams:
        pass


@dataclass
class ActorEntity:
    init_state: Callable[[str], Any]
    command_handlers: MutableMapping[str, Callable] = field(default_factory=dict)

    def command(self, name: str):
        def register_command_handler(function):
            """
            Register the function to handle commands
            """
            if name in self.command_handlers:
                raise Exception(
                    "Command handler function {} already defined for command {}".format(
                        self.command_handlers[name], name
                    )
                )

            if function.__code__.co_argcount > 2:
                raise Exception(
                    "At most two parameters, the command and the context, should be accepted by the command function"
                )

            self.command_handlers[name] = function
            return function

        return register_command_handler


@dataclass
class ActorEntityHandler:
    entity: ActorEntity

    def init_actor(self):
        return self.entity.init()