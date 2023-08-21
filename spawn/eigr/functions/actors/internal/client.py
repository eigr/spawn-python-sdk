
import requests
import os

from requests.adapters import HTTPAdapter, Retry

from spawn.eigr.functions.protocol.actors.protocol_pb2 import (
    SpawnRequest,
    SpawnResponse,
    InvocationRequest,
    InvocationResponse,
    RegistrationRequest,
    RegistrationResponse
)

_DEFAULT_HEADERS = {
    "Accept": "application/octet-stream",
    "Content-Type": "application/octet-stream",
}
_DEFAULT_MAX_RETRIES = 100
_DEFAULT_MAX_RETRIES_BACKOFF_FACTOR = 0.2

req = requests.Session()
retries = Retry(total=_DEFAULT_MAX_RETRIES,
                backoff_factor=_DEFAULT_MAX_RETRIES_BACKOFF_FACTOR)
req.mount('http://', HTTPAdapter(max_retries=retries))


class SpawnClient:
    _instance = None

    def __init__(self, host: str = None, port: str = None):
        self.host = os.environ.get(
            "PROXY_HTTP_HOST", "0.0.0.0") if not host else host
        self.port = os.environ.get(
            "PROXY_HTTP_PORT", "9001") if not port else port

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def register(self, request: RegistrationRequest) -> RegistrationResponse:
        proxy_url = "http://{}:{}{}".format(self.host,
                                            self.port, "/api/v1/system")

        binary_payload = request.SerializeToString()

        resp = req.post(
            proxy_url, data=binary_payload, headers=_DEFAULT_HEADERS
        )

        databytes = bytes(resp.content)
        response = RegistrationResponse()
        response.ParseFromString(databytes)
        return response

    def spawn(self, system: str, request: SpawnRequest, revision: int = None) -> SpawnResponse:
        proxy_url: str = None
        if not revision:
            proxy_url = "http://{}:{}/api/v1/system/{}/actors/spawn".format(self.host,
                                                                            self.port, system)
        else:
            proxy_url = "http://{}:{}/api/v1/system/{}/actors/spawn?revision={}".format(self.host,
                                                                                        self.port, system, revision)

        binary_payload = request.SerializeToString()

        resp = req.post(
            proxy_url, data=binary_payload, headers=_DEFAULT_HEADERS
        )

        databytes = bytes(resp.content)
        response = SpawnResponse()
        response.ParseFromString(databytes)
        return response

    def invoke(self, system: str, actor: str, request: InvocationRequest) -> InvocationResponse:
        proxy_url = "http://{}:{}/api/v1/system/{}/actors/{}/invoke".format(self.host,
                                                                            self.port, system, actor)

        binary_payload = request.SerializeToString()

        resp = req.post(
            proxy_url, data=binary_payload, headers=_DEFAULT_HEADERS
        )

        databytes = bytes(resp.content)
        response = InvocationResponse()
        response.ParseFromString(databytes)
        return response
