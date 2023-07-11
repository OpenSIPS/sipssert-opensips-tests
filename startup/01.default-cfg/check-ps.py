from opensipscli import cli
import sys

handler = cli.OpenSIPSCLI()

out = handler.mi("ps")

if out:
	sys.exit(0)
else:
	sys.exit(1)