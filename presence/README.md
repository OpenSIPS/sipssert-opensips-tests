# Presence tests

These scenarios check presence signaling and shared call appearance behavior.
Call-info scenarios use internal publishing and require the `list_lines` MI
command. Test 04 requires independent seizures for different appearance indexes.

| Test | Behavior checked | Expected result |
| --- | --- | --- |
| 01.presence | Basic PUBLISH / SUBSCRIBE / NOTIFY | Successful signaling sequence |
| 02.presence-callinfo-reject-active | Seize active index 1 after its seizure expires | 480; active state preserved |
| 03.presence-callinfo-idle | Seize idle index 2 while index 1 has an active call and an expired seizure | 200; index 1 stays active |
| 04.presence-callinfo-reject-seized | Seize index 2 while index 1 still has a live seizure, then refresh/release index 2 | 200; independent refresh/release; index 1 stays seized |
| 05.presence-callinfo-reject-held | Seize held index 1 after its seizure expires, then resume the original call | 480; held state preserved; resume succeeds |
| 06.presence-callinfo-reject-same-index | Competing subscription seizes index 1 while index 1 has a live seizure | 480; original seizure preserved |

Test 04 also checks same-index rejection before attempting index 2.
Test 06 isolates that rejection as a standalone test.
The call-info MI assertions accept both line-level and per-index seizure fields.

Run from the repository root:

```sh
sudo sipssert presence
```

Run one scenario with `-t`, for example:

```sh
sudo sipssert presence -t 06.presence-callinfo-reject-same-index
```
