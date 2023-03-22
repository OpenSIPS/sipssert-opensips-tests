from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

if len(sys.argv) < 1:
    sys.exit(-1)

dialogs = handler.mi("dlg_list")['Dialogs']
if sys.argv[1] == "active":
    out = handler.mi("get_statistics", {"statistics" : ["active_dialogs"]})
    if out["dialog:active_dialogs"] != 1:
        print("Active dialogs: {}".format(out["dialog:active_dialogs"]))
        sys.exit(11)
    if len(dialogs) != 1:
        print("Number of dialogs: {}".format(len(dialogs)))
        sys.exit(12)
elif sys.argv[1] == "expired":
    out = handler.mi("get_statistics", {"statistics" : ["dialog:"]})
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
    if out["dialog:expired_dialogs"] < 1:
        print("Expired dialogs: {}".format(out["dialog:expired_dialogs"]))
        sys.exit(25)
    if out["dialog:processed_dialogs"] < 1:
        print("Processed dialogs: {}".format(out["dialog:processed_dialogs"]))
        sys.exit(26)
sys.exit(0)
