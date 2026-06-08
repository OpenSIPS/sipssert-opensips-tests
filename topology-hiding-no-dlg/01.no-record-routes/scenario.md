# 01. No Record-Routes

**What it tests:** Topology hiding with no dialog state, verifying that when the proxy hides topology, no Record-Route headers leak to the UAC, and sequential requests (UPDATE, BYE) are correctly routed using only the encoded Contact.

## Network Layout

- **UAC** — on the public network (`203.0.100.10:5060`, TCP)
- **OpenSIPS** — dual-homed (public + private)
- **UAS** — on the private network (`10.50.100.10:8060`, UDP)

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE over TCP to OpenSIPS's public socket.
2. OpenSIPS calls `topology_hiding("U")` — encodes the Contact using the `thinfo` param with password `ToPoCtPaSS`. The `"U"` flag means only the Contact URI user-part is used for encoding.
3. OpenSIPS switches the outbound socket to the internal UDP socket and forwards to the UAS.
4. UAS receives the INVITE and validates:
   - Exactly **one** Record-Route header is present (the internal proxy hop, containing `thinfo=`).
   - Exactly **two** Via headers (proxy + UAC's original via is hidden by proxy via).
   - No third Via or second Record-Route leaks through.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK, echoing back the single Record-Route it received.
2. OpenSIPS decodes topology info and strips the Record-Route before forwarding to UAC.
3. UAC validates:
   - **No Record-Route** headers in the 200 OK.
   - Extracts the Contact URI (which is the encoded/hidden contact from OpenSIPS).

## ACK (UAC → OpenSIPS → UAS)

- UAC sends ACK directly to the Contact URI it received (the encoded contact).
- OpenSIPS matches via `topology_hiding_match()`, decodes the real UAS contact, and forwards.
- UAS verifies: exactly 2 Via headers, no extra.

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC sends UPDATE to the same encoded Contact.
- OpenSIPS matches, decodes, validates `$TH_decoded_routes_count == 0` (no hidden routes expected), confirms the decoded contact host is a private IP.
- UAS verifies: 2 Vias, no third.
- UAS responds 200 OK with a new Contact.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE back through the Route it stored (the single Record-Route from the INVITE).
- OpenSIPS matches, decodes, forwards to UAC.
- UAC verifies: no Record-Route in the 200 reply, extracts updated Contact.

## BYE (UAC → OpenSIPS → UAS)

- UAC sends BYE to the latest Contact it received.
- OpenSIPS matches and relays.
- UAS verifies: 2 Vias, responds 200 OK.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAC | UAC checks `check_it_inverse` on all responses |
| Exactly 1 Record-Route (with `thinfo`) reaches UAS | UAS checks on INVITE |
| No third Via leaks | UAS checks on INVITE, ACK, UPDATE, BYE |
| Decoded routes count = 0 | OpenSIPS checks `$TH_decoded_routes_count` for inbound sequentials |
| Decoded contact host is private IP | OpenSIPS checks `$(var(ct_host){ip.isprivate})` |
