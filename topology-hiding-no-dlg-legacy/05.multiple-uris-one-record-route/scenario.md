# 05. Multiple URIs One Record-Route (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding when the UAS packs all Record-Route URIs (internal + external) into a **single Record-Route header line** (comma-separated). Verifies that OpenSIPS correctly parses multiple URIs from one header, identifies which are internal, hides them, and preserves the external ones for the UAC.

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

1. UAS responds with a **single Record-Route header** containing 5 comma-separated URIs:
   - `<sip:UAS_IP:9090;...lr>` (internal)
   - `<sip:UAS_IP:PORT;...lr>` (internal)
   - `<route1>`, `<route2>`, `<route3>` (echoed from INVITE)
2. OpenSIPS parses all 5 URIs from the single header, identifies 2 as internal, encodes them, and strips them.
3. UAC validates:
   - 2 external Record-Routes preserved (matching the originals).

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
| Single-line multi-URI Record-Route parsed correctly | Implicit — test passes only if parsing works |
| 2 external RRs preserved for UAC | UAC validates in 200 OK |
| Decoded routes count = 2 | OpenSIPS checks on inbound sequentials |
| Both decoded route hosts are private | OpenSIPS validates `{ip.isprivate}` |
| Decoded contact host is private | OpenSIPS validates on sequential match |
| No Record-Route in sequential responses | UAC checks UPDATE responses |
