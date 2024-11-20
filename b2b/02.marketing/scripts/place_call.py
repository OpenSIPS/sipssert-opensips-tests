from opensips.mi import OpenSIPSMI, OpenSIPSMIException
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

if len(sys.argv) < 5:
    sys.exit(1)

try:
    handler.execute("b2b_trigger_scenario",
                    [sys.argv[1], sys.argv[2], sys.argv[3], [sys.argv[4]]])
except OpenSIPSMIException as e:
    print(e)
    sys.exit(1)
