from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

if len(sys.argv) < 1:
    print("no action specified")
    sys.exit(-1)
action = sys.argv[1]

out = handler.mi("ul_dump")
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
