# Seize an idle appearance alongside an active call

Requires OpenSIPS with `sca_engage()` and the `list_lines` MI command.
Internal SCA publishing is enabled.

The setup seizes and releases appearance 2, leaving it explicitly idle. It then
seizes appearance 1 for 10 seconds and establishes a call that lasts 22 seconds.
MI confirms that appearance 1 is active, its seizure has expired, and appearance
2 is idle. A second endpoint seizes appearance 2: expect 200 OK and a NOTIFY.
MI then confirms that appearance 2 is seized with a live expiry while appearance
1 remains active. The original call ends normally with BYE / 200 OK.

This should pass both before and after adding occupied-appearance rejection:
the requested appearance is idle, even though another appearance on the same
shared line has an active call. A still-live seizure is deliberately excluded
from the preconditions, since it prevents a new seizure anywhere on the line.

From the SIPssert tests repository:

```sh
sudo sipssert presence -t 03.presence-callinfo-idle -E opensips_image=opensips-local:callinfo
sudo sipssert presence -t 03.presence-callinfo-idle -E opensips_image=opensips-local:callinfo-fix
```
