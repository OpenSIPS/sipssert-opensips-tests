#!/bin/bash

yaml_list() {
	DIR="$(dirname -- "$(readlink "$0")")"
	python3 -c "import yaml;print(' '.join(yaml.safe_load(open('$DIR/environment.yml'))['$1']))"
}

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:-$(yaml_list params)}

SETS=${SETS:-$(yaml_list test_set)}

sipssert \
	$PARAMS \
	$SETS \
	$@
