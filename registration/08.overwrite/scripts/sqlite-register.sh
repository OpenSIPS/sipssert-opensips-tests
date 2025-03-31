#!/usr/bin/env sh

ct=$(sqlite3 /var/lib/opensips/db_sqlite/opensips.db "SELECT contact FROM location")
if [ -z "$1" ]; then
	[ -z "$ct" ] && exit 0
	echo "ERROR: no contact expected, but got [$ct]"
	exit 1
fi
echo "Contact: $ct"
port="${ct##*:}"
echo "Port: $port"
[ "$port" == "$1" ] && exit 0
echo "ERROR: different contact port $port (expected $1)"
exit 1
