
#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

function fetch() {
  local local=$1
  local tag=$2
  local path=$3
  mkdir -p $(dirname $local)
  curl -o ${local} https://raw.githubusercontent.com/eigr-labs/spawn/${tag}${path}
}

tag=$1

# Spawn protocol
#fetch "cloudstate/entity.proto" $tag "/protocols/protocol/cloudstate/entity.proto"
