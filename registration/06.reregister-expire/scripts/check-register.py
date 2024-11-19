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

if len(sys.argv) < 1:
    print("no action specified")
    sys.exit(-1)
action = sys.argv[1]

out = handler.execute("ul_dump")
l = len(out['Domains'][0]['AORs'])

if action == "expired":
    if l == 0:
        sys.exit(0)
    if l != 1:
        print("Number of contacts is {}".format(l))
        sys.exit(1)
    expires = out['Domains'][0]['AORs'][0]['Contacts'][0]['Expires']
    try:
        expires = int(expires)
        if expires != 0:
            print("Expires is {}".format(expires))
            sys.exit(3)
    except ValueError:
        if expires != "expired":
            print("Expires is {}".format(expires))
            sys.exit(4)
else:
    if l != 1:
        print("Number of contacts is {}".format(l))
        sys.exit(1)
    expires = out['Domains'][0]['AORs'][0]['Contacts'][0]['Expires']
    try:
        expires = int(expires)
        if action == "reregister":
            if expires > 5:
                print("Expires {} is higher than 5".format(expires))
                sys.exit(5)
        else:
            if expires < 30:
                print("Expires {} is too low".format(expires))
                sys.exit(6)
    except ValueError:
        print("Expires is {}".format(expires))
        sys.exit(2)
sys.exit(0)
