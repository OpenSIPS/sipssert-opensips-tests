# 09. Two-Way Hiding - Reply Record-Routes (Legacy Encoding)

> **Legacy Mode:** This test is identical to its non-legacy counterpart but uses the legacy Contact encoding format (`:L` flag in `th_contact_encode_param_password`). This validates backward compatibility with the older encoding scheme.

**What it tests:** Two-way topology hiding where the UAC sends **no** Record-Routes in the request, but the UAS adds Record-Routes in its 200 OK reply. Verifies that with no socket tags configured, OpenSIPS hides the UAS's reply Record-Routes from the UAC completely.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), **no socket tags configured**
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with **no Record-Route** headers.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - **No Record-Route** headers.
   - **Only 1 Via** header (full two-way hiding).

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK with a Record-Route containing 2 comma-separated internal URIs.
2. OpenSIPS encodes and strips them completely (two-way hiding, no external routes to preserve).
3. UAC validates:
   - **No Record-Route** in the 200 OK.
   - Extracts encoded Contact.

## Sequential Requests (ACK, UPDATE, BYE)

- UAC sends all sequentials to the encoded Contact.
- UAS verifies: only 1 Via on all requests.
- UAS sends UPDATE directly to encoded Contact (no Route headers).
- UAC verifies: no Record-Route in any sequential message.

## Key Assertions

| Check | Where |
|-------|-------|
| No Record-Route reaches UAS on INVITE | UAS checks `check_it_inverse` |
| Only 1 Via reaches UAS | UAS checks all received requests |
| No Record-Route reaches UAC in 200 OK | UAC checks `check_it_inverse` |
| No Record-Route in any sequential message | UAC checks UPDATE response and request |
| UAS reply RRs fully hidden | Implicit — no RR seen by UAC |
