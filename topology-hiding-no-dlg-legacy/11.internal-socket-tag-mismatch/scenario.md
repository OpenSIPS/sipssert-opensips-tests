# 11. Internal Socket Tag Mismatch (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Negative test — verifies that `topology_hiding_match()` **fails** when the UAS sends a sequential request with a Route URI containing a modified host that does NOT match the internal socket, AND the external socket tag is misconfigured (`external_socket-other` instead of `external_socket`). This ensures the proxy correctly rejects the request with a 400 error.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with **mismatched external socket tag** (`external_socket-other`)
- **UAS** — on the private network, UDP

## Key Config Difference

The `th_external_socket_tag` is set to `"external_socket-other"` while the actual socket tag is `"external_socket"`. This mismatch causes `topology_hiding_match()` to fail on sequential requests from the UAS side when the Route host is altered.

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 external Record-Route headers.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - 3 Record-Routes (1 internal with `thinfo=` + 2 external).
   - Extracts params from the first RR.

## 200 OK (UAS → OpenSIPS → UAC)

- UAS echoes back all 3 Record-Routes.
- OpenSIPS strips internal, preserves external.
- UAC validates: 2 external RRs preserved.

## Sequential UPDATE (UAS → OpenSIPS) — FAILURE CASE

- UAS sends UPDATE with Route header using `<sip:1.2.3.4:5062[route1_params]>` — different host with same params.
- Due to the socket tag mismatch configuration, `topology_hiding_match()` **fails**.
- OpenSIPS responds with **400 "MatchError"**.
- UAS expects and validates receiving the 400 response.

## BYE (UAC → OpenSIPS → UAS)

- Despite the failed UAS UPDATE, the call continues normally from the UAC side.
- UAC sends BYE successfully, UAS responds 200.

## Key Assertions

| Check | Where |
|-------|-------|
| topology_hiding_match() fails with tag mismatch | OpenSIPS returns 400 to UAS UPDATE |
| UAS receives 400 "MatchError" | UAS expects 400 response |
| UAC-side sequentials still work | UAC sends UPDATE and BYE successfully |
| External socket tag mismatch causes rejection | Config uses `external_socket-other` vs actual `external_socket` |
