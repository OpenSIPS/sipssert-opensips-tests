#!/bin/bash

n1=$(mysql opensips -Nse 'select count(*) from acc where sip_code="486"')
n2=$(mysql opensips -Nse 'select count(*) from missed_calls where sip_code="486"')
if [[ "$n1" == "1" && "$n2" == "1" ]]; then
	exit 0
fi

exit 1
