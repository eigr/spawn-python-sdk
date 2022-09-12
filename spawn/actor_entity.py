"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import List, Callable, Any, Mapping, MutableMapping
import inspect


@dataclass
class ActorEntity:

    def command_handler(self, name: str):
        def register_command_handler(function):
            """
            Register the function to handle commands
            """
            if name in self.command_handlers:
                raise Exception("Command handler function {} already defined for command {}".format(
                    self.command_handlers[name], name))
            if function.__code__.co_argcount > 3:
                raise Exception(
                    "At most three parameters, the current state, the command and the context, should be accepted by the command_handler function")
            self.command_handlers[name] = function
            return function

        return register_command_handler
