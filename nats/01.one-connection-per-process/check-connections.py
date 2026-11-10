# With event_nats, cachedb_nats and nats_consumer loaded, every OpenSIPS
# process shares ONE NATS connection (nats.so's pool): the broker sees at
# most one client connection per process from the OpenSIPS address.
from opensips.mi import OpenSIPSMI
import json
import os
import sys
import urllib.request

mi = OpenSIPSMI(conn='http', url='http://{}:{}/mi'.format(
    os.getenv('MI_IP', '127.0.0.1'), os.getenv('MI_PORT', '8888')))
nats_ip, osips_ip = sys.argv[1], sys.argv[2]
procs = mi.execute("ps")["Processes"]
connz = json.load(urllib.request.urlopen(
    "http://{}:8222/connz?limit=1024".format(nats_ip), timeout=5))
mine = [c for c in connz.get("connections", []) if c.get("ip") == osips_ip]
print("processes:", len(procs), "connections from OpenSIPS:", len(mine))
sys.exit(0 if 0 < len(mine) <= len(procs) else 1)
