"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Blueprint, request

from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2

from eigr.functions.protocol.actors.protocol_pb2 import ActorInvocation as Invocation
from eigr.functions.protocol.actors.protocol_pb2 import ActorInvocationResponse as InvocationResponse
from eigr.functions.protocol.actors.protocol_pb2 import Context

import logging


action_endpoint = Blueprint(
    'action_endpoint', __name__, template_folder='templates')


@action_endpoint.route('/system/<string:system>/actors/<string:name>/invoke', methods=["POST"])
def action(name: str, system: str):
    data = request.data
    logging.info('Received Actor action request: %s', data)
    # Decode request payload data here and call python real actors methods.
    # Then send ActorInvocationResponse back to the caller

    return 'Hello, World!'
