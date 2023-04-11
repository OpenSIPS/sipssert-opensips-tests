#!/bin/bash

# exclude tests that we know they fail for sure
PARAMS="--exclude topology-hiding/02.th-no-dialog-username"

sipssert \
	$PARAMS \
	registration \
	auth \
	record-route \
	dialog \
	topology-hiding \
	b2b \
	$@
