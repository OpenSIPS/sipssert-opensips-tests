# nats_reg_list must list the AoR the REGISTER saved, with one active contact
from opensips.mi import OpenSIPSMI
import os
import sys

mi = OpenSIPSMI(conn='http', url='http://{}:{}/mi'.format(
    os.getenv('MI_IP', '127.0.0.1'), os.getenv('MI_PORT', '8888')))
user = sys.argv[1]
out = mi.execute("nats_reg_list")
print(out)
ok = [a for a in out.get('aors', [])
      if a.get('aor', '').startswith(user + '@')
      and a.get('contacts') == 1 and a.get('active') == 1]
sys.exit(0 if ok and out.get('matched') == len(out.get('aors', [])) else 1)
