"""Check seizure expiry and preservation of the active appearance."""
import json
import os
import sys
import time

from opensips.mi import OpenSIPSMI

host = os.getenv("MI_IP", "127.0.0.1")
handler = OpenSIPSMI(conn="http", url="http://{}:{}/mi".format(
    host, os.getenv("MI_PORT", "8888")))
line_uri = "sip:shared-line@" + host
phase = sys.argv[1]
deadline = time.monotonic() + 5

while True:
    result = handler.execute("list_lines")
    print(json.dumps(result), flush=True)
    lines = [line for line in result["lines"] if line["line"] == line_uri]
    if len(lines) != 1:
        raise RuntimeError("Expected exactly one record for " + line_uri)
    line = lines[0]
    indexes = [idx for idx in line["indexes"] if idx["index"] == 1]
    if len(indexes) != 1 or indexes[0]["state"] != "active":
        raise RuntimeError("Appearance 1 must remain active: " + repr(line))
    if line["seize_state"] != 1:
        raise RuntimeError("Expected the original seizure: " + repr(line))
    if line["seize_expires"] < 0:
        break
    if phase != "before" or time.monotonic() >= deadline:
        raise RuntimeError("Expected expired seizure: " + repr(line))
    time.sleep(.2)

print("PASS ({}): appearance 1 active, original seizure expired".format(phase))
