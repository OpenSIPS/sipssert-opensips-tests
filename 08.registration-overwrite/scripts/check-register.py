from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

if len(sys.argv) == 1:
    port = None
else:
    port = ":{}".format(sys.argv[1])

aors = handler.mi("ul_dump")['Domains'][0]['AORs']
l = len(aors)
if l != 1:
    if l == 0 and not port:
        sys.exit(0)
    print("Unexpected number of AORs: {}!".format(l))
    sys.exit(1)
contacts = aors[0]['Contacts']
if not port:
    expires = contacts[0]['Expires']
    if expires != "expired":
        print("contact still valid, expires {}!".format(expires))
        sys.exit(2)
    sys.exit(0)
if len(contacts) != 1:
    print("Unexpected number of contacts: {}!".format(len(contacts)))
    sys.exit(3)
contact = contacts[0]['Contact']
if contact.endswith(port):
    sys.exit(0)
print("Contact {} does not end with {}".format(contact, port))
sys.exit(1)
