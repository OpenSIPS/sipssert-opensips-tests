# Reject competing seizure while a seizure is live

Requires OpenSIPS with the `list_lines` MI command.

The setup seizes and releases appearance 2, leaving it explicitly idle. An
endpoint then seizes appearance 1 for 10 seconds. MI confirms appearance 1 is
seized with a live expiry and appearance 2 is idle. Before that seizure expires,
a second endpoint requests appearance 2: expect 480 Temporarily Unavailable.
MI confirms the original seizure is still live and appearance 2 remains idle.

No call is established: this isolates the existing line-wide seizure lock from
checks for appearances occupied by calls. It should pass with both images.

From the SIPssert tests repository:

```sh
sudo sipssert presence -t 04.presence-callinfo-reject-seized -E opensips_image=opensips-local:callinfo
sudo sipssert presence -t 04.presence-callinfo-reject-seized -E opensips_image=opensips-local:callinfo-fix
```
