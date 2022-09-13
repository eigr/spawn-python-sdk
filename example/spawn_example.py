"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from spawn.sdk import Spawn
from example.joe import JoeActor 

if __name__ == '__main__':
    spawn = Spawn()\
        .port('8080')\
        .register_actor(JoeActor.entity)\
        .start()
