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

out = handler.execute("ps")

if out:
	sys.exit(0)
else:
	sys.exit(1)