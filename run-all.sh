#!/bin/bash

yaml_list() {
	test -n "${BASH_SOURCE[0]}" && DIR="$(dirname "${BASH_SOURCE[0]}")" || DIR=.
	python3 -c "import yaml;print(' '.join(yaml.safe_load(open('$DIR/environment.yml'))['$1']))"
}

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:-$(yaml_list params)}

SETS=${SETS:-$(yaml_list test_set)}

sipssert \
	$PARAMS \
	$SETS \
	$@
