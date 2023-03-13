#!/bin/bash

l=$(mysql opensips -Nse 'select * from location' | wc -l)
if [ "$1" = "unregister" ]; then
	[ "$l" == "0" ] && exit 0
else
	[ "$l" == "1" ] && exit 0
fi
echo "ERROR: length is $l"
exit 1
