from functools import wraps

from spawn.eigr.functions.actor_settings import ActorSettings


class Actor:
    actions = None

    def __init__(self, settings: ActorSettings):
        self.settings = settings

    def __call__(self, *args, **kwds):
        def __get_settings__(self):
            print(self.settings)
            return self.settings

        def __register_action__(self, action):
            pass
