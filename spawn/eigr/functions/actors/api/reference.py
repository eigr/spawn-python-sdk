
from spawn.eigr.functions.actors.internal.client import SpawnClient

from spawn.eigr.functions.protocol.actors.actor_pb2 import (
    Actor,
    ActorId,
    ActorState,
    Metadata,
    ActorSettings,
    Action,
    FixedTimerAction,
    ActorSnapshotStrategy,
    ActorDeactivationStrategy,
    ActorSystem,
    Kind,
    Registry,
    TimeoutStrategy,
)

from spawn.eigr.functions.protocol.actors.protocol_pb2 import (
    SpawnRequest,
    SpawnResponse,
    InvocationRequest,
    InvocationResponse,
    RegistrationRequest,
    RegistrationResponse
)


def spawn(client: SpawnClient, system: str, actor: str, parent: str, revision: int = None):
    actor_id = ActorId()
    actor_id.name = actor
    actor_id.system = system

    if parent != None:
        actor_id.parent = parent

    request: SpawnRequest = SpawnRequest()
    request.actors.append(actor_id)
    spawn_response: SpawnResponse = client.spawn(system, request, revision)
    return spawn_response


class ActorRef:
    def __init__(self, client: SpawnClient, system: str, actor: str, parent: str = None, revision: int = None):
        self.__spawn_client = client
        self.actor_system = system
        self.actor_name = actor
        self.actor_parent = parent
        self.revision = revision
        if parent != None:
            spawn(self.__spawn_client, self.actor_system,
                  self.actor_name, self.actor_parent, self.revision)

    def invoke(self, request: any):
        pass
