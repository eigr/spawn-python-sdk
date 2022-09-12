"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Blueprint, request, send_file

from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2

from eigr.functions.protocol.actors.protocol_pb2 import ActorInvocation as Invocation
from eigr.functions.protocol.actors.protocol_pb2 import ActorInvocationResponse as InvocationResponse
from eigr.functions.protocol.actors.protocol_pb2 import Context

import io
import logging

action_handler = Blueprint(
    'action_endpoint', __name__, url_prefix='/api/v1')


@action_handler.route('/system/<string:system>/actors/<string:name>/invoke', methods=["POST"])
def action(name: str, system: str):
    data = request.data
    logging.info('Received Actor action request: %s', data)
    # Decode request payload data here and call python real actors methods.
    invocation = Invocation.ParseFromString(data)
    logging.debug('Actor invocation data: %s', invocation)
    
    # Update Context
    updated_context = Context()

    # Then send ActorInvocationResponse back to the caller
    actor_invocation_response = InvocationResponse()
    actor_invocation_response.actor_name = invocation.actor_name
    actor_invocation_response.actor_system = invocation.actor_system
    actor_invocation_response.updated_context = updated_context

    return send_file(
        io.BytesIO(actor_invocation_response.SerializeToString()),
        mimetype='application/octet-stream'
    )
