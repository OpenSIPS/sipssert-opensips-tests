"""A competing SUBSCRIBE must not replace or renew a live seizure."""
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
    raise RuntimeError("Expected exactly one shared line: " + repr(result))
line = lines[0]
indexes = line["indexes"]
if len(indexes) != 1 or indexes[0]["index"] != 1 or indexes[0]["state"] != "seized":
    raise RuntimeError("Expected only appearance 1, still seized: " + repr(line))
seizure = indexes[0] if "seize_expires" in indexes[0] else line
if seizure["seize_state"] != 1 or seizure["seize_expires"] <= 0:
    raise RuntimeError("Expected the original live seizure: " + repr(line))
# The owner requests 30 seconds; the contender requests 10. A positive expiry
# alone would miss an implementation which rejects but renews the seizure.
if seizure["seize_expires"] <= 10:
    raise RuntimeError("Original seizure was replaced or test setup was too slow: " + repr(line))
print("PASS ({}): appearance 1 remains seized with the owner's expiry".format(sys.argv[1]))
