from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

if len(sys.argv) < 3:
    print("Usage: {} URI entity".format(sys.argv[0]))
    sys.exit(-1)

uri = sys.argv[1]
entity = sys.argv[2]
prov_media_uri = sys.argv[3] if len(sys.argv) > 3 else None

dialogs = handler.mi("b2b_list")
logic = dialogs['Tuples'][0]['key'] # we are only interested in the first dialog
params = {'dialog_id':logic, 'new_uri':uri, 'flag':entity}
if prov_media_uri:
    params['prov_media_uri'] = prov_media_uri
handler.mi("b2b_bridge", params)
