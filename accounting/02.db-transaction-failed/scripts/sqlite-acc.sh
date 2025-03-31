#!/usr/bin/env sh

n1=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM acc WHERE sip_code='486'")
n2=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT COUNT(*) FROM missed_calls WHERE sip_code='486'")
if [[ "$n1" == "1" && "$n2" == "1" ]]; then
	exit 0
fi

exit 1
