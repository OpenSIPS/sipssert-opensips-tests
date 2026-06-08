# 08. Two-Way Hiding - Mixed Record-Routes

**What it tests:** Two-way topology hiding where both the UAC sends Record-Routes in the request AND the UAS adds Record-Routes in the reply. With no socket tags configured, OpenSIPS hides everything from both sides — the UAS sees no Record-Routes from the request, and the UAC only sees its own original external Record-Routes (not the UAS's).

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), **no socket tags configured**
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 Record-Route headers.
2. OpenSIPS calls `topology_hiding("U")` — strips all Record-Routes from the request (two-way hiding).
3. UAS receives the INVITE and validates:
   - **No Record-Route** headers.
   - **Only 1 Via** header (UAC's Via stripped for full hiding).

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with a Record-Route header containing 2 comma-separated internal URIs:
   - `<sip:UAS_IP:9090;transport=tls;r2=on;lr>`
   - `<sip:UAS_IP:PORT;transport=tcp;r2=on;lr>`
2. OpenSIPS encodes and strips UAS's Record-Routes, restores the UAC's original external ones.
3. UAC validates:
   - 2 Record-Routes preserved (matching original externals).

## Sequential Requests

- UAC sends ACK, UPDATE, BYE to encoded Contact.
- UAS verifies: only 1 Via on all requests (full two-way hiding).
- UAS sends UPDATE directly to encoded Contact (no Route needed since it received none).
- UAC verifies: no Record-Route in sequential responses/requests.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS on INVITE | UAS checks `check_it_inverse` |
| Only 1 Via reaches UAS | UAS checks all received requests |
| UAS's reply Record-Routes hidden from UAC | UAC sees only its original 2 RRs |
| 2 external RRs preserved for UAC | UAC validates content in 200 OK |
| No Record-Route in sequential messages | UAC checks UPDATE |
