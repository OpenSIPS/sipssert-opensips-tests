#!/usr/bin/env sh

l=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM location")
[ "$l" == "$1" ] && exit 0
echo "ERROR: number of contacts is $l (expected $1)"
exit 1
