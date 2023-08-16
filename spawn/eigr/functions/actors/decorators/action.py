import logging
from functools import wraps

from spawn.eigr.functions.actors.settings import ActorSettings
from spawn.eigr.functions.actors.decorators.actor import ActionInfo, Actor, Actors, Context

_logger = logging.getLogger(__name__)


def action(name: str = None):
    def decorator(func):
        _logger.debug("Registering Action {0}".format(func.__name__))

        cls_name = func.__module__
        func_name = func.__name__ if not name else name
        action_info = ActionInfo(name=func_name)

        actor_info = Actors.actors().get(cls_name)
        actor_info.actions.append(action_info)

        Actors.actors().update(cls_name, actor_info)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@Actor(settings=ActorSettings(name="myactor", stateful=False))
class MyActor:
    def __init__(self):
        pass

    @action(name="sum")
    def sum(input, ctx: Context):
        pass


actor = MyActor()
actor.__get_settings__
