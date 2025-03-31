#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM dialog")
if [ "$1" = "active" ]; then
	[ "$l" == "1" ] && exit 0
else
	[ "$l" == "0" ] && exit 0
fi
echo "ERROR: number of dialogs is $l"
exit 1
