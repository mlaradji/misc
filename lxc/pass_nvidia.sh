#!/bin/bash

container=$1

# NVIDIA info
vendor_id=10de
product_id=1401

lxc stop $container
lxc config set $container nvidia.runtime true
lxc config device add $container gpu gpu vendorid=$vendor_id productid=$product_id
lxc start $container
