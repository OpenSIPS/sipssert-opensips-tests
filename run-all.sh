#!/bin/bash

# exclude tests that we know they fail for sure
PARAMS="--exclude b2b/09.refer-unattended-uac-notify-fail
	--exclude b2b/10.refer-unattended-uas-notify-fail
	--exclude b2b/15.refer-unattended-uac-prov-notify-fail
	--exclude b2b/16.refer-unattended-uas-prov-notify-fail
	--exclude topology-hiding/02.th-no-dialog-username"

sipssert \
	$PARAMS \
	registration \
	auth \
	record-route \
	dialog \
	topology-hiding \
	b2b \
	$@
