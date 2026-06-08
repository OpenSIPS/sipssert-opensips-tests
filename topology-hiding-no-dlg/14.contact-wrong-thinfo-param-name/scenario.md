# 14. Contact Wrong thinfo Param Name

**What it tests:** Negative test — verifies that `topology_hiding_match()` correctly rejects a sequential request where the topology hiding parameter uses a **wrong parameter name** (e.g., `whatever=` instead of `thinfo=`), even though the encoded value itself is valid.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — not involved in the failure scenario

## Call Flow

1. UAC sends INVITE, receives 200 OK with encoded Contact containing `thinfo=<encoded_value>`.
2. UAC extracts the `thinfo` value from the Contact.
3. UAC sends ACK to the encoded Contact (normal).
4. UAC sends UPDATE with a **manually crafted Request-URI** using `whatever=<valid_thinfo_value>` — correct encoded data but under the **wrong parameter name**.
5. OpenSIPS attempts `topology_hiding_match()`, which **fails** because it looks for the `thinfo` param specifically and doesn't find it.
6. OpenSIPS responds with **500 "Error"**.
7. UAC expects and validates receiving the 500 response.

## Key Assertions

| Check | Where |
|-------|-------|
| Wrong param name causes match failure | OpenSIPS returns 500 |
| Valid thinfo value under wrong key is rejected | Param name must match configured `th_use_param` |
| Normal INVITE/200/ACK flow works | Setup succeeds before the bad UPDATE |
