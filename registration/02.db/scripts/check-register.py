from opensips.mi import OpenSIPSMI
import sys
import os

mi_type = os.getenv('MI_TYPE', 'http')
mi_ip = os.getenv('MI_IP', '127.0.0.1')
mi_port = os.getenv('MI_PORT', '8888')

if mi_type == 'http':
    handler = OpenSIPSMI(conn='http', url='http://{}:{}/mi'.format(mi_ip, mi_port))
elif mi_type == 'datagram':
    handler = OpenSIPSMI(conn='datagram', datagram_ip=mi_ip, datagram_port=mi_port)
else:
    sys.exit(1)

unregister = True if len(sys.argv) > 1 and sys.argv[1] == "unregister" else False

out = handler.execute("ul_dump")
l = len(out['Domains'][0]['AORs'])

if unregister:
    if l == 0:
        sys.exit(0)
    if l != 1:
        sys.exit(1)
    if out['Domains'][0]['AORs'][0]['Contacts'][0]['Expires'] != "deleted":
        sys.exit(2)
else:
    if l != 1:
        sys.exit(1)
sys.exit(0)
