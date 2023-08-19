
import inspect

from dataclasses import dataclass, field
from typing import Callable, MutableMapping

from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.settings import ActorSettings


@dataclass
class Actor:
    settings: ActorSettings

    action_handlers: MutableMapping[str,
                                    Callable] = field(default_factory=dict)

    def action(self, name: str):
        def register_action_handler(function):
            """
            Register the function to handle actions
            """
            if name in self.action_handlers:
                raise Exception("Action handler function {} already defined for action {}".format(
                    self.action_handlers[name], name))
            if function.__code__.co_argcount > 2:
                raise Exception(
                    "At most two parameters, the input parameter and the context parameter, should be accepted by the action function")
            self.action_handlers[name] = function
            return function

        return register_action_handler


def invoke(function, parameters):
    ordered_parameters = []
    for parameter_definition in inspect.signature(function).parameters.values():
        annotation = parameter_definition.annotation
        if annotation == inspect._empty:
            raise Exception("Cannot inject parameter {} of function {}: Missing type annotation".format(
                parameter_definition.name, function))
        match_found = False
        for param in parameters:
            if isinstance(param, annotation):
                match_found = True
                ordered_parameters.append(param)
        if not match_found:
            raise Exception("Cannot inject parameter {} of function {}: No matching value".format(
                parameter_definition.name, function))
    return function(*ordered_parameters)


@dataclass
class ActorHandler:
    entity: Actor

    def handle_action(self, action_name, input, ctx: Context):
        if action_name not in self.entity.action_handlers:
            raise Exception("Missing action handler function for Actor {} and action {}".format(
                self.entity.settings.name, action_name))
        return invoke(self.entity.action_handlers[action_name], [input, ctx])
