# Reject seizure of an active appearance after seizure expiry

Tests line-seize rejection for an appearance already in an active call. Requires
`sca_engage()` and the `list_lines` MI command. Internal SCA publishing is enabled.

One endpoint seizes appearance 1 for 10 seconds. A caller establishes a dialog
on that appearance while the seizure is live, then keeps the call up for 22
seconds. MI verifies that the appearance is active and its retained seizure has
expired before the second endpoint attempts to seize the same appearance.
The second SUBSCRIBE must return 480. A second MI check verifies that the
appearance is still active and that the seizure was not renewed. Finally, the
original call ends with BYE / 200 OK.

SIPp performs the signaling; Python is used only for the MI assertions.
The initial subscriber answers the initial NOTIFY and accepts an expiration
NOTIFY if one is sent. The
presence cleanup and subscription database timers run every second so expiry notification fits within the
test timeout.

Build the image from the desired OpenSIPS checkout (see
`docker/README.sipssert-local.md` in that repository):

```sh
docker build -f docker/Dockerfile.sipssert-local -t opensips-local:callinfo .
```

Then, from the SIPssert tests repository:

```sh
sudo sipssert presence -t 02.presence-callinfo-reject-active -E opensips_image=opensips-local:callinfo
```

