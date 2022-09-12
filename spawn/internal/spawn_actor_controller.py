"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from actor_entity import ActorEntity

from dataclasses import (dataclass, field)
from typing import List

from urllib import request, parse

import logging


class SpawnActorController:

    def register(self, actors: List[ActorEntity]):
        logging.info('Registering Actors on the Proxy %s', actors)
