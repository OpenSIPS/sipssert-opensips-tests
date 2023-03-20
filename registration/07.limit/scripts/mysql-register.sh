#!/bin/bash

l=$(mysql opensips -Nse 'select count(*) from location')
[ "$l" == "$1" ] && exit 0
echo "ERROR: number of contacts is $l (expected $1)"
exit 1
