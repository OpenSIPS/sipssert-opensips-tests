# Per-appearance line seizures

Requires OpenSIPS with per-appearance seizure tracking and the `list_lines` MI
command. This implements the policy permitted by BroadWorks SCA specification
R230, section 6.1.6: different appearances may be seized concurrently.

1. Prepare appearance 2 as idle, then seize appearance 1 for 30 seconds.
2. Try a competing seizure of appearance 1: expect 480.
3. Seize appearance 2 while appearance 1 is still seized: expect 200.
4. MI confirms both appearances have live seizures.
5. Refresh and release appearance 2. Each NOTIFY must identify appearance 2.
6. MI confirms appearance 2 is idle and appearance 1 retains its live seizure.

No call is established, so this isolates seizure handling from call state.
Test 06 separately isolates same-index rejection.

From the SIPssert tests repository:

```sh
sudo sipssert presence -t 04.presence-callinfo-reject-seized
```
