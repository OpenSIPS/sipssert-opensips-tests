# 20. Internal Record-Routes Mixed - UAC Internal

**What it tests:** Topology hiding where the UAC is on the internal network and sends **multiple internal Record-Routes** (IPv4, IPv6, and hostname) in the INVITE. Verifies that when the UAC is internal, these Record-Routes are hidden from the external UAS but correctly decoded and restored when the UAS sends sequential requests back.

## Network Layout (Reversed)

- **UAC** — on the **private** network, TCP (connects to internal socket)
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the **public** network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 3 Record-Routes:
   - `<sip:UAC_IP:PORT;transport=tcp;lr>` (IPv4, internal)
   - `<sips:[2001:db8:abcd:abc:ab::123:5678]:9090;transport=tls;r2=on;lr>` (IPv6)
   - `<sip:prv.acme.com;transport=tls;r2=on;lr>` (hostname)
2. OpenSIPS calls `topology_hiding("U")`, hides all from UAS.
3. UAS receives INVITE with:
   - **No Record-Route** headers.
   - Only 1 Via.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK (echoing the empty Record-Route set).
2. OpenSIPS adds the proxy's Record-Route and restores the UAC's original routes.
3. UAC validates:
   - **4 Record-Route** headers total: 1 from proxy (auto-route) + 3 originals.
   - No fifth Record-Route.

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC routes through the proxy's Record-Route (the auto-route).
- UAS verifies: 1 Via, no Record-Route.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE back, routing through the encoded Contact.
- OpenSIPS decodes, restores the internal routes, and forwards to UAC.
- UAC verifies:
  - Route headers contain the IPv6 and `prv.acme.com` routes (restored).
  - No `thinfo=` leaks into Route headers.
  - No Record-Route in the request.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS | UAS checks on INVITE, ACK, UPDATE, BYE |
| Only 1 Via reaches UAS | UAS checks all requests |
| 4 Record-Routes given to UAC | UAC checks in 200 OK |
| Restored routes include IPv6 and hostname | UAC checks Route in received UPDATE |
| No thinfo leaks into Route | UAC verifies `check_it_inverse` on Route for thinfo |
