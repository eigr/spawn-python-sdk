import logging
from functools import wraps

from spawn.eigr.functions.actors.settings import ActorSettings
from spawn.eigr.functions.actors.decorators.actor import ActionInfo, Actor, Actors, Context

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def action(name: str = None):
    def decorator(func):
        _logger.debug("Registering Action {0}".format(func.__name__))

        cls_name = func.__class__.__name__
        func_name = func.__name__ if not name else name
        print(cls_name)
        print(func_name)
        action_info = ActionInfo(name=func_name)

        _logger.debug("Actors {0}".format(Actors().actors))
        # print("One line Code Key value: ", dict.keys())

        # actor_info = Actors().actors.get(cls_name)
        # actor_info.actions.append(action_info)

        # Actors().actors.update(cls_name, actor_info)

        @ wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@ Actor
class MyActor:
    def __init__(self, settings: ActorSettings):
        self.settings = settings

    @ action(name="sum")
    def sum(input, ctx: Context):
        pass
