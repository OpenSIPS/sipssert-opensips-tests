#!/bin/bash

l=$(mysql opensips -Nse 'select count(*) from acc')
if [ "$l" = "1" ]; then
	exit 0
fi
echo "ERROR: number of dialogs is $l"
exit 1
