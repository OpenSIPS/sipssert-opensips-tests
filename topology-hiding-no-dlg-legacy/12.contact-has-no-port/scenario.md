# 12. Contact Has No Port (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding when the UAS's Contact URI has **no port** specified (e.g., `sip:user@host` without `:port`). Verifies that OpenSIPS correctly encodes and decodes Contacts that omit the port, using the default SIP port (5060) for routing.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the private network, UDP (destination port 5060 instead of 8060)

## Key Difference

- UAS Contact in 200 OK: `<sip:+13175000120@[local_ip]>` — no port.
- The `inbound_socket_switch` route sets `$du` to port 5060 (matching default).

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE, no Record-Routes in request.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives INVITE and validates:
   - 1 Record-Route with `thinfo=`.
   - No second Record-Route.
   - 2 Vias, no third.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with Contact `<sip:+13175000120@UAS_IP>` (no port).
2. OpenSIPS encodes this port-less Contact into the topology hiding info.
3. UAC validates: no Record-Route in 200 OK.

## Sequential Requests (ACK, UPDATE, BYE)

- All work normally, proving that the port-less Contact was correctly encoded/decoded.
- OpenSIPS validates decoded routes count = 0 and decoded contact host is private.
- UAS also sends its own Contact without port in UPDATE responses.

## Key Assertions

| Check | Where |
|-------|-------|
| Port-less Contact correctly encoded/decoded | Implicit — sequentials succeed |
| No Record-Route reaches UAC | UAC checks all responses |
| Decoded routes count = 0 | OpenSIPS checks on inbound sequentials |
| Decoded contact host is private | OpenSIPS validates |
| 2 Vias on UAS side | UAS checks all requests |
