#!/bin/bash

l=$(mysql opensips -Nse 'select count(*) from location')
if [ "$1" = "expired" ]; then
	[ "$l" == "0" ] && exit 0
else
	[ "$l" == "1" ] && exit 0
fi
echo "ERROR: number of contacts is $l"
exit 1
