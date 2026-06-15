# 22. Malicious thinfo

**What it tests:** Robustness/security test — sends a series of INVITEs whose Request-URI carries a deliberately malformed `thinfo` parameter to verify that OpenSIPS's topology hiding decoder rejects every crafted payload gracefully (responding **500**) rather than crashing, reading out of bounds, or accepting invalid data. Each vector targets a specific code path in the `thinfo` decode logic.

> **Note:** Each `thinfo` value is precomputed (offline) using the default XOR password configured for this test. The encoded blobs are intentionally omitted from this document — see `scripts/uac.xml` for the actual values.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — not involved; every INVITE is rejected at the proxy

## Flow

The UAC runs 14 independent attack vectors back to back. For each vector it:
1. Sends an INVITE with a crafted `thinfo` in the R-URI.
2. Expects a **500** response from OpenSIPS.
3. Sends an ACK to complete the failed transaction.

There is no UAS and no successful call — passing means every malformed payload is rejected with a 500.

## Vectors

| # | Name | What it targets |
|---|------|-----------------|
| 01 | `mal_uri_count_zero` | `uri_count == 0` — rejected in the sequential path |
| 02 | `mal_uri_count_255` | `uri_count = 255` exceeds the max (12) — rejected before the decode loop |
| 03 | `mal_uri_count_overstated` | Claims 12 URIs but supplies 1 — bounds underrun guard returns -1 |
| 04 | `mal_invalid_scheme` | Scheme bits = 6 (greater than the max URN value) — invalid properties detected |
| 05 | `mal_invalid_transport` | Transport bits = 0x30 (greater than WSS) — garbage data rejected |
| 06 | `mal_invalid_domain` | Domain bits = 0xC0 (greater than FQDN) — garbage data rejected |
| 07 | `mal_fqdn_len_truncated` | FQDN length byte = 255 with no following data — read bounds guard returns -1 |
| 08 | `mal_dual_missing_uri2props` | Dual-URI flag set but the second URI's properties byte is absent — bounds guard returns -1 |
| 09 | `mal_decode_buffer_pressure` | 12 maximal URIs — exercises the decode output bounds guard |
| 10 | `mal_socket_truncated` | Socket block only 2 bytes — `decode_socket` fails |
| 11 | `mal_socket_bad_proto` | Socket proto bits = 7 (reserved) — switch hits default, returns -1 |
| 12 | `mal_params_len_overrun` | `HAS_PARAMS` length = 255 with 1 byte of data — read bounds guard returns -1 |
| 13 | `mal_pure_garbage` | Arbitrary bytes — header/properties validation rejects |
| 14 | `mal_uri_count` | uri count greater than actual encoded uris - indicated 3 URIs, actual 2 URIs - bounds guard returns -1 |
| 15 | `mal_empty` | Empty `thinfo` value — base64 decode returns <= 0, rejected |

## Key Assertions

| Check | Where |
|-------|-------|
| Every malformed `thinfo` yields a 500 | UAC expects `response="500"` per vector |
| No crash / clean rejection across all 14 vectors | Scenario completes all vectors |
| Bounds and validation guards cover count, scheme, transport, domain, FQDN, dual-URI, socket, params, and empty inputs | One vector per guard |
