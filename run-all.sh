#!/bin/bash

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:---exclude topology-hiding/02.th-no-dialog-username}

SETS=${SETS:-startup
	registration \
	auth \
	record-route \
	dialog \
	topology-hiding \
	b2b \
	uac-auth \
	stir-shaken \
	accounting \
	presence \
	permissions}

sipssert \
	$PARAMS \
	$SETS \
	$@
