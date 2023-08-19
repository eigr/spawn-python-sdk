# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eigr/functions/protocol/actors/actor.proto
"""Generated protocol buffer code."""
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n*eigr/functions/protocol/actors/actor.proto\x12\x1e\x65igr.functions.protocol.actors\x1a\x19google/protobuf/any.proto\"\xa6\x01\n\x08Registry\x12\x44\n\x06\x61\x63tors\x18\x01 \x03(\x0b\x32\x34.eigr.functions.protocol.actors.Registry.ActorsEntry\x1aT\n\x0b\x41\x63torsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.eigr.functions.protocol.actors.Actor:\x02\x38\x01\"W\n\x0b\x41\x63torSystem\x12\x0c\n\x04name\x18\x01 \x01(\t\x12:\n\x08registry\x18\x02 \x01(\x0b\x32(.eigr.functions.protocol.actors.Registry\"g\n\x15\x41\x63torSnapshotStrategy\x12\x42\n\x07timeout\x18\x01 \x01(\x0b\x32/.eigr.functions.protocol.actors.TimeoutStrategyH\x00\x42\n\n\x08strategy\"k\n\x19\x41\x63torDeactivationStrategy\x12\x42\n\x07timeout\x18\x01 \x01(\x0b\x32/.eigr.functions.protocol.actors.TimeoutStrategyH\x00\x42\n\n\x08strategy\"\"\n\x0fTimeoutStrategy\x12\x0f\n\x07timeout\x18\x01 \x01(\x03\"\x16\n\x06\x41\x63tion\x12\x0c\n\x04name\x18\x01 \x01(\t\"[\n\x10\x46ixedTimerAction\x12\x0f\n\x07seconds\x18\x01 \x01(\x05\x12\x36\n\x06\x61\x63tion\x18\x02 \x01(\x0b\x32&.eigr.functions.protocol.actors.Action\"\xa2\x01\n\nActorState\x12\x42\n\x04tags\x18\x01 \x03(\x0b\x32\x34.eigr.functions.protocol.actors.ActorState.TagsEntry\x12#\n\x05state\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x90\x01\n\x08Metadata\x12\x15\n\rchannel_group\x18\x01 \x01(\t\x12@\n\x04tags\x18\x02 \x03(\x0b\x32\x32.eigr.functions.protocol.actors.Metadata.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xaf\x02\n\rActorSettings\x12\x32\n\x04kind\x18\x01 \x01(\x0e\x32$.eigr.functions.protocol.actors.Kind\x12\x10\n\x08stateful\x18\x02 \x01(\x08\x12P\n\x11snapshot_strategy\x18\x03 \x01(\x0b\x32\x35.eigr.functions.protocol.actors.ActorSnapshotStrategy\x12X\n\x15\x64\x65\x61\x63tivation_strategy\x18\x04 \x01(\x0b\x32\x39.eigr.functions.protocol.actors.ActorDeactivationStrategy\x12\x15\n\rmin_pool_size\x18\x05 \x01(\x05\x12\x15\n\rmax_pool_size\x18\x06 \x01(\x05\"7\n\x07\x41\x63torId\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06system\x18\x02 \x01(\t\x12\x0e\n\x06parent\x18\x03 \x01(\t\"\xf6\x02\n\x05\x41\x63tor\x12\x33\n\x02id\x18\x01 \x01(\x0b\x32\'.eigr.functions.protocol.actors.ActorId\x12\x39\n\x05state\x18\x02 \x01(\x0b\x32*.eigr.functions.protocol.actors.ActorState\x12:\n\x08metadata\x18\x06 \x01(\x0b\x32(.eigr.functions.protocol.actors.Metadata\x12?\n\x08settings\x18\x03 \x01(\x0b\x32-.eigr.functions.protocol.actors.ActorSettings\x12\x37\n\x07\x61\x63tions\x18\x04 \x03(\x0b\x32&.eigr.functions.protocol.actors.Action\x12G\n\rtimer_actions\x18\x05 \x03(\x0b\x32\x30.eigr.functions.protocol.actors.FixedTimerAction*E\n\x04Kind\x12\x0f\n\x0bUNKNOW_KIND\x10\x00\x12\t\n\x05NAMED\x10\x01\x12\n\n\x06UNAMED\x10\x02\x12\n\n\x06POOLED\x10\x03\x12\t\n\x05PROXY\x10\x04\x42R\n!io.eigr.functions.protocol.actorsZ-github.com/eigr/go-support/eigr/actors;actorsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'spawn.eigr.functions.protocol.actors.actor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n!io.eigr.functions.protocol.actorsZ-github.com/eigr/go-support/eigr/actors;actors'
    _REGISTRY_ACTORSENTRY._options = None
    _REGISTRY_ACTORSENTRY._serialized_options = b'8\001'
    _ACTORSTATE_TAGSENTRY._options = None
    _ACTORSTATE_TAGSENTRY._serialized_options = b'8\001'
    _METADATA_TAGSENTRY._options = None
    _METADATA_TAGSENTRY._serialized_options = b'8\001'
    _globals['_KIND']._serialized_start = 1782
    _globals['_KIND']._serialized_end = 1851
    _globals['_REGISTRY']._serialized_start = 106
    _globals['_REGISTRY']._serialized_end = 272
    _globals['_REGISTRY_ACTORSENTRY']._serialized_start = 188
    _globals['_REGISTRY_ACTORSENTRY']._serialized_end = 272
    _globals['_ACTORSYSTEM']._serialized_start = 274
    _globals['_ACTORSYSTEM']._serialized_end = 361
    _globals['_ACTORSNAPSHOTSTRATEGY']._serialized_start = 363
    _globals['_ACTORSNAPSHOTSTRATEGY']._serialized_end = 466
    _globals['_ACTORDEACTIVATIONSTRATEGY']._serialized_start = 468
    _globals['_ACTORDEACTIVATIONSTRATEGY']._serialized_end = 575
    _globals['_TIMEOUTSTRATEGY']._serialized_start = 577
    _globals['_TIMEOUTSTRATEGY']._serialized_end = 611
    _globals['_ACTION']._serialized_start = 613
    _globals['_ACTION']._serialized_end = 635
    _globals['_FIXEDTIMERACTION']._serialized_start = 637
    _globals['_FIXEDTIMERACTION']._serialized_end = 728
    _globals['_ACTORSTATE']._serialized_start = 731
    _globals['_ACTORSTATE']._serialized_end = 893
    _globals['_ACTORSTATE_TAGSENTRY']._serialized_start = 850
    _globals['_ACTORSTATE_TAGSENTRY']._serialized_end = 893
    _globals['_METADATA']._serialized_start = 896
    _globals['_METADATA']._serialized_end = 1040
    _globals['_METADATA_TAGSENTRY']._serialized_start = 850
    _globals['_METADATA_TAGSENTRY']._serialized_end = 893
    _globals['_ACTORSETTINGS']._serialized_start = 1043
    _globals['_ACTORSETTINGS']._serialized_end = 1346
    _globals['_ACTORID']._serialized_start = 1348
    _globals['_ACTORID']._serialized_end = 1403
    _globals['_ACTOR']._serialized_start = 1406
    _globals['_ACTOR']._serialized_end = 1780
# @@protoc_insertion_point(module_scope)
