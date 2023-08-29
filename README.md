# Spawn Python SDK
Python User Language Support for [Spawn](https://github.com/eigr/spawn).

# Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Advanced Use Cases](#advanced-use-cases)
   - [Types of Actors](#types-of-actors)
   - [Broadcast](#broadcast)
   - [Side Effects](#side-effects)
   - [Forward](#forward)
   - [Pipe](#pipe)
   - [State Management](#state-management)
4. [Using Actors](#using-actors)
   - [Call Named Actors](#call-named-actors)
   - [Call Unnamed Actors](#call-unnamed-actors)
   - [Async and other options](#async-calls-and-other-options)
5. [Deploy](#deploy)
   - [Packing with Containers](#packing-with-containers)
   - [Defining an ActorSytem](#defining-an-actorsytem)
   - [Defining an ActorHost](#defining-an-actorhost)
   - [Activators](#activators)
6. [Actor Model](#actor-model)
   - [Virtual Actors](#virtual-actors)


## Overview

Spawn is a Stateful Serverless Runtime and Framework basead on the [Actor Model](https://youtu.be/7erJ1DV_Tlo) and operates as a Service Mesh.

Spawn's main goal is to remove the complexity in developing services or microservices, providing simple and intuitive APIs, as well as a declarative deployment and configuration model and based on a Serverless architecture and Actor Model.
This leaves the developer to focus on developing the business domain while the platform deals with the complexities and infrastructure needed to support the scalable, resilient, distributed, and event-driven architecture that modern systems requires.

Spawn is based on the sidecar proxy pattern to provide a polyglot Actor Model framework and platform.
Spawn's technology stack, built on the [BEAM VM](https://www.erlang.org/blog/a-brief-beam-primer/) (Erlang's virtual machine) and [OTP](https://www.erlang.org/doc/design_principles/des_princ.html), provides support for different languages from its native Actor model.

For more information consult the main repository [documentation](https://github.com/eigr/spawn).

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
from domain.domain_pb2 import JoeState
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value

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

But of course you will need to locally run the our Elixir proxy which will actually provide all the functionality for your Python application. One way to do this is to create a docker-compose file containing all the services that your application depends on, in this case, in addition to the Spawn proxy, it also has a database and possibly a nats broker if you want access to more advanced Spawn features.

```docker-compose
version: "3.8"
services:
  mariadb:
    image: mariadb
    environment:
      MYSQL_ROOT_PASSWORD: admin
      MYSQL_DATABASE: eigr-functions-db
      MYSQL_USER: admin
      MYSQL_PASSWORD: admin
    volumes:
      - mariadb:/var/lib/mysql
    ports:
      - "3307:3306"
  nats:
    image: nats:0.8.0
    entrypoint: "/gnatsd -DV"
    ports:
      - "8222:8222"
      - "4222:4222"
  spawn-proxy:
    build:
      context: https://github.com/eigr/spawn.git#main
      dockerfile: ./Dockerfile-proxy
    restart: always
    network_mode: "host"
    environment:
      SPAWN_USE_INTERNAL_NATS: "true"
      SPAWN_PUBSUB_ADAPTER: nats
      SPAWN_STATESTORE_KEY: 3Jnb0hZiHIzHTOih7t2cTEPEpY98Tu1wvQkPfq/XwqE=
      PROXY_APP_NAME: spawn
      PROXY_CLUSTER_STRATEGY: gossip
      PROXY_DATABASE_PORT: 3307
      PROXY_DATABASE_TYPE: mariadb
      PROXY_HTTP_PORT: 9003
      USER_FUNCTION_PORT: 8091
    depends_on:
      - mariadb
      - nats
networks:
  mysql-compose-network:
    driver: bridge
volumes:
  mariadb:

```

And this is it to start! Now that you know the basics of local development, we can go a little further.

## Advanced Use Cases

Spawn Actors abstract a huge amount of developer infrastructure and can be used for many different types of jobs. In the sections below we will demonstrate some of the features available in Spawn that contribute to the development of complex applications in a simplified way.

### Types of Actors

First we need to understand how the various types of actors available in Spawn behave. Spawn defines the following types of Actors:

* **Named Actors**: Named actors are actors whose name is defined at compile time. They also behave slightly differently than unnamed actors and pooled actors. Named actors when they are defined with the stateful parameter equal to True are immediately instantiated when they are registered at the beginning of the program, they can also only be referenced by the name given to them in their definition.

* **Unnamed Actors**: Unlike named actors, unnamed actors are only created when they are named at runtime, that is, during program execution. Otherwise they behave like named actors.

* **Pooled Actors**: Pooled Actors, as the name suggests, are a collection of actors that are grouped under the same name assigned to them at compile time. Pooled actors are generally used when higher performance is needed and are also recommended for handling serverless loads.

Another important feature of Spawn Actors is that the lifecycle of each Actor is managed by the platform itself. This means that an Actor will exist when it is invoked and that it will be deactivated after an idle time in its execution. This pattern is known as [Virtual Actors](#virtual-actors) but Spawn's implementation differs from some other known frameworks like [Orleans](https://www.microsoft.com/en-us/research/project/orleans-virtual-actors/) or [Dapr](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/) by defining a specific behavior depending on the type of Actor (named, unnamed, pooled, and etc...). 

For example, named actors are instantiated the first time as soon as the host application registers them with the Spawn proxy. Whereas unnamed and pooled actors are instantiated the first time only when they receive their first invocation call.

### Broadcast

Actors in Spawn can subscribe to a thread and receive, as well as broadcast, events for a given thread.

To consume from a topic, you just need to configure the Actor decorator using the channel option as follows:

```python
actor = Actor(settings=ActorSettings(
    name="joe", stateful=True, channel="test"))
```
In the case above, the Actor `joe` was configured to receive events that are forwarded to the topic called `test`.

To produce events in a topic, just use the Broadcast Workflow. The example below demonstrates a complete example of producing and consuming events. In this case, the same actor is the event consumer and producer, but in a more realistic scenario, different actors would be involved in these processes.

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

### Side Effects

Actors can also emit side effects to other Actors as part of their response.
See an example:

```python
from domain.domain_pb2 import State, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.effect import Effect


actor = Actor(settings=ActorSettings(name="joe", stateful=True))


@actor.timer_action(every=1000)
def hi(ctx: Context) -> Value:
    new_state = None
    request = Request()
    request.language = "python"

    effect: Effect = Effect(action="setLanguage", payload=request,
                            system="spawn-system", actor="mike", parent="abs_actor")

    if not ctx.state:
        new_state = State()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value()\
        .effect(effect)\
        .state(new_state)\
        .noreply()

```

Side effects such as broadcast are not part of the response flow to the caller. They are request-asynchronous events that are emitted after the Actor's state has been saved in memory.

### Forward

Actors can route some actions to other actors as part of their response. For example, sometimes you may want another Actor to be responsible for processing a message that another Actor has received. We call this forwarding and it occurs when we want to forward the input argument of a request that a specific Actor has received to the input of an action in another Actor.

See an example:

```python
from domain.domain_pb2 import Request

from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.forward import Forward

actor = Actor(settings=ActorSettings(name="joe", stateful=True))

@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    return Value()\
        .forward(Forward("mike", "setLanguage"))\
        .reply()
```

### Pipe

Similarly, sometimes we want to chain a request through several different processes. For example forwarding an actor's computational output as another actor's input. There is this type of routing we call Pipe, as the name suggests, a pipe forwards what would be the response of the received request to the input of another Action in another Actor.
In the end, just like in a Forward, it is the response of the last Actor in the chain of routing to the original caller.

Example:

```python
from domain.domain_pb2 import State, Request, Reply

from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.pipe import Pipe

actor = Actor(settings=ActorSettings(name="joe", stateful=True))

@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    reply = Reply()
    reply.language = "python"

    if not ctx.state:
        new_state = State()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value()\
        .response(reply)\
        .pipe(Pipe("mike", "setLanguage"))\
        .reply()
```

Forwards and pipes do not have an upper thread limit other than the request timeout.

### State Management

The Spawn runtime handles the internal state of your actors. It is he who maintains its state based on the types of actors and configurations that you, the developer, have made.

The persistence of the state of the actors happens through snapshots that follow the [Write Behind Pattern](https://redisson.org/glossary/write-through-and-write-behind-caching.html) during the period in which the Actor is active and [Write Ahead](https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html) during the moment of the Actor's deactivation. That is, data is saved at regular intervals asynchronously while the Actor is active and once synchronously when the Actor suffers a deactivation, when it is turned off.

These snapshots happen from time to time. And this time is configurable through the ***snapshot_timeout*** property of the ***ActorSettings*** class. However, you can tell the Spawn runtime that you want it to persist the data immediately synchronously after executing an Action. And this can be done in the following way:

Example:

```python
from domain.domain_pb2 import State, Request, Reply

from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value
from spawn.eigr.functions.actors.api.workflows.pipe import Pipe

actor = Actor(settings=ActorSettings(name="joe", stateful=True, snapshot_timeout=2000))

@actor.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    reply = Reply()
    reply.language = "python"

    if not ctx.state:
        new_state = State()
        new_state.languages.append("python")
    else:
        new_state = ctx.state

    return Value()\
        .response(reply)\
        .pipe(Pipe("mike", "setLanguage"))\
        .reply(checkpoint=True)
```

The most important thing in this example is the use of the parameter checkpoint=True:

```python
.reply(checkpoint=True)
```

It is this parameter that will indicate to the Spawn runtime that you want the data to be saved immediately after this Action is called back.
In most cases this strategy is completely unnecessary, as the default strategy is sufficient for most use cases. But Spawn democratically lets you choose when you want your data persisted.

In addition to this functionality regarding state management, Spawn also allows you to perform some more operations on your Actors such as restoring the actor's state to a specific point in time:

Restore Example:

TODO

## Using Actors

There are several ways to interact with our actors, some internal to the application code and others external to the application code. In this section we will deal with the internal ways of interacting with our actors and this will be done through direct calls to them. For more details on the external ways to interact with your actors see the [Activators](#activators) section.

In order to be able to call methods of an Actor, we first need to get a reference to the actor. This is done with the help of the static method `create_actor_ref` of the `Spawn` class. This method accepts some arguments, the most important being `system`, `actor_name` and `parent`. 

In the sections below we will give some examples of how to invoke different types of actors in different ways.

### Call Named Actors

To invoke an actor named like the one we defined in section [Getting Started](#getting-started) we could do as follows:

```python
actor: ActorRef = Spawn.create_actor_ref(
    system="spawn-system",
    actor_name="joe"
)

request = Request()
request.language = "erlang"

(status, result) = actor.invoke(
    action="setLanguage", request=request)
print("Invocation Result Status: " + status)
print("Invocation Result Value:  " + str(result.response))
```

Calls like the one above, that is, synchronous calls, always returned a tuple composed of the invocation status message and the response object emitted by the Actor.

### Call Unnamed Actors

Unnamed actors are equally simple to invoke. All that is needed is to inform the `parent` parameter which refers to the name given to the actor that defines the ActorRef template.

To better exemplify, let's first show the Actor's definition code and later how we would call this actor with a concrete name at runtime:

```python
from domain.domain_pb2 import State, Request, Reply
from spawn.eigr.functions.actors.api.actor import Actor
from spawn.eigr.functions.actors.api.settings import ActorSettings, Kind
from spawn.eigr.functions.actors.api.context import Context
from spawn.eigr.functions.actors.api.value import Value

abstract = Actor(settings=ActorSettings(
    name="abs_actor", stateful=True, kind=Kind.UNNAMED))


@abstract.action("setLanguage")
def set_language(request: Request, ctx: Context) -> Value:
    print("Request -> " + str(request))
    print("Current State -> " + str(ctx.state))

    reply = Reply()
    reply.response = "erlang"
    new_state = State()
    new_state.languages.append("python")
    return Value().of(reply, new_state).reply()
```

The important part of the code above is the following snippet:

```python
abstract = Actor(settings=ActorSettings(
    name="abs_actor", stateful=True, kind=Kind.UNNAMED))
```

This tells Spawn that this actor will actually be named at runtime. The name parameter in this case is just a reference that will be used later so that we can actually create an instance of the real Actor.

Finally below we will see how to invoke such an actor. We'll name the royal actor "mike":

```python
# Get abstract actor reference called mike
actor: ActorRef = Spawn.create_actor_ref(
    system="spawn-system",
    actor_name="mike",
    parent="abs_actor"
)

request = Request()
request.language = "erlang"

(status, result) = actor.invoke(
    action="setLanguage", request=request)
print("Invocation Result Status: " + status)
print("Invocation Result Value:  " + str(result.response))
```

### Async calls and other options

Basically Spawn can perform actor functions in two ways. Synchronously, where the callee waits for a response, or asynchronously, where the callee doesn't care about the return value of the call. In this context we should not confuse Spawn's asynchronous way with Python's concept of async because async for Spawn is just a fire-and-forget call.

Therefore, to call an actor's function asynchronously, just inform the parameter async_mode with the value True:

```python
some_actor.invoke(
    action="setLanguage", request=request, async_mode=True)
```

## Deploy

See [Getting Started](https://github.com/eigr/spawn#getting-started) section from the main Spawn repository for more details on how to deploy a Spawn application.

### Packing with Containers 

Spawn is a k8s based runtime and therefore your workloads should be made up of containers.

So all you need to do is create a container with your Python application. There are several tutorials on the internet that can help you with this process and we will not go into detail in this document.

### Defining an ActorSytem

See [Getting Started](https://github.com/eigr/spawn#getting-started) section from the main Spawn repository for more details on how to define an ActorSystem.

### Defining an ActorHost

See [Getting Started](https://github.com/eigr/spawn#getting-started) section from the main Spawn repository for more details on how to define an ActorHost.

### Activators
TODO

## Actor Model

According to Wikipedia Actor Model is:

"A mathematical model of concurrent computation that treats actor as the universal primitive of concurrent computation. In response to a message it receives, an actor can: make local decisions, create more actors, send more messages, and determine how to respond to the next message received. Actors may modify their own private state, but can only affect each other indirectly through messaging (removing the need for lock-based synchronization).

The actor model originated in 1973. It has been used both as a framework for a theoretical understanding of computation and as the theoretical basis for several practical implementations of concurrent systems."

The Actor Model was proposed by Carl Hewitt, Peter Bishop, and Richard Steiger and is inspired by several characteristics of the physical world.

Although it emerged in the 70s of the last century, only in the previous two decades of our century has this model gained strength in the software engineering communities due to the massive amount of existing data and the performance and distribution requirements of the most current applications.

For more information about the Actor Model, see the following links:

https://en.wikipedia.org/wiki/Actor_model

https://codesync.global/media/almost-actors-comparing-pony-language-to-beam-languages-erlang-elixir/

https://www.infoworld.com/article/2077999/understanding-actor-concurrency--part-1--actors-in-erlang.html

https://doc.akka.io/docs/akka/current/general/actors.html

### Virtual Actors

In the context of the Virtual Actor paradigm, actors possess the inherent ability to seamlessly retain their state. The underlying framework dynamically manages the allocation of actors to specific nodes. If a node happens to experience an outage, the framework automatically revives the affected actor on an alternate node. This process of revival maintains data integrity as actors are inherently designed to preserve their state. Interruptions to availability are minimized during this seamless transition, contingent on the actors correctly implementing their state preservation mechanisms.

The Virtual Actor model offers several merits:

* **Scalability**: The system can effortlessly accommodate a higher number of actor instances by introducing additional nodes.

* **Availability**: In case of a node failure, actors swiftly and nearly instantly regenerate on another node, all while safeguarding their state from loss.