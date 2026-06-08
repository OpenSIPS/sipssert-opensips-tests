# 03. Internal Record-Routes Mixed (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Topology hiding when the UAS adds internal Record-Route headers (IPv4, IPv6, and hostname-based) in its 200 OK response. Verifies that OpenSIPS hides these internal routes from the UAC but correctly decodes and restores them for sequential requests reaching the UAS.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private)
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE (no Record-Routes in original request).
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - Exactly **one** Record-Route (the proxy's internal hop with `thinfo=`).
   - No second Record-Route.
   - Exactly 2 Via headers, no third.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with **four** Record-Route headers:
   - `<sip:prv.acme.com;transport=tls;r2=on;lr>` (hostname-based)
   - `<sips:[2001:db8:abcd:abc:ab::123:5678]:9090;transport=tls;r2=on;lr>` (IPv6)
   - `<sip:UAS_IP:PORT;transport=tcp;lr>` (UAS local)
   - `<proxy internal route>` (echoed from INVITE)
2. OpenSIPS encodes the 3 internal routes into topology hiding info and strips all Record-Routes before forwarding to UAC.
3. UAC validates: **no Record-Route** in the 200 OK.

## ACK (UAC → OpenSIPS → UAS)

- UAC sends ACK to encoded Contact.
- OpenSIPS decodes and forwards, restoring the internal routes.
- UAS verifies:
  - 2 Vias, no third.
  - Route headers contain the IPv6 route and the `prv.acme.com` route.
  - No `thinfo=` parameter leaks into the Route headers.

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC sends UPDATE to encoded Contact.
- OpenSIPS matches and validates:
  - `$TH_decoded_routes_count == 3`
  - Route hosts are: IPv4 address, IPv6 address, and `prv.acme.com` (in order).
  - Decoded contact host is private.
- Forwards to UAS with restored Route headers.
- UAS verifies same Route assertions as ACK (IPv6, hostname present, no `thinfo`).

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE with its own Record-Routes and Route through the proxy.
- OpenSIPS matches, decodes, forwards to UAC.
- UAC verifies: no Record-Route in response.

## BYE (UAC → OpenSIPS → UAS)

- UAC sends BYE to latest Contact.
- UAS verifies: 2 Vias, correct Route headers (IPv6 + hostname), no `thinfo`.
- Responds 200.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAC | UAC checks all responses |
| Decoded routes count = 3 | OpenSIPS validates on inbound sequentials |
| Route host[0] is IPv4 | OpenSIPS validates `{ip.isip4}` |
| Route host[1] is IPv6 | OpenSIPS validates `{ip.isip6}` |
| Route host[2] is `prv.acme.com` | OpenSIPS validates hostname match |
| Decoded contact host is private | OpenSIPS validates `{ip.isprivate}` |
| Restored routes contain IPv6 and hostname | UAS checks ACK, UPDATE, BYE Route headers |
| No `thinfo` leaks into Route | UAS checks `check_it_inverse` on Route headers |
