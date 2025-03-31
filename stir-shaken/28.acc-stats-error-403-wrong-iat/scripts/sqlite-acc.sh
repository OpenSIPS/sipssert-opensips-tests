#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT attr FROM acc WHERE id = 1")

echo "$l" | grep -q "identity_header"
if [ $? -eq 0 ]; then
	echo "$l"
	exit 0
else
	echo "ERROR: identity_header isn't in attr ($l)"
	echo "ERROR: full acc:"
	l2=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT * FROM acc WHERE id = 1")
	echo "$l2"
	exit 1
fi



