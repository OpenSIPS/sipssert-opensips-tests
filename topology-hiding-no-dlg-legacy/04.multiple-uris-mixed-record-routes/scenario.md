# 04. Multiple URIs Mixed Record-Routes (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding when both external Record-Routes (from UAC) and internal Record-Routes (from UAS) are present, with multiple URIs packed into single Record-Route header lines (comma-separated). Verifies correct parsing of multi-URI Record-Route headers and that internal routes are hidden while external ones are preserved.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private)
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with **two external Record-Route** headers.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - **Three** Record-Route headers (1 internal with `thinfo=` + 2 external passed through).
   - No fourth Record-Route.
   - Exactly 2 Via headers.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with Record-Routes containing **multiple URIs per header line** (comma-separated):
   - Line 1: `<sip:UAS_IP:9090;...lr>, <sip:UAS_IP:PORT;...lr>` (two internal URIs on one line)
   - Line 2: `<route1>, <route2>` (echoed proxy routes)
   - Line 3: `<route3>` (echoed external route)
2. OpenSIPS parses the multi-URI headers, identifies 2 internal routes, encodes them in topology hiding, and strips them.
3. UAC validates:
   - **Two Record-Route** headers preserved (the original external ones from the INVITE).
   - First matches `<sip:IP:5060;transport=tcp;lr>`.
   - Second matches `<sip:10.0.0.1:9090;transport=udp;custom;lr>`.

## ACK / Sequential UPDATE / BYE

- Same flow as other tests: UAC sends to encoded Contact, OpenSIPS decodes.
- OpenSIPS validates on sequential inbound requests:
  - `$TH_decoded_routes_count == 2`
  - Both decoded route hosts are private IPs.
  - Decoded contact host is private.
- UAC verifies no Record-Route in sequential responses.
- UAS verifies 2 Vias on all received requests.

## Key Assertions

| Check | Where |
|-------|-------|
| Multi-URI Record-Route headers parsed correctly | Implicit — test passes only if parsing works |
| 2 external RRs preserved for UAC | UAC validates RR content in 200 OK |
| Decoded routes count = 2 | OpenSIPS checks on inbound sequentials |
| Both decoded route hosts are private | OpenSIPS validates `{ip.isprivate}` |
| Decoded contact host is private | OpenSIPS validates on sequential match |
| No Record-Route in sequential responses | UAC checks UPDATE responses |
| 2 Vias only | UAS checks all received requests |
