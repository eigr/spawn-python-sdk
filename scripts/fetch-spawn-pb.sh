
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

#fetch "cloudstate/event_sourced.proto" $tag "/protocols/protocol/cloudstate/event_sourced.proto"
#fetch "cloudstate/action.proto" $tag "/protocols/protocol/cloudstate/action.proto"
#fetch "cloudstate/crdt.proto" $tag "/protocols/protocol/cloudstate/crdt.proto"

# TCK shopping cart example
#fetch "cloudstate/test/shoppingcart/shoppingcart.proto" $tag "/protocols/example/shoppingcart/shoppingcart.proto"
#fetch "cloudstate/test/shoppingcart/persistence/domain.proto" $tag "/protocols/example/shoppingcart/persistence/domain.proto"

# Cloudstate frontend
#fetch "cloudstate/entity_key.proto" $tag "/protocols/frontend/cloudstate/entity_key.proto"
#fetch "cloudstate/eventing.proto" $tag  "/protocols/frontend/cloudstate/eventing.proto"

# dependencies
#fetch "protobuf/lib/google/api/annotations.proto" $tag "/protocols/frontend/google/api/annotations.proto"
#fetch "protobuf/lib/google/api/http.proto" $tag "/protocols/frontend/google/api/http.proto"
#fetch "protobuf/lib/google/api/httpbody.proto" $tag "/protocols/frontend/google/api/httpbody.proto"