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

if len(sys.argv) == 1:
    port = None
else:
    port = ":{}".format(sys.argv[1])

aors = handler.execute("ul_dump")['Domains'][0]['AORs']
l = len(aors)
if l != 1:
    if l == 0 and not port:
        sys.exit(0)
    print("Unexpected number of AORs: {}!".format(l))
    sys.exit(1)
contacts = aors[0]['Contacts']
if not port:
    expires = contacts[0]['Expires']
    if expires != "expired":
        print("contact still valid, expires {}!".format(expires))
        sys.exit(2)
    sys.exit(0)
if len(contacts) != 1:
    print("Unexpected number of contacts: {}!".format(len(contacts)))
    sys.exit(3)
contact = contacts[0]['Contact']
if contact.endswith(port):
    sys.exit(0)
print("Contact {} does not end with {}".format(contact, port))
sys.exit(1)
