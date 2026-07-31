# 19. Single URI Per Record-Route - UAC Internal (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding where the UAC is on the internal network and sends Record-Routes, and the UAS responds with its own internal Record-Routes (each as a separate header). Both sets of internal routes are hidden from the opposite side. This combines the "UAC internal" scenario with "UAS adds internal Record-Routes as separate headers."

## Network Layout (Reversed)

- **UAC** — on the **private** network, TCP (connects to internal socket)
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the **public** network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 Record-Routes (both internal/private addresses).
2. OpenSIPS calls `topology_hiding("U")`, hides all from UAS, switches to external socket.
3. UAS receives INVITE with:
   - **No Record-Route** headers.
   - Only 1 Via.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with 2 internal Record-Routes (separate headers):
   - `<sip:10.100.0.1:8080;transport=tls;custom;lr>`
   - `<sip:UAS_IP:PORT;transport=tcp;lr>`
2. OpenSIPS encodes UAS's internal routes, adds the proxy auto-route, and restores UAC's original routes.
3. UAC validates:
   - **5 Record-Route** headers total (2 UAS internal + proxy auto-route + 2 UAC original).
   - No sixth Record-Route.

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC routes through the auto-route + the UAS's encoded routes (rr2, rr1).
- UAS verifies: 1 Via, no Record-Route.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE through the encoded Contact.
- OpenSIPS decodes, restores UAC's internal routes, forwards.
- UAC verifies: Route contains IPv6 address and `prv.acme.com`, no `thinfo` leaks.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS | UAS checks on all requests |
| Only 1 Via reaches UAS | UAS checks all requests |
| 5 Record-Routes returned to UAC | UAC checks in 200 OK |
| UAS internal RRs hidden from UAC sequentials | Handled internally by proxy |
| UAC internal RRs restored for UAS→UAC sequentials | UAC checks Route in received UPDATE |
| No thinfo leaks into Route | UAC checks `check_it_inverse` |
