#!/bin/bash

DIR="$( dirname "${BASH_SOURCE[0]}")"
yaml_list() {
	python3 -c "import yaml;print(' '.join(yaml.safe_load(open('$DIR/matrix.yml'))['$1']))"
}

# exclude tests that we know they fail for sure
PARAMS=${PARAMS:-$(yaml_list params)}

SETS=${SETS:-$(yaml_list scenario)}

sipssert \
	$PARAMS \
	$SETS \
	$@
