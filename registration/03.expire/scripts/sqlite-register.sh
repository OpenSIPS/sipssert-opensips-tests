#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM location")
if [ "$1" = "expired" ]; then
	[ "$l" == "0" ] && exit 0
else
	[ "$l" == "1" ] && exit 0
fi
echo "ERROR: number of contacts is $l"
exit 1
