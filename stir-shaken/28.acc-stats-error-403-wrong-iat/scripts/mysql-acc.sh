#!/bin/bash

l=$(mysql opensips -Nse 'select attr from acc where id = 1')

if [[ $l =~ "identity_header" ]]; then
	echo "$l"
	exit 0
else
	echo "ERROR: identity_header isn't in attr ($l)"
	echo "ERROR: full acc:"
	l2=$(mysql opensips -Nse 'select * from acc where id = 1')
	echo "$l2"
	exit 1
fi



