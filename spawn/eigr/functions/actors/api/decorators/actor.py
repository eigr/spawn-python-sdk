import functools

from spawn.eigr.functions.actors.internal.core import ActorInfo, Actors


def Actor(cls):

    @functools.wraps(cls)
    def wrapper_actor(*args, **kwargs):
        wrapper_actor.instance = cls(*args, **kwargs)

        print(type(wrapper_actor.instance).__name__)
        cls_name = type(wrapper_actor.instance).__name__
        settings = kwargs.get('settings')

        actor_info = ActorInfo(name=settings.name, settings=settings)
        Actors().actors.update({cls_name: actor_info})

    return wrapper_actor
