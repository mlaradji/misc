#!/bin/bash

OS="$4"
container="$1"
pool="$2"
ipaddress="$3"

lxc init "$OS" "$container" -s "$pool"
#lxc stop "$container"
#sleep 10
lxc config set "$container" raw.lxc "lxc.net.0.ipv4.address = $ipaddress"
#lxc start "$container" &

exit 0
