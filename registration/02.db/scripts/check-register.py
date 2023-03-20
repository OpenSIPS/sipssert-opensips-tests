from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

unregister = True if len(sys.argv) > 1 and sys.argv[1] == "unregister" else False

out = handler.mi("ul_dump")
l = len(out['Domains'][0]['AORs'])

if unregister:
    if l == 0:
        sys.exit(0)
    if l != 1:
        sys.exit(1)
    if out['Domains'][0]['AORs'][0]['Contacts'][0]['Expires'] != "deleted":
        sys.exit(2)
else:
    if l != 1:
        sys.exit(1)
sys.exit(0)
