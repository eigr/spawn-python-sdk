#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# follow the basic steps here: https://grpc.io/docs/tutorials/basic/python/
python3 -m grpc_tools.protoc -I ../protobuf/ --python_out=../spawn eigr/actor.proto
python3 -m grpc_tools.protoc -I ../protobuf/ --python_out=../spawn eigr/protocol.proto

python3 -m grpc_tools.protoc -I ../example/protobuf/ --python_out=../example ../example/protobuf/domain/domain.proto
