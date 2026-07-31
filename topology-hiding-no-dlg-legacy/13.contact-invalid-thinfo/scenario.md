# 13. Contact Invalid thinfo (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Negative test — verifies that `topology_hiding_match()` correctly rejects a sequential request where the `thinfo` parameter in the Request-URI contains **garbage/invalid data** that cannot be decoded.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — not involved in the failure scenario

## Call Flow

1. UAC sends INVITE, receives 200 OK with encoded Contact (normal setup).
2. UAC sends ACK to the encoded Contact (normal).
3. UAC sends UPDATE with a **manually crafted Request-URI** containing `thinfo=GARBAGE_INVALID_DATA--` — invalid encoded data.
4. OpenSIPS attempts `topology_hiding_match()`, which **fails** because the thinfo value cannot be decoded.
5. OpenSIPS responds with **500 "Error"**.
6. UAC expects and validates receiving the 500 response.

## Key Assertions

| Check | Where |
|-------|-------|
| Invalid thinfo data causes match failure | OpenSIPS returns 500 |
| Garbage thinfo rejected gracefully | No crash, clean 500 response |
| Normal INVITE/200/ACK flow works | Setup succeeds before the bad UPDATE |
