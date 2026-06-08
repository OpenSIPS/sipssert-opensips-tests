# 10. Internal Socket Tag Match

**What it tests:** Topology hiding where the UAS sends a sequential request (UPDATE) with the Route header modified to use a **different IP** but keeping the same `thinfo` parameter from the original Record-Route. This tests that `topology_hiding_match()` correctly matches based on the `thinfo` parameter regardless of the host in the Route URI — simulating a scenario where the internal socket's IP matches the tag.

## Network Layout

- **UAC** — on the public network, TCP
- **OpenSIPS** — dual-homed (public + private), with socket tags configured
- **UAS** — on the private network, UDP

## Initial INVITE (UAC → OpenSIPS → UAS)

1. UAC sends INVITE with 2 external Record-Route headers.
2. OpenSIPS calls `topology_hiding("U")` and forwards to UAS.
3. UAS receives the INVITE and validates:
   - 3 Record-Routes (1 internal with `thinfo=` + 2 external).
   - First RR has `thinfo=` parameter.
   - Extracts the params from the first RR for later use.
   - No fourth Record-Route.
   - Exactly 2 Vias.

## 200 OK (UAS → OpenSIPS → UAC)

1. UAS responds 200 OK echoing back the 3 Record-Routes it received.
2. OpenSIPS strips the internal one, preserves external ones.
3. UAC validates: 2 external Record-Routes preserved.

## Sequential UPDATE (UAS → OpenSIPS → UAC)

- UAS sends UPDATE with Route header using `<sip:1.2.3.4:5062[route1_params]>` — a **different host** (`1.2.3.4`) but with the same `thinfo` params extracted from the original Record-Route.
- OpenSIPS successfully matches via `topology_hiding_match()` because the `thinfo` param is present and valid.
- The test passes, proving that match works on the param, not the host.

## Key Assertions

| Check | Where |
|-------|-------|
| Match works with different host but same thinfo param | UAS sends Route with `1.2.3.4` but correct params |
| 2 external RRs preserved for UAC | UAC validates in 200 OK |
| Decoded routes count = 0 | OpenSIPS checks on inbound sequentials |
| Decoded contact host is private | OpenSIPS validates |
| No Record-Route in sequential responses | UAC checks |
| 2 Vias only on UAS side | UAS checks all requests |
