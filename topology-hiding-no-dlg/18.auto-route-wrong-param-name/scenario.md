# 18. Auto-Route Wrong Param Name

**What it tests:** Negative test — verifies that `topology_hiding_match()` correctly rejects a sequential request from the UAS where the Route header uses a **wrong parameter name** (`whatever=` instead of `thinfo=`), even though the encoded value is valid. This is the Route-header counterpart to test 14.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the private network, UDP

## Call Flow

1. Normal INVITE/200/ACK setup succeeds.
2. UAS extracts the valid `thinfo` value from the Record-Route it received.
3. UAS sends UPDATE with Route header: `<sip:10.100.20.40:5062;whatever=<valid_thinfo_value>--;lr>` — correct encoded data under the **wrong parameter name**.
4. OpenSIPS attempts `topology_hiding_match()` — **fails** because it looks for `thinfo` specifically.
5. OpenSIPS responds with **500 "Error"**.
6. UAS expects and validates the 500 response.
7. UAC then sends BYE normally, which succeeds.

## Key Assertions

| Check | Where |
|-------|-------|
| Wrong param name in Route causes match failure | OpenSIPS returns 500 to UAS UPDATE |
| Valid thinfo value under `whatever` is rejected | Param name must match `th_use_param` |
| UAC-side sequentials still work | UAC BYE succeeds |
| Correct Route IP, valid value, wrong key | Only param name is wrong |
