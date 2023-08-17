#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# follow the basic steps here: https://grpc.io/docs/tutorials/basic/python/
protoc -I ../protobuf/ --python_out=../spawn eigr/functions/protocol/actors/actor.proto
protoc -I ../protobuf/ --python_out=../spawn eigr/functions/protocol/actors/protocol.proto

#protoc -I ../example/protobuf/ --python_out=../example ../example/protobuf/domain/domain.proto
