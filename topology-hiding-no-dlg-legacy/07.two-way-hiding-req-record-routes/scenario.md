# 07. Two-Way Hiding - Request Record-Routes (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Two-way topology hiding where the proxy hides topology from **both** the UAC and UAS. The UAC sends Record-Routes in the request, but because no `th_internal_trusted_tag` / `th_external_socket_tag` are configured, the proxy strips all Record-Routes from the request before forwarding to the UAS, and strips all from the reply before forwarding to the UAC. Only the external ones are preserved for the UAC.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), **no socket tags configured**
- **UAS** — on the private network, UDP

## Key Config Difference

Unlike tests 01-06, this test does **not** configure `th_internal_trusted_tag` or `th_external_socket_tag`. This means OpenSIPS treats all Record-Routes as needing to be hidden from the UAS side (two-way hiding).

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 Record-Route headers.
2. OpenSIPS calls `topology_hiding("U")` — strips all Record-Routes from the request.
3. UAS receives the INVITE and validates:
   - **No Record-Route** headers at all.
   - **Only 1 Via** header (proxy's via only — UAC's via is stripped for full two-way hiding).

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with no Record-Route (since it received none).
2. OpenSIPS forwards to UAC.
3. UAC validates:
   - **2 Record-Route** headers preserved (the original external ones from the request).

## ACK (UAC → OpenSIPS → UAS)

- UAC sends ACK to encoded Contact.
- OpenSIPS matches and forwards.
- UAS verifies: only 1 Via (full hiding — UAC's via not visible).

## Sequential UPDATE (UAC → OpenSIPS → UAS)

- UAC sends UPDATE.
- OpenSIPS matches and forwards.
- UAS verifies: 1 Via only.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE directly to the Contact it received (encoded contact from proxy).
- OpenSIPS matches and forwards.
- UAC verifies: no Record-Route in response.

## BYE (UAC → OpenSIPS → UAS)

- UAC sends BYE. UAS verifies 1 Via, responds 200.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS | UAS checks `check_it_inverse` on INVITE |
| Only 1 Via reaches UAS (full hiding) | UAS checks on INVITE, ACK, UPDATE, BYE |
| 2 external Record-Routes preserved for UAC | UAC checks in 200 OK |
| No Record-Route in sequential responses/requests to UAC | UAC checks UPDATE |
| Two-way hiding active (no socket tags) | OpenSIPS config has no tag params |
