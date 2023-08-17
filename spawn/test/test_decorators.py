import logging

from spawn.eigr.functions.actors.internal.core import ActorSettings
from spawn.eigr.functions.actors.api.decorators.action import MyActor

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def test_decorators():
    actor_one = MyActor(settings=ActorSettings(
        name="myactora", stateful=False))


if __name__ == '__main__':
    # TODO definir env PYTHONPATH=/Users/jorley/Workspace/Repositorios/Publicos/spawn-python-sdk python spawn/test/test_decorators.py
    actor_one = MyActor(settings=ActorSettings(
        name="myactora", stateful=False))
