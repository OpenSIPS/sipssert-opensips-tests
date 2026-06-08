# 02. External Record-Routes Only

**What it tests:** Topology hiding when the UAC includes external (non-proxy) Record-Route headers in the INVITE. Verifies that OpenSIPS preserves these external Record-Routes for the UAC while adding its own internal hop for the UAS, and that sequential requests are routed correctly.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private)
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with **two external Record-Route headers** already present (simulating upstream proxies).
2. OpenSIPS calls `topology_hiding("U")` and forwards to the UAS.
3. UAS receives the INVITE and validates:
   - Exactly **three** Record-Route headers: 1 internal (with `thinfo=`) + 2 external ones passed through.
   - No fourth Record-Route.
   - Exactly 2 Via headers (no extra Via leaks).

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK, echoing back all 3 Record-Routes it received.
2. OpenSIPS decodes and strips the internal Record-Route, passes through the external ones.
3. UAC validates:
   - **Two Record-Route** headers remain (the original external ones).
   - First RR matches `<sip:IP:5060;transport=tcp;lr>` (the proxy's external-facing address).
   - Second RR matches `<sip:10.0.0.1:9090;transport=udp;custom;lr>` (the upstream proxy).

## ACK (UAC → OpenSIPS → UAS)

- UAC sends ACK to the encoded Contact.
- OpenSIPS matches and forwards.
- UAS verifies: 2 Vias, no third.

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC sends UPDATE to the encoded Contact.
- OpenSIPS matches, validates decoded routes count = 0 and decoded contact host is private.
- UAS verifies: 2 Vias.
- UAS responds 200 OK with new Contact.
- UAC verifies: **no Record-Route** in the UPDATE 200 response.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE using Route headers (all 3 Record-Routes from the INVITE).
- OpenSIPS matches, decodes, forwards to UAC.
- UAC verifies: no Record-Route in the UPDATE request or 200 response.

## BYE (UAC → OpenSIPS → UAS)

- UAC sends BYE to the latest Contact.
- UAS verifies: 2 Vias, responds 200.

## Key Assertions

| Check | Where |
|-------|-------|
| 2 external Record-Routes preserved for UAC in 200 OK | UAC checks RR content matches original external RRs |
| 3 Record-Routes reach UAS (1 internal + 2 external) | UAS checks on INVITE |
| No Record-Route in sequential responses to UAC | UAC checks UPDATE responses |
| No third Via leaks | UAS checks on INVITE, ACK, UPDATE, BYE |
| Decoded routes count = 0 | OpenSIPS checks for inbound sequentials |
| Decoded contact host is private | OpenSIPS validates on sequential match |
