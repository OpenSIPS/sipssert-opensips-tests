#!/bin/bash

l=$(mysql opensips -Nse 'select attr from acc where id = 1')

if [[ $l =~ "identity_header" ]]; then
	echo "$l"
	exit 0
else
	echo "ERROR: identity_header isn't in attr $l"
	exit 1
fi



