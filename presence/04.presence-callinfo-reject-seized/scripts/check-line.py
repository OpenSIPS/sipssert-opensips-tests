"""Check same-index exclusion and independent seizure lifetimes."""
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
indexes = {idx["index"]: idx for idx in line["indexes"]}
# The previous image reports one seizure on the line; the new image reports
# seizure data per index. Normalize only the old representation.
if "seize_state" in line:
    for number, item in indexes.items():
        item["seize_state"] = number if line["seize_state"] == number else 0
        item["seize_expires"] = line["seize_expires"] if line["seize_state"] == number else 0
phase = sys.argv[1]
states = {idx: item["state"] for idx, item in indexes.items()}
expected = {1: "seized", 2: "seized" if phase == "parallel" else "idle"}
if states != expected:
    raise RuntimeError("Unexpected appearance states: " + repr(line))
if indexes[1]["seize_state"] != 1 or indexes[1]["seize_expires"] <= 0:
    raise RuntimeError("Appearance 1 must retain its live seizure: " + repr(line))
if phase == "parallel":
    if indexes[2]["seize_state"] != 2 or indexes[2]["seize_expires"] <= 0:
        raise RuntimeError("Both appearances must have live seizures: " + repr(line))
elif indexes[2]["seize_state"] != 0 or indexes[2]["seize_expires"] != 0:
    raise RuntimeError("Appearance 2 must be released: " + repr(line))
print("PASS ({}): independent appearance seizures".format(phase))
