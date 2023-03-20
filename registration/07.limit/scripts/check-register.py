from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

if len(sys.argv[1]) < 1:
    print("Number of contacts not specified!")
    sys.exit(-1)
contacts = int(sys.argv[1])

aors = handler.mi("ul_dump")['Domains'][0]['AORs']
l = len(aors)
if l != 1:
    if l == 0 and contacts == 0:
        sys.exit(0)
    print("Unexpected number of AORs: {}!".format(l))
    sys.exit(1)
count = 0
for ct in aors[0]['Contacts']:
    expires = ct['Expires']
    try:
        expires = int(expires)
        if expires > 0:
            count += 1
    except ValueError:
        continue

if count != contacts:
    print("Expected contacts {} differs from the actual ones {}: {}".
            format(contacts, count, aors))
    sys.exit(contacts - count)
else:
    sys.exit(0)
