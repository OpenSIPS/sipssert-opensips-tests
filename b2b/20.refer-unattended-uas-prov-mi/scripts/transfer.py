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

if len(sys.argv) < 3:
    print("Usage: {} URI entity".format(sys.argv[0]))
    sys.exit(-1)

uri = sys.argv[1]
entity = sys.argv[2]
prov_media_uri = sys.argv[3] if len(sys.argv) > 3 else None

dialogs = handler.execute("b2b_list")
logic = dialogs['Tuples'][0]['key'] # we are only interested in the first dialog
params = {'dialog_id':logic, 'new_uri':uri, 'flag':entity}
if prov_media_uri:
    params['prov_media_uri'] = prov_media_uri
handler.execute("b2b_bridge", params)
