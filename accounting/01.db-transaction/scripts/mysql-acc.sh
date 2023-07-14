#!/bin/bash

l=$(mysql opensips -Nse 'select count(*) from acc where sip_code="200"')
if [ "$l" = "1" ]; then
	exit 0
fi

exit 1
