# import logging
# import importlib
# from spawn.eigr.functions.actors.api.context import Context

# from spawn.eigr.functions.actors.internal.core import ActorSettings
# from spawn.eigr.functions.actors.api.decorators.action import MyActor

# logging.basicConfig(level=logging.DEBUG)
# _logger = logging.getLogger(__name__)


# def import_class_from_string(path):
#     from importlib import import_module
#     module_path, _, class_name = path.rpartition('.')
#     mod = import_module(module_path)
#     klass = getattr(mod, class_name)
#     return klass


# def spawn(tospawn, *args, **kwargs):
#     obj = tospawn(*args, **kwargs)
#     obj


# class Spawner:

#     @classmethod
#     def spawn(cls, tospawn, *args, **kwargs):
#         tospawn(*args, **kwargs)


# def test_decorators():
#     settings: ActorSettings = ActorSettings(
#         name="myactora", stateful=False)

#     actor_one = MyActor(settings=settings)

from spawn.eigr.functions.actors.internal.controller import ActorController


if __name__ == '__main__':

    #     # TODO definir env PYTHONPATH=/Users/jorley/Workspace/Repositorios/Publicos/spawn-python-sdk python spawn/test/test_decorators.py
    #     settings: ActorSettings = ActorSettings(
    #         name="myactora", stateful=False)

    #     # actor_one = MyActor(settings=ActorSettings(
    #     #     name="myactora", stateful=False))

    #     instance = Spawner.spawn(MyActor, settings=settings)
    #     print(instance)

    #     # type = MyActor
    #     # module = type.__module__
    #     # cls_name = type.__name__

    #     # type_str = f"{module}.{cls_name}"

    #     # c = type(type_str)

    #     # c = type.__new__(type.__name__, settings)

    #     # typeclass = import_class_from_string(f"{module}.{cls_name}")
    #     # t = typeclass.__class__
    #     # test = type(t) is MyActor
    #     # print(c)
    #     # instance = typeclass(settings)
    #     # print(f"Teste {instance}")

    #     print(instance.sum("test", Context()))
