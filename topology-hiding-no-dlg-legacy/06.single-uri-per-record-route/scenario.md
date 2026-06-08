# 06. Single URI Per Record-Route (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding when the UAS responds with internal Record-Routes as **separate headers** (one URI per Record-Route line). This is the counterpart to test 05, verifying that the same hiding logic works regardless of whether URIs are packed on one line or split across multiple headers.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private)
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 external Record-Route headers.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - 3 Record-Routes (1 internal with `thinfo=` + 2 external).
   - No fourth Record-Route.
   - Exactly 2 Vias.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds with **5 separate Record-Route headers** (one URI each):
   - `<sip:UAS_IP:9090;transport=tls;r2=on;lr>` (internal)
   - `<sip:UAS_IP:PORT;transport=tcp;r2=on;lr>` (internal)
   - `<route1>` (proxy internal, echoed)
   - `<route2>` (external, echoed)
   - `<route3>` (external, echoed)
2. OpenSIPS identifies 2 internal routes, hides them, preserves the external ones.
3. UAC validates:
   - 2 external Record-Routes preserved in 200 OK (first occurrence matches proxy external IP pattern, second matches `10.0.0.1:9090`).

## Sequential Requests (UPDATE, BYE)

- OpenSIPS validates on inbound sequentials:
  - `$TH_decoded_routes_count == 2`
  - Both decoded route hosts are private IPs.
  - Decoded contact host is private.
- UAC verifies no Record-Route in sequential responses.
- UAS verifies 2 Vias on all received requests.

## Key Assertions

| Check | Where |
|-------|-------|
| Separate-header Record-Routes parsed correctly | Implicit — test passes only if parsing works |
| 2 external RRs preserved for UAC | UAC validates RR content in 200 OK |
| Decoded routes count = 2 | OpenSIPS checks on inbound sequentials |
| Both decoded route hosts are private | OpenSIPS validates `{ip.isprivate}` |
| Decoded contact host is private | OpenSIPS validates on sequential match |
| No Record-Route in sequential responses | UAC checks UPDATE responses |
