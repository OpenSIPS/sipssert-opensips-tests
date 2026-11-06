"""Check that an idle appearance can be seized alongside an active call."""
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
    idle = [idx for idx in line["indexes"] if idx["index"] == 2]
    expected_state = "idle" if phase == "before" else "seized"
    if len(idle) != 1 or idle[0]["state"] != expected_state:
        raise RuntimeError("Unexpected appearance 2 state: " + repr(line))
    if phase == "after":
        if line["seize_state"] != 2 or line["seize_expires"] <= 0:
            raise RuntimeError("Appearance 2 must have a live seizure: " + repr(line))
        break
    if line["seize_state"] != 1:
        raise RuntimeError("Expected the original seizure: " + repr(line))
    if line["seize_expires"] < 0:
        break
    if phase != "before" or time.monotonic() >= deadline:
        raise RuntimeError("Expected expired seizure: " + repr(line))
    time.sleep(.2)

print("PASS ({}): appearance 1 active, appearance 2 {}".format(
    phase, "idle" if phase == "before" else "seized"))
