from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

expired = True if len(sys.argv) > 1 and sys.argv[1] == "expired" else False

out = handler.mi("ul_dump")
l = len(out['Domains'][0]['AORs'])

if expired:
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
            sys.exit(2)
    except ValueError:
        if expires != "expired":
            print("Expires is {}".format(expires))
            sys.exit(3)
else:
    if l != 1:
        print("Number of contacts is {}".format(l))
        sys.exit(1)
sys.exit(0)
