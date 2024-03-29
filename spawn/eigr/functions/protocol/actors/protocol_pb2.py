# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eigr/functions/protocol/actors/protocol.proto
"""Generated protocol buffer code."""
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from spawn.eigr.functions.protocol.actors import actor_pb2 as eigr_dot_functions_dot_protocol_dot_actors_dot_actor__pb2
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-eigr/functions/protocol/actors/protocol.proto\x12\x17\x65igr.functions.protocol\x1a*eigr/functions/protocol/actors/actor.proto\x1a\x19google/protobuf/any.proto\"\xf8\x02\n\x07\x43ontext\x12#\n\x05state\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\x12@\n\x08metadata\x18\x04 \x03(\x0b\x32..eigr.functions.protocol.Context.MetadataEntry\x12\x38\n\x04tags\x18\x05 \x03(\x0b\x32*.eigr.functions.protocol.Context.TagsEntry\x12\x37\n\x06\x63\x61ller\x18\x02 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\x12\x35\n\x04self\x18\x03 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x06\n\x04Noop\"\x1b\n\x08JSONType\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\x94\x01\n\x13RegistrationRequest\x12:\n\x0cservice_info\x18\x01 \x01(\x0b\x32$.eigr.functions.protocol.ServiceInfo\x12\x41\n\x0c\x61\x63tor_system\x18\x02 \x01(\x0b\x32+.eigr.functions.protocol.actors.ActorSystem\"\x86\x01\n\x14RegistrationResponse\x12\x36\n\x06status\x18\x01 \x01(\x0b\x32&.eigr.functions.protocol.RequestStatus\x12\x36\n\nproxy_info\x18\x02 \x01(\x0b\x32\".eigr.functions.protocol.ProxyInfo\"\xd4\x01\n\x0bServiceInfo\x12\x14\n\x0cservice_name\x18\x01 \x01(\t\x12\x17\n\x0fservice_version\x18\x02 \x01(\t\x12\x17\n\x0fservice_runtime\x18\x03 \x01(\t\x12\x1c\n\x14support_library_name\x18\x04 \x01(\t\x12\x1f\n\x17support_library_version\x18\x05 \x01(\t\x12\x1e\n\x16protocol_major_version\x18\x06 \x01(\x05\x12\x1e\n\x16protocol_minor_version\x18\x07 \x01(\x05\"G\n\x0cSpawnRequest\x12\x37\n\x06\x61\x63tors\x18\x01 \x03(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\"G\n\rSpawnResponse\x12\x36\n\x06status\x18\x01 \x01(\x0b\x32&.eigr.functions.protocol.RequestStatus\"v\n\tProxyInfo\x12\x1e\n\x16protocol_major_version\x18\x01 \x01(\x05\x12\x1e\n\x16protocol_minor_version\x18\x02 \x01(\x05\x12\x12\n\nproxy_name\x18\x03 \x01(\t\x12\x15\n\rproxy_version\x18\x04 \x01(\t\"I\n\nSideEffect\x12;\n\x07request\x18\x01 \x01(\x0b\x32*.eigr.functions.protocol.InvocationRequest\"\x98\x01\n\tBroadcast\x12\x15\n\rchannel_group\x18\x01 \x01(\t\x12\x13\n\x0b\x61\x63tion_name\x18\x02 \x01(\t\x12%\n\x05value\x18\x03 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12-\n\x04noop\x18\x04 \x01(\x0b\x32\x1d.eigr.functions.protocol.NoopH\x00\x42\t\n\x07payload\"*\n\x04Pipe\x12\r\n\x05\x61\x63tor\x18\x01 \x01(\t\x12\x13\n\x0b\x61\x63tion_name\x18\x02 \x01(\t\"-\n\x07\x46orward\x12\r\n\x05\x61\x63tor\x18\x01 \x01(\t\x12\x13\n\x0b\x61\x63tion_name\x18\x02 \x01(\t\"\xe6\x01\n\x08Workflow\x12\x35\n\tbroadcast\x18\x02 \x01(\x0b\x32\".eigr.functions.protocol.Broadcast\x12\x34\n\x07\x65\x66\x66\x65\x63ts\x18\x01 \x03(\x0b\x32#.eigr.functions.protocol.SideEffect\x12-\n\x04pipe\x18\x03 \x01(\x0b\x32\x1d.eigr.functions.protocol.PipeH\x00\x12\x33\n\x07\x66orward\x18\x04 \x01(\x0b\x32 .eigr.functions.protocol.ForwardH\x00\x42\t\n\x07routing\"\xe7\x03\n\x11InvocationRequest\x12;\n\x06system\x18\x01 \x01(\x0b\x32+.eigr.functions.protocol.actors.ActorSystem\x12\x34\n\x05\x61\x63tor\x18\x02 \x01(\x0b\x32%.eigr.functions.protocol.actors.Actor\x12\x13\n\x0b\x61\x63tion_name\x18\x03 \x01(\t\x12%\n\x05value\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12-\n\x04noop\x18\x07 \x01(\x0b\x32\x1d.eigr.functions.protocol.NoopH\x00\x12\r\n\x05\x61sync\x18\x05 \x01(\x08\x12\x37\n\x06\x63\x61ller\x18\x06 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\x12J\n\x08metadata\x18\x08 \x03(\x0b\x32\x38.eigr.functions.protocol.InvocationRequest.MetadataEntry\x12\x14\n\x0cscheduled_to\x18\t \x01(\x03\x12\x0e\n\x06pooled\x18\n \x01(\x08\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\t\n\x07payload\"\xb3\x02\n\x0f\x41\x63torInvocation\x12\x36\n\x05\x61\x63tor\x18\x01 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\x12\x13\n\x0b\x61\x63tion_name\x18\x02 \x01(\t\x12\x39\n\x0f\x63urrent_context\x18\x03 \x01(\x0b\x32 .eigr.functions.protocol.Context\x12%\n\x05value\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12-\n\x04noop\x18\x05 \x01(\x0b\x32\x1d.eigr.functions.protocol.NoopH\x00\x12\x37\n\x06\x63\x61ller\x18\x06 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorIdB\t\n\x07payload\"\xa8\x02\n\x17\x41\x63torInvocationResponse\x12\x12\n\nactor_name\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63tor_system\x18\x02 \x01(\t\x12\x39\n\x0fupdated_context\x18\x03 \x01(\x0b\x32 .eigr.functions.protocol.Context\x12%\n\x05value\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12-\n\x04noop\x18\x06 \x01(\x0b\x32\x1d.eigr.functions.protocol.NoopH\x00\x12\x33\n\x08workflow\x18\x05 \x01(\x0b\x32!.eigr.functions.protocol.Workflow\x12\x12\n\ncheckpoint\x18\x07 \x01(\x08\x42\t\n\x07payload\"\xa0\x02\n\x12InvocationResponse\x12\x36\n\x06status\x18\x01 \x01(\x0b\x32&.eigr.functions.protocol.RequestStatus\x12;\n\x06system\x18\x02 \x01(\x0b\x32+.eigr.functions.protocol.actors.ActorSystem\x12\x34\n\x05\x61\x63tor\x18\x03 \x01(\x0b\x32%.eigr.functions.protocol.actors.Actor\x12%\n\x05value\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12-\n\x04noop\x18\x05 \x01(\x0b\x32\x1d.eigr.functions.protocol.NoopH\x00\x42\t\n\x07payload\"Q\n\rRequestStatus\x12/\n\x06status\x18\x01 \x01(\x0e\x32\x1f.eigr.functions.protocol.Status\x12\x0f\n\x07message\x18\x02 \x01(\t*=\n\x06Status\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x06\n\x02OK\x10\x01\x12\x13\n\x0f\x41\x43TOR_NOT_FOUND\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x42O\n\x1aio.eigr.functions.protocolZ1github.com/eigr/go-support/eigr/protocol;protocolb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'eigr.functions.protocol.actors.protocol_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\032io.eigr.functions.protocolZ1github.com/eigr/go-support/eigr/protocol;protocol'
    _CONTEXT_METADATAENTRY._options = None
    _CONTEXT_METADATAENTRY._serialized_options = b'8\001'
    _CONTEXT_TAGSENTRY._options = None
    _CONTEXT_TAGSENTRY._serialized_options = b'8\001'
    _INVOCATIONREQUEST_METADATAENTRY._options = None
    _INVOCATIONREQUEST_METADATAENTRY._serialized_options = b'8\001'
    _globals['_STATUS']._serialized_start = 3357
    _globals['_STATUS']._serialized_end = 3418
    _globals['_CONTEXT']._serialized_start = 146
    _globals['_CONTEXT']._serialized_end = 522
    _globals['_CONTEXT_METADATAENTRY']._serialized_start = 430
    _globals['_CONTEXT_METADATAENTRY']._serialized_end = 477
    _globals['_CONTEXT_TAGSENTRY']._serialized_start = 479
    _globals['_CONTEXT_TAGSENTRY']._serialized_end = 522
    _globals['_NOOP']._serialized_start = 524
    _globals['_NOOP']._serialized_end = 530
    _globals['_JSONTYPE']._serialized_start = 532
    _globals['_JSONTYPE']._serialized_end = 559
    _globals['_REGISTRATIONREQUEST']._serialized_start = 562
    _globals['_REGISTRATIONREQUEST']._serialized_end = 710
    _globals['_REGISTRATIONRESPONSE']._serialized_start = 713
    _globals['_REGISTRATIONRESPONSE']._serialized_end = 847
    _globals['_SERVICEINFO']._serialized_start = 850
    _globals['_SERVICEINFO']._serialized_end = 1062
    _globals['_SPAWNREQUEST']._serialized_start = 1064
    _globals['_SPAWNREQUEST']._serialized_end = 1135
    _globals['_SPAWNRESPONSE']._serialized_start = 1137
    _globals['_SPAWNRESPONSE']._serialized_end = 1208
    _globals['_PROXYINFO']._serialized_start = 1210
    _globals['_PROXYINFO']._serialized_end = 1328
    _globals['_SIDEEFFECT']._serialized_start = 1330
    _globals['_SIDEEFFECT']._serialized_end = 1403
    _globals['_BROADCAST']._serialized_start = 1406
    _globals['_BROADCAST']._serialized_end = 1558
    _globals['_PIPE']._serialized_start = 1560
    _globals['_PIPE']._serialized_end = 1602
    _globals['_FORWARD']._serialized_start = 1604
    _globals['_FORWARD']._serialized_end = 1649
    _globals['_WORKFLOW']._serialized_start = 1652
    _globals['_WORKFLOW']._serialized_end = 1882
    _globals['_INVOCATIONREQUEST']._serialized_start = 1885
    _globals['_INVOCATIONREQUEST']._serialized_end = 2372
    _globals['_INVOCATIONREQUEST_METADATAENTRY']._serialized_start = 430
    _globals['_INVOCATIONREQUEST_METADATAENTRY']._serialized_end = 477
    _globals['_ACTORINVOCATION']._serialized_start = 2375
    _globals['_ACTORINVOCATION']._serialized_end = 2682
    _globals['_ACTORINVOCATIONRESPONSE']._serialized_start = 2685
    _globals['_ACTORINVOCATIONRESPONSE']._serialized_end = 2981
    _globals['_INVOCATIONRESPONSE']._serialized_start = 2984
    _globals['_INVOCATIONRESPONSE']._serialized_end = 3272
    _globals['_REQUESTSTATUS']._serialized_start = 3274
    _globals['_REQUESTSTATUS']._serialized_end = 3355
# @@protoc_insertion_point(module_scope)
