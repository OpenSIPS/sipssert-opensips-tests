"""Check that a live seizure prevents seizure of a different idle appearance."""
import json
import os
import sys

from opensips.mi import OpenSIPSMI

host = os.getenv("MI_IP", "127.0.0.1")
handler = OpenSIPSMI(conn="http", url="http://{}:{}/mi".format(
    host, os.getenv("MI_PORT", "8888")))
line_uri = "sip:shared-line@" + host
result = handler.execute("list_lines")
print(json.dumps(result), flush=True)
lines = [line for line in result["lines"] if line["line"] == line_uri]
if len(lines) != 1:
    raise RuntimeError("Expected exactly one record for " + line_uri)
line = lines[0]
states = {idx["index"]: idx["state"] for idx in line["indexes"]}
if states != {1: "seized", 2: "idle"}:
    raise RuntimeError("Expected appearance 1 seized and appearance 2 idle: " + repr(line))
if line["seize_state"] != 1 or line["seize_expires"] <= 0:
    raise RuntimeError("Expected a live seizure of appearance 1: " + repr(line))
print("PASS ({}): appearance 1 seized with live expiry; appearance 2 idle".format(sys.argv[1]))
