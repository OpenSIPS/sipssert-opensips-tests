# 15. No Contact in Reply

**What it tests:** Topology hiding behavior when the UAS responds with a 200 OK that contains **no Contact header**. Verifies that OpenSIPS handles this gracefully — it strips the Record-Route but does not add an encoded Contact since there's nothing to encode. The UAC confirms no Contact and no Record-Route in the response.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the private network, UDP

## Call Flow

1. UAC sends INVITE (no Record-Routes in request).
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives INVITE with 1 Record-Route (with `thinfo=`), 2 Vias.
4. UAS responds 200 OK with the Record-Route echoed but **no Contact header**.
5. OpenSIPS strips the Record-Route before forwarding to UAC.
6. UAC validates:
   - **No Contact** header in 200 OK.
   - **No Record-Route** header in 200 OK.
7. UAC sends ACK to the original Request-URI (since no Contact was received to update the target).

## Key Assertions

| Check | Where |
|-------|-------|
| No Contact in 200 OK reaches UAC | UAC checks `check_it_inverse` for Contact |
| No Record-Route in 200 OK | UAC checks `check_it_inverse` for Record-Route |
| OpenSIPS handles missing Contact gracefully | No crash, call completes |
| ACK sent to original R-URI (no contact update) | UAC sends ACK to `sip:...@remote_ip:remote_port` |
