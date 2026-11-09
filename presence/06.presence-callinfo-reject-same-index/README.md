# Reject a competing seizure of the same appearance

An endpoint seizes appearance 1 for 30 seconds. MI confirms the appearance is
seized and the seizure is live. A different subscription then requests the same
appearance for 10 seconds: expect 480 Temporarily Unavailable.

After rejection, MI confirms appearance 1 is still seized with a remaining
lifetime greater than the contender's requested 10 seconds. This checks that
the rejected request did not replace the owner's seizure or its expiry.
No call is established and no other appearance is involved.

The MI check accepts both line-level and per-index seizure fields.

```sh
sudo sipssert presence -t 06.presence-callinfo-reject-same-index
```
