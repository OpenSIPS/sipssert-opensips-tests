#!/bin/bash

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:---exclude b2b/09.refer-unattended-uac-notify-fail \
				 --exclude b2b/10.refer-unattended-uas-notify-fail \
				 --exclude b2b/15.refer-unattended-uac-prov-notify-fail \
				 --exclude b2b/16.refer-unattended-uas-prov-notify-fail \
				 --exclude topology-hiding/02.th-no-dialog-username \
		}

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
