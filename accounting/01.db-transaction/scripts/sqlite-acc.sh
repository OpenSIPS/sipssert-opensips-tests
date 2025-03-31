#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM acc WHERE sip_code='200'")
if [ "$l" = "1" ]; then
	exit 0
fi

exit 1
