# Seize an idle appearance alongside an active call

Requires OpenSIPS with `sca_engage()` and the `list_lines` MI command.
Internal SCA publishing is enabled.

The setup seizes and releases appearance 2, leaving it explicitly idle. It then
seizes appearance 1 for 10 seconds and establishes a call that lasts 22 seconds.
MI confirms that appearance 1 is active, its seizure has expired, and appearance
2 is idle. A second endpoint seizes appearance 2: expect 200 OK and a NOTIFY.
MI then confirms that appearance 2 is seized with a live expiry while appearance
1 remains active. The original call ends normally with BYE / 200 OK.

This case checks an idle appearance while another appearance is in an active
call. The original seizure has expired before the request. Test 04 separately
checks concurrent live seizures on different indexes.

From the SIPssert tests repository:

```sh
sudo sipssert presence -t 03.presence-callinfo-idle
```
