# Reject seizure of a held appearance after seizure expiry

Requires OpenSIPS with `sca_engage()` and the `list_lines` MI command.
Internal SCA publishing is enabled.

An endpoint seizes appearance 1 for 10 seconds and establishes a call. It places
that call on hold using a re-INVITE with `a=sendonly`. MI verifies that appearance
1 is held and its original seizure has expired. A second endpoint then attempts
to seize appearance 1: expect 480, with the appearance still held and the seizure
still expired. The original endpoint resumes using a re-INVITE with `a=sendrecv`.
MI verifies the appearance becomes active again; the call ends with BYE / 200 OK.

This test defines held appearances as unavailable for a fresh seizure. It checks
state preservation and resumption by the original endpoint; it does not test
retrieval by another endpoint or decide the signaling required for that feature.

From the SIPssert tests repository:

```sh
sudo sipssert presence -t 05.presence-callinfo-reject-held -E opensips_image=opensips-local:callinfo
sudo sipssert presence -t 05.presence-callinfo-reject-held -E opensips_image=opensips-local:callinfo-fix
```
