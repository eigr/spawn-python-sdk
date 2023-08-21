# Spawn Python SDK
Python User Language Support for [Spawn](https://github.com/eigr/spawn).

# Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Advanced Use Cases](#advanced-use-cases)
   - [Side Effects](#side-effects)
   - [Broadcast](#broadcast)
   - [Forward](#forward)
   - [Pipe](#pipe)
4. [Deploy](#deploy)
   - [Packing with Containers](#packing-with-containers)
   - [Defining an ActorSytem](#defining-an-actorsytem)
   - [Defining an ActorHost](#defining-an-actorhost)


## Overview
TODO

## Getting Started

First we must create a new Python project. In this example we will use [Poetry](https://python-poetry.org) as our package manager.

```shell
poetry new spawn-py-demo
```

The second thing we have to do is add the spawn dependency to the project.

```toml
[tool.poetry.dependencies]
python = ">=3.9.7,<4.0"
spawn = {git = "https://github.com/eigr/spawn-python-sdk.git"}
```

Now it is necessary to download the dependencies via Poetry:

```shell
poetry env use python3 # use your own python here
poetry lock
poetry install
```

So far it's all pretty boring and not really Spawn related so it's time to start playing for real.
The first thing we're going to do is define a place to put our protobuf files. In the root of the project we will create a folder called protobuf and some subfolders

```shell
mkdir -p spawn_py_demo/protobuf/domain
```

That done, let's create our protobuf file inside the example folder.

```shell
touch spawn_py_demo/protobuf/domain/domain.proto
```

And let's populate this file with the following content:

```proto
syntax = "proto3";

package domain;

message JoeState {
  repeated string languages = 1;
}

message Request {
  string language = 1;
}

message Reply {
  string response = 1;
}
```

We must compile this file using the protoc utility. In the root of the project type the following command:

```shell
protoc -I spawn_py_demo/protobuf/ --python_out=spawn_py_demo spawn_py_demo/protobuf/domain/domain.proto
```

Now in the spawn_py_demo folder we will create our first python file containing the code of our Actor.

```shell
touch spawn_py_demo/joe.py
```

Populate this file with the following content:

```python
from domain.domain_pb2 import JoeState, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast

actor = Actor(settings=ActorSettings(
    name="joe", stateful=True, channel="test"))


@actor.timer_action(every=1000)
def hi(ctx: Context) -> Value:
    new_state = None

    if not ctx.state:
        new_state = JoeState()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value().state(new_state).noreply()
```

Now with our Actor properly defined, we just need to start the SDK correctly. Create another file called main.py to serve as your application's entrypoint and fill it with the following content:

```python
from spawn.eigr.functions.actors.api.sdk import Spawn
from joe import actor as joe_actor

if __name__ == "__main__":
    spawn = Spawn()
    spawn.port(8091).proxy_port(9003).actor_system(
        "spawn-system").add_actor(joe_actor).start()
```

Then:

```shell
poetry run python3 spawn_py_demo/main.py
```

And this is it to start! Now that you know the basics of local development, we can go a little further.

## Advanced Use Cases
TODO

### Side Effects
TODO

### Broadcast
TODO

```python
from domain.domain_pb2 import JoeState, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.broadcast import Broadcast

actor = Actor(settings=ActorSettings(
    name="joe", stateful=True, channel="test"))


@actor.timer_action(every=1000)
def hi(ctx: Context) -> Value:
    new_state = None
    request = Request()
    request.language = "python"
    broadcast = Broadcast()
    broadcast.channel = "test"
    broadcast.action_name = "setLanguage"
    broadcast.value = request

    if not ctx.state:
        new_state = JoeState()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value()\
        .broadcast(broadcast)\
        .state(new_state)\
        .noreply()


@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    reply = Reply()
    reply.response = "erlang"
    return Value().of(reply, ctx.state).reply()
```

### Forward
TODO

### Pipe
TODO

## Deploy
TODO

### Packing with Containers 
TODO

### Defining an ActorSytem
TODO

### Defining an ActorHost
TODO 
   