#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM acc WHERE duration > 0")
if [ "$l" = "1" ]; then
	exit 0
fi

exit 1
