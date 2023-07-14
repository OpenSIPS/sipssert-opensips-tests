#!/bin/bash

l=$(mysql opensips -Nse 'select count(*) from acc where duration > 0')
if [ "$l" = "1" ]; then
	exit 0
fi

exit 1
