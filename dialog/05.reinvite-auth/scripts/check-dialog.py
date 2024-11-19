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
    sys.exit(-1)

dialogs = handler.execute("dlg_list")['Dialogs']
if sys.argv[1] == "active":
    out = handler.execute("get_statistics", {"statistics" : ["active_dialogs"]})
    if out["dialog:active_dialogs"] != 1:
        print("Active dialogs: {}".format(out["dialog:active_dialogs"]))
        sys.exit(11)
    if len(dialogs) != 1:
        print("Number of dialogs: {}".format(len(dialogs)))
        sys.exit(12)
elif sys.argv[1] == "deleted":
    out = handler.execute("get_statistics", {"statistics" : ["dialog:"]})
    if out["dialog:active_dialogs"] != 0:
        print("Active dialogs: {}".format(out["dialog:active_dialogs"]))
        sys.exit(21)
    if len(dialogs) != 0:
        if len(dialogs) > 1:
            print("Too many dialogs: {}".format(len(dialogs)))
            sys.exit(22)
        if dialogs[0]['state'] != 5:
            print("Bad state {} for dialog".format(dialogs[0]['state']))
            sys.exit(23)
    if out["dialog:failed_dialogs"] != 0:
        print("Failed dialogs: {}".format(out["dialog:failed_dialogs"]))
        sys.exit(24)
    if out["dialog:expired_dialogs"] != 0:
        print("Expired dialogs: {}".format(out["dialog:expired_dialogs"]))
        sys.exit(25)
    if out["dialog:processed_dialogs"] < 1:
        print("Processed dialogs: {}".format(out["dialog:processed_dialogs"]))
        sys.exit(26)
sys.exit(0)
