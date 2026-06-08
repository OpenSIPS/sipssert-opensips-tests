# 17. Internal Record-Routes Only - UAC Internal (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding where the **UAC is on the internal/private network** and the UAS is on the public network. This reverses the typical topology — the proxy hides the internal UAC from the external UAS. The UAC receives a Record-Route (for routing back through the proxy), while the UAS sees no Record-Routes and only 1 Via.

## Network Layout (Reversed)

- **UAC** — on the **private** network, TCP (connects to internal socket `10.100.20.40:5062`)
- **OpenSIPS** — dual-homed (public + private), with socket tags
- **UAS** — on the **public** network, UDP (reached via `203.0.100.10:5060`)

## Key Config Difference

- The `outbound_socket_switch` route is used when traffic is OUTBOUND (from internal to external).
- UAC connects via TCP to the internal socket; proxy forwards to UAS via the external UDP socket.

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE over TCP to OpenSIPS's internal socket.
2. OpenSIPS calls `topology_hiding("U")`, switches to external socket, forwards to UAS.
3. UAS receives INVITE and validates:
   - **No Record-Route** headers (all hidden from UAS).
   - **Only 1 Via** header.
   - Contact contains `thinfo=` (the encoded UAC contact).

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with no Record-Routes.
2. OpenSIPS adds a Record-Route for the UAC (so it can route sequentials back through proxy).
3. UAC validates:
   - **1 Record-Route** present.
   - No second Record-Route.

## Sequential Requests

- UAC includes `[routes]` (the Record-Route) in ACK, UPDATE, BYE.
- UAS verifies: 1 Via, no Record-Route on all received requests.
- UAS sends UPDATE directly to the encoded Contact.
- UAC verifies: no Record-Route in UPDATE response, 2 Vias in received UPDATE.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS | UAS checks `check_it_inverse` on INVITE, ACK, UPDATE, BYE |
| Only 1 Via reaches UAS | UAS checks all received requests |
| 1 Record-Route given to UAC | UAC checks in 200 OK |
| UAC Contact encoded with thinfo | UAS verifies `thinfo=` present in Contact |
| No Record-Route in sequential responses | UAC checks UPDATE 200 |
