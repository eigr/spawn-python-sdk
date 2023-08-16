import logging
from functools import wraps

from spawn.eigr.functions.actor_settings import ActorSettings
from spawn.eigr.functions.decorators.actor import Actor

_logger = logging.getLogger(__name__)


def action(name):
    def decorator(func):
        _logger.debug("Registering Action {0}".format(func.__name__))

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@Actor(settings=ActorSettings(name="myactor", kind="singleton", deactivate_timeout=1, snapshot_timeout=2))
class MyActor:
    def __init__(self):
        pass

    @action(name="sum")
    def sum(type):
        pass


actor = MyActor()
actor.__get_settings__
