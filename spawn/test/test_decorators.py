import logging

from spawn.eigr.functions.actors.settings import ActorSettings
from spawn.eigr.functions.actors.decorators.action import MyActor
from spawn.eigr.functions.actors.decorators.actor import Actors

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def test_decorators():
    teste = Actors()
    # actor_one = MyActor()
    # actor_two = MyActor()
    # assert actor_one.sum(values=[1, 4]) == 5
    # assert actor_two.sum(values=[2, 4]) == 6


if __name__ == '__main__':
    # TODO definir env PYTHONPATH=/Users/jorley/Workspace/Repositorios/Publicos/spawn-python-sdk python spawn/test/test_decorators.py
    actor_one = MyActor(settings=ActorSettings(
        name="myactora", stateful=False))

    # actor_two = MyActor(settings=ActorSettings(
    #     name="myactorb", stateful=False))
    # _logger.debug(Actors().actors.get(MyActor))

    # _logger.debug(actor_one.sum(values=[1, 4]))
    # _logger.debug(actor_two.sum(values=[2, 4]))
