# 17. Auto-Route Invalid thinfo

**What it tests:** Negative test — verifies that `topology_hiding_match()` correctly rejects a sequential request from the UAS where the **Route header** contains a `thinfo` parameter with **garbage/invalid encoded data**. This is the Route-header counterpart to test 13 (which tests invalid thinfo in the Contact/R-URI).

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the private network, UDP

## Call Flow

1. Normal INVITE/200/ACK setup succeeds.
2. UAS sends UPDATE with Route header: `<sip:10.100.20.40:5062;thinfo=GARBAGE_INVALID_DATA--;lr>`.
3. OpenSIPS attempts `topology_hiding_match()` using the Route header's `thinfo` param — **fails** because the value is garbage.
4. OpenSIPS responds with **500 "Error"**.
5. UAS expects and validates the 500 response.
6. UAC then sends BYE normally (using the valid encoded Contact), which succeeds.

## Key Assertions

| Check | Where |
|-------|-------|
| Invalid thinfo in Route causes match failure | OpenSIPS returns 500 to UAS UPDATE |
| UAS-side Route with garbage rejected | UAS expects 500 |
| UAC-side sequentials still work | UAC BYE succeeds after the failed UAS UPDATE |
| Correct Route IP but invalid param data | Route points to correct proxy IP |
