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

if len(sys.argv[1]) < 1:
    print("Number of contacts not specified!")
    sys.exit(-1)
contacts = int(sys.argv[1])

aors = handler.execute("ul_dump")['Domains'][0]['AORs']
l = len(aors)
if l != 1:
    if l == 0 and contacts == 0:
        sys.exit(0)
    print("Unexpected number of AORs: {}!".format(l))
    sys.exit(1)
count = 0
for ct in aors[0]['Contacts']:
    expires = ct['Expires']
    try:
        expires = int(expires)
        if expires > 0:
            count += 1
    except ValueError:
        continue

if count != contacts:
    print("Expected contacts {} differs from the actual ones {}: {}".
            format(contacts, count, aors))
    sys.exit(contacts - count)
else:
    sys.exit(0)
