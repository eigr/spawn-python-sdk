
from spawn.eigr.functions.actors.internal.client import SpawnClient
from spawn.eigr.functions.actors.internal.controller import pack, get_payload

from spawn.eigr.functions.protocol.actors.actor_pb2 import (
    Actor,
    ActorId,
    ActorSystem
)

from spawn.eigr.functions.protocol.actors.protocol_pb2 import (
    SpawnRequest,
    SpawnResponse,
    InvocationRequest,
    InvocationResponse,
    RequestStatus,
    Status
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

    def invoke(self, action: str, request: any = None, async_mode: bool = False, pooled: bool = False):
        req: InvocationRequest = self.__build_request(
            action, request, async_mode, pooled)

        resp: InvocationResponse = self.__spawn_client.invoke(
            self.actor_system, self.actor_name, req)

        return self.__build_result(resp)

    def __build_request(self, action: str, request: any, async_mode: bool = False, pooled: bool = False):
        req: InvocationRequest = InvocationRequest()
        system = ActorSystem()
        system.name = self.actor_system

        actor_id = ActorId()
        actor_id.name = self.actor_name
        actor_id.system = self.actor_system

        actor = Actor()
        actor.id.CopyFrom(actor_id)

        req.system.CopyFrom(system)
        req.actor.CopyFrom(actor)
        req.action_name = action
        req.pooled = pooled
        setattr(req, 'async', async_mode)

        if request != None:
            req.value.CopyFrom(pack(request))

        return req

    def __build_result(self, resp: InvocationResponse) -> any:
        sts: RequestStatus = resp.status

        if sts.status == Status.OK:
            output = None if resp.WhichOneof(
                "payload") == "noop" else get_payload(resp.value)

            return "ok", output
        elif sts.status == Status.ACTOR_NOT_FOUND:
            return "actor_not_found", None
        else:
            return "error", None
