# 16. No Contact in Reply with Internal Record-Routes

**What it tests:** Topology hiding behavior when the UAS responds with a 200 OK that has **no Contact header** but includes **internal Record-Routes** (from the UAS side). Verifies that OpenSIPS correctly strips the internal Record-Routes, preserves external ones for the UAC, and handles the missing Contact gracefully.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the private network, UDP

## Call Flow

1. UAC sends INVITE with 1 external Record-Route.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives INVITE with 2 Record-Routes (1 internal with `thinfo=` + 1 external), 2 Vias.
4. UAS responds 200 OK with:
   - An additional internal Record-Route `<sip:1.2.3.4:5060>`.
   - The echoed proxy internal Record-Route.
   - **No Contact header**.
5. OpenSIPS strips internal Record-Routes, preserves the external one.
6. UAC validates:
   - **No Contact** in 200 OK.
   - **1 Record-Route** preserved (the original external one from the request).
   - No second Record-Route.
7. UAC sends ACK to original R-URI.

## Key Assertions

| Check | Where |
|-------|-------|
| No Contact in 200 OK reaches UAC | UAC checks `check_it_inverse` for Contact |
| 1 external Record-Route preserved | UAC checks exactly 1 RR present, no second |
| Internal RRs stripped despite missing Contact | OpenSIPS handles correctly |
| ACK sent to original R-URI | UAC uses `sip:...@remote_ip:remote_port` |
