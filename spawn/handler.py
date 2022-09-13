"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
from flask import Blueprint, request, send_file

from google.protobuf.any_pb2 import Any as ProtoAny

from spawn.eigr.protocol_pb2 import ActorInvocation, ActorInvocationResponse, Context

import io
import logging

action_handler = Blueprint('action_endpoint', __name__)


@action_handler.route('/actors/actions', methods=["POST"])
def action():
    data = request.data
    logging.info('Received Actor action request: %s', data)
    
    # Decode request payload data here and call python real actors methods.
    databytes = bytes(data)
    actor_invocation = ActorInvocation()
    actor_invocation.ParseFromString(databytes)
    logging.debug('Actor invocation data: %s', actor_invocation)
    
    # Update Context
    updated_context = Context()

    # Then send ActorInvocationResponse back to the caller
    actor_invocation_response = ActorInvocationResponse()
    actor_invocation_response.actor_name = actor_invocation.actor_name
    actor_invocation_response.actor_system = actor_invocation.actor_system
    actor_invocation_response.updated_context.CopyFrom(updated_context)

    return send_file(
        io.BytesIO(actor_invocation_response.SerializeToString()),
        mimetype='application/octet-stream'
    )
