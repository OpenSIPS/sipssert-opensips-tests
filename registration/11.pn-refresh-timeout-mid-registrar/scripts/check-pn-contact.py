from opensips.mi import OpenSIPSMI
import os
import sys

mi_type = os.getenv('MI_TYPE', 'http')
mi_ip = os.getenv('MI_IP', '127.0.0.1')
mi_port = os.getenv('MI_PORT', '8888')

if mi_type == 'http':
    handler = OpenSIPSMI(conn='http', url='http://{}:{}/mi'.format(mi_ip, mi_port))
elif mi_type == 'datagram':
    handler = OpenSIPSMI(conn='datagram', datagram_ip=mi_ip, datagram_port=mi_port)
else:
    sys.exit(1)

out = handler.execute("ul_dump")
print(out)

try:
    aors = out['Domains'][0]['AORs']
    contacts = aors[0]['Contacts']
except (KeyError, IndexError):
    sys.exit(1)

if len(aors) != 1 or len(contacts) != 1:
    sys.exit(1)

contact = contacts[0]

if int(contact.get('Flags', 0)) != 4:
    sys.exit(1)

if 'pn-provider=fcm' not in contact.get('Contact', ''):
    sys.exit(1)

sys.exit(0)
