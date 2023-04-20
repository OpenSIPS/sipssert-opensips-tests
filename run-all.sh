#!/bin/bash

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:---exclude topology-hiding/02.th-no-dialog-username}
SETS=${SETS:-registration \
	auth \
	record-route \
	dialog \
	topology-hiding \
	b2b}

sipssert \
	$PARAMS \
	$SETS \
	$@
