
import inspect

from dataclasses import dataclass, field
from typing import Callable, MutableMapping

from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.settings import ActorSettings


@dataclass
class TimerFunction:
    every: int
    action: Callable


@dataclass
class Actor:
    settings: ActorSettings

    action_handlers: MutableMapping[str,
                                    Callable] = field(default_factory=dict)

    timer_action_handlers: MutableMapping[str,
                                          Callable] = field(default_factory=dict)

    def action(self, name: str):
        def register_action_handler(function):
            """
            Register the function to handle actions
            """
            action_name = name if name is not None else function.__name__

            if action_name in self.action_handlers:
                raise Exception("Action handler function {} already defined for action {}".format(
                    self.action_handlers[action_name], action_name))
            if function.__code__.co_argcount > 2:
                raise Exception(
                    "At most two parameters, the input parameter and the context parameter, should be accepted by the action function")
            self.action_handlers[action_name] = function
            return function

        return register_action_handler

    def timer_action(self, every: int, name: str = None):
        def register_timer_action_handler(function):
            """
            Register the function to handle actions
            """
            action_name = name if name is not None else function.__name__

            if name in self.timer_action_handlers:
                raise Exception("Timer Action handler function {} already defined for action {}".format(
                    self.timer_action_handlers[action_name], action_name))
            if function.__code__.co_argcount > 2:
                raise Exception(
                    "At most two parameters, the input parameter and the context parameter, should be accepted by the action function")
            self.timer_action_handlers[action_name] = TimerFunction(
                every=every, action=function)
            return function

        return register_timer_action_handler


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
        if action_name in self.entity.action_handlers:
            return invoke(self.entity.action_handlers[action_name], [input, ctx])
        elif action_name in self.entity.timer_action_handlers:
            action = self.entity.timer_action_handlers[action_name].action
            return invoke(action, [input, ctx])
        else:
            error = "Missing action handler function for Actor [{}] and Action [{}]".format(
                self.entity.settings.name, action_name)
            raise Exception(error)
