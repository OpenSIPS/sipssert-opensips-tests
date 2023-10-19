[![OpenSIPS 3.4 Conformance Tests](https://github.com/OpenSIPS/sipssert-opensips-tests/actions/workflows/run-tests.yml/badge.svg?branch=3.4)](https://github.com/OpenSIPS/sipssert-opensips-tests/actions/workflows/run-tests.yml)

# OpenSIPS Tests

This project contains a set of tests that are being performed to test the
behavior of the [OpenSIPS](https://www.opensips.org) SIP Server under certain
scenarios.

Tests are being executed by the [SIPssert](https://github.com/OpenSIPS/sipssert) tool

## Tests

There are multiple tests sets available, depending on what is their main
testing focus:

### Startup

Tests whether OpenSIPS starts up successfully with various configurations and settings.

#### 01.default-cfg

Tests OpenSIPS startup with the default sample script.

#### 02.gen-residential-cfg

Tests OpenSIPS startup with the menuconfig generated Residential Script.

#### 03.gen-trunking-cfg

Tests OpenSIPS startup with the menuconfig generated Trunking Script.

#### 04.gen-loadbalancer-cfg

Tests OpenSIPS startup with the menuconfig generated Load-Balancer Script.

### Registrations

Performs registration tests:

#### 01.no-db

Performs registrations tests when no database is involved. Verification steps are:
1. Register to OpenSIPS using sipp
2. Check the registration exists using OpenSIPS CLI
3. Unregister using sipp
4. Check the registration dissapeared

#### 02.db

Performs registrations tests using MySQL database. Verification steps are:
1. Register to OpenSIPS using sipp
2. Check the registration exists using OpenSIPS CLI
3. Check the registration exists in DB after flush timeout passes
4. Unregister using sipp
5. Check the registration dissapeared
6. Checks the database is empty after timer flush

#### 03.expire

Same as [02.db](#02db), but leaves the contact to expire.
1. Checks through MI that the registration was removed
2. Checks the database is empty after timer flush

#### 04.expire-min

Same as [03.expire](#03expire), but enforces a
minimum expire time.

#### 05.expire-max

Same as [03.expire](#03expire), but enforces a
maximum expire time.

#### 06.reregister-expire

Performs a registration and then a re-registration for the same contact.
1. Verifies that the initial registration was correct both through MI and MySQL
2. Checks the re-register matches the same contact and updates the registration
3. Verifies the entry expires correctly

#### 07.limit

Performs multiple registrations, but limit the number of contacts
1. Verifies that after each iteration, the correct number of contacts is in memory
2. Checks that the database contains the correct number of entries

#### 08.overwrite

Performs multiple registrations, each one overwriting the previous one
1. Verifies that after each iteration, there is only one contact registered
2. Checks that each registration overwrites the next one

#### 09.lookup

Does a registration and then relays a call to the registerd contact.

### Authentication

Performs authentication tests:

#### 01.password-db-www

Checks registration of an endpoint with passwords stored in DB
1. The tests expects a challenge followed by a 200 OK at SIP level

#### 02.password-db-www-domain

Same as [01.password-db-www](#01password-db-www), but checks also checks the
domain is correct.

#### 03.password-db-proxy

Same as [01.password-db-www](#01password-db-www), but checks if a call gets
authenticated.

#### 04.password-db-proxy-domain

Same as [03.password-db-proxy](#03password-db-proxy), but checks if the domain
is correct.

#### 05.ha1-db-www

Same as [01.password-db-www](#01password-db-www), but checks the ha1 password.

#### 06.ha1-db-www-domain

Same as [02.password-db-www-domain](#02password-db-www-domain), but checks the
ha1 password.

#### 07.ha1-db-proxy

Same as [03.password-db-proxy](#03password-db-proxy), but checks the ha1
password.

#### 08.ha1-db-proxy-domain

Same as [04.password-db-proxy-domain](#04password-db-proxy-domain), but checks
the ha1 password.

### Record Route

Places calls without using the Record-Route mechanism. Checks are being
performed at the (SIPP) UAC/UAS level, ensuring the traffic completes as
expected and validating the Route and Record-Route headers.

#### 01.record-route

Places a call and validates it establishes correctly.

#### 02.record-route-protocols

Similar to [01.record-route](#01record-route), but establishes a call for two
UAs that are using different protocols (i.e. UDP vs TCP), using double
Record-Routing.

#### 03.record-route-double

Similar to [01.record-route](#01record-route), but establishes a call between
two different interfaces in two different networks.

### Dialog

Checks call using dialog support.

#### 01.dialog

Performs a call with dialog support and stored in MySQL database. Verification steps are:
1. Place a call from a UAC to an UAS
2. Check the dialog has been created (dialog stats and `dlg_list` are checked)
3. Check that the dialog has been properly flushed in database
4. When the call finishes, we check the stats are properly cleared
5. We check the call as been removed from the database
6. SIPP scenarios check the Record-Route headers are present and no Route

#### 02.pinging

Similar to [01.dialog](#01simple), but checks that OPTIONS pinging is working.

#### 03.reinvite-pinging

Similar to [02.pinging](#02pinging), but checks that re-INVITE pinging is working.

#### 04.expire

Similar to [01.dialog](#01simple), but expires the dialog before a BYE is received.

#### 05.reinvite-auth

Runs a call through dialog where the re-INVITE is challenged by the UAC.

#### 06.auth-update

Runs a scenario when an UPDATE message is being sent while the calls is being
answered.

Runs a call through dialog where the re-INVITE is challenged by the UAC.
### Topology Hiding

Runs a set of calls using the topology hiding scenario, verifying that the UAS
are seeing only the next hop (OpenSIPS) in their signaling.

#### 01.th-no-dialog

Performs a call using topology hiding without dialog support. Verifies that:
1. UAs are only seeing next hop
2. Routing is correctly done
3. Topology hiding information is present in the Route and Record-Route headers

#### 02.th-no-dialog-username

Similar to [01.th-no-dialog](#01th-no-dialog), but passes the username in the
Contact header.

#### 03.th-dialog

Similar to [01.th-no-dialog](#01th-no-dialog), but uses the dialog module to
store topology hiding information.

#### 04.th-dialog-username

Similar to [03.th-dialog](#03th-dialog), but propagates the username
in the Contact header.

#### 05.th-dialog-did

Similar to [03.th-dialog](#03th-dialog), but pushes the dialog id in the
Contact username, rather than in the URI param.

#### 06.th-dialog-callid

Similar to [03.th-dialog](#03th-dialog), but changes the Call-ID of
the UAS leg.

#### 07.th-b2b

Simiar to [01.th-no-dialog](#01th-no-dialog) and [01.th-dialog](#01.th-dialog)
but performs the tests going through the B2B engine.

### B2B

Runs a set of tests against common B2B scenarios, verifying that the SIP flows
complete correctly.

#### 01.prepaid
Performs the Prepaid scenario, and checks that calls are properly executed.

#### 02.marketing
Performs the Marketing B2B scenario, and checks that the two entities are
executed according to the desired flow and scenario.

#### 03.refer-unattended-uac
Runs the REFER/unattended transfer scenario, triggering the transfer from the
UAC side.

#### 04.refer-unattended-uas
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but transfers from
the UAS side.

#### 05.refer-unattended-uac-fail
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but the transfer
fails, checking that all the entities are properly removed.

#### 06.refer-unattended-uas-fail
Same as [05.refer-unattended-uac-fail](#05refer-unattended-uac-fail), but the
transfer is attempted from the UAS side.

#### 07.refer-unattended-uac-notify
Same as [04.refer-unattended-uac](#03refer-unattended-uac), but enables RFC3515
NOTIFYs.

#### 08.refer-unattended-uas-notify
Same as [04.refer-unattended-uas](#04refer-unattended-uas), but enables RFC3515
NOTIFYs.

#### 09.refer-unattended-uac-notify-fail
Attempts a call transfer, but fails, checking that the call remains alive.

#### 10.refer-unattended-uas-notify-fail
Same as
[09.refer-unattended-uac-notify-fail](#09refer-unattended-uac-notify-fail), but
tries to transfer from UAS, which fails, then checks that the call remains
alive.

#### 11.refer-unattended-uac-prov
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but provides a
provisional media to the remaining participant.

#### 12.refer-unattended-uas-prov
Same as [04.refer-unattended-uas](#04refer-unattended-uac), but provides a
provisional media to the remaining participant.

#### 13.refer-unattended-uac-prov-fail
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but provides a
provisional media to the remaining participant, and the transfer fails.

#### 14.refer-unattended-uas-prov-fail
Same as [04.refer-unattended-uas](#04refer-unattended-uac), but provides a
provisional media to the remaining participant, and the transfer fails.

#### 15.refer-unattended-uac-prov-notify-fail
Same as
[09.refer-unattended-uac-notify-fail](#09refer-unattended-uac-notify-fail), but
provides a provisional media to the remaining participant.

#### 16.refer-unattended-uas-prov-notify-fail
Same as
[10.refer-unattended-uas-notify-fail](#10refer-unattended-uas-notify-fail), but
provides a provisional media to the remaining participant.

#### 17.refer-unattended-uac-mi
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but the transfer is
being triggered through MI.

#### 18.refer-unattended-uas-mi
Same as [04.refer-unattended-uas](#04refer-unattended-uas), but the transfer is
being triggered through MI.

#### 19.refer-unattended-uac-prov-mi
Same as [17.refer-unattended-uac-mi](#17refer-unattended-uac-mi), but
provides a provisional media to the remaining participant.

#### 20.refer-unattended-uas-prov-mi
Same as [18.refer-unattended-uas-mi](#18refer-unattended-uas-mi), but
provides a provisional media to the remaining participant.

#### 21.refer-unattended-uac-hold
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but
puts the remaining participant on hold first.

#### 22.refer-unattended-uac-no-late
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but does not
use late SDP with the new participant.

#### 23.refer-unattended-uac-no-late-prov
Same as [22.refer-unattended-uac-no-late](#22refer-unattended-uac-no-late), but
provides a provisional media to the remaining participant.

#### 24.refer-unattended-uac-retry
Same as [03.refer-unattended-uac](#03refer-unattended-uac), but the transfer
fails and the remaining participant is bridged with a new destination.

#### 25.top-hiding
Runs the internal topology hiding scenario.

#### 26.parking
Runs a simple parking scenario where a call is sent to a media server then picked
up by the called entity later.

#### 27.top-hiding-reject
Run the same as [25.top-hiding](#25top-hiding) scenario, but send re-INVITEs
which are rejected.

#### 28.top-hiding-overlapping
Run the same as [25.top-hiding](#25top-hiding) scenario, but send re-INVITEs
in such a manner that they overlap.

#### 29.refer-unattended-uas-491-uas
Runs a b2b transfer scenario where there is a race between a re-INVITE
generated by the caller and the one generated by the referee. In this case,
the referee/uac sends its re-INVITE after the 491.

#### 30.refer-unattended-uas-491-uac
Run the same as
[29.refer-unattended-uas-491-uas](#29refer-unattended-uas-491-uas)
scenario, but the referee no longer sends the re-INVITE, thus we retry
the bridging after 2.1-4s.

#### 31.refer-unattended-uac-notify-cancel
Run a transfer similar to 
[09.refer-unattended-uac-notify-fail](#09refer-unattended-uac-notify-fail), but
the call times out and the referee's call gets canceled.

#### 32.refer-unattended-uas-notify-cancel
Run a transfer similar to 
[10.refer-unattended-uas-notify-fail](#10refer-unattended-uas-notify-fail), but
the call times out and the referee's call gets canceled.

#### 33.refer-unattended-uac-notify-terminate
Run a transfer similar to 
[09.refer-unattended-uac-notify-fail](#09refer-unattended-uac-notify-fail), but
the remaining participant terminates the call during transfer.

#### 34.refer-unattended-uas-notify-terminate
Run a transfer similar to 
[10.refer-unattended-uas-notify-fail](#10refer-unattended-uas-notify-fail), but
the remaining participant terminates the call during transfer.

### UAC Auth

Verifies the behavior of uac_auth module.

#### 01.register-uac-auth-credentials-plain
Registers using the uac_auth module with credentials provided in plain text.

#### 02.register-uac-auth-credentials-ha1
Same as
[01.register-uac-auth-credentials-plain](#01register-uac-auth-credentials-plain),
but uses the credentials stored in the ha1 format.

#### 03.register-uac-auth-avp-plain
Same as
[01.register-uac-auth-credentials-plain](#01register-uac-auth-credentials-plain),
but takes the credentials in plain text through script AVPs.

#### 04.register-uac-auth-avp-ha1
Same as
[01.register-uac-auth-credentials-plain](#01register-uac-auth-credentials-plain),
but takes the credentials in ha1 format through script AVPs.

#### 05.register-uac-auth-int-credentials-plain
Same as
[01.register-uac-auth-credentials-plain](#01register-uac-auth-credentials-plain),
but uses authentication integrity (`auth-int`) for quality of protection
(`qop`).

#### 06.register-uac-auth-int-credentials-ha1
Same as
[02.register-uac-auth-credentials-ha1](#02register-uac-auth-credentials-ha1),
but uses authentication integrity (`auth-int`) for quality of protection
(`qop`).

#### 07.register-uac-auth-int-avp-plain
Same as
[03.register-uac-auth-avp-plain](#03register-uac-auth-avp-plain),
but uses authentication integrity (`auth-int`) for quality of protection
(`qop`).

#### 08.register-uac-auth-int-credentials-ha1
Same as
[04.register-uac-auth-avp-ha1](#04register-uac-auth-avp-ha1),
but uses authentication integrity (`auth-int`) for quality of protection
(`qop`).

#### 09.register-uac-auth-auth-int-credentials-plain
Same as
[01.register-uac-auth-credentials-plain](#01register-uac-auth-credentials-plain), and
[05.register-uac-auth-int-credentials-plain](#05register-uac-auth-int-credentials-plain),
but server supports both authentication (`auth`) and uses authentication
integrity (`auth-int`) for quality of protection (`qop`).

#### 10.register-uac-auth-auth-int-credentials-ha1
Same as
[02.register-uac-auth-credentials-ha1](#02register-uac-auth-credentials-ha1), and
[06.register-uac-auth-int-credentials-ha1](#06register-uac-auth-int-credentials-ha1),
but server supports both authentication (`auth`) and uses authentication
integrity (`auth-int`) for quality of protection (`qop`).

#### 11.register-uac-auth-auth-int-avp-plain
Same as
[03.register-uac-auth-avp-plain](#03register-uac-auth-avp-plain), and
[07.register-uac-auth-int-avp-plain](#07register-uac-auth-int-avp-plain),
but server supports both authentication (`auth`) and uses authentication
integrity (`auth-int`) for quality of protection (`qop`).

#### 12.register-uac-auth-auth-int-credentials-ha1
Same as
[04.register-uac-auth-avp-ha1](#04register-uac-auth-avp-ha1), and
[08.register-uac-auth-int-avp-ha1](#08register-uac-auth-int-avp-ha1),
but server supports both authentication (`auth`) and uses authentication
integrity (`auth-int`) for quality of protection (`qop`).

#### 13.rr-auth-invite-uas
Places a call where the UAS authenticates for the initial INVITE.

#### 14.rr-auth-bye-uas
Places a call where the UAS authenticates for the in-dialog BYE.

#### 15.rr-auth-bye-uac
Places a call where the UAC authenticates for the in-dialog BYE.

#### 16.dialog-auth-invite-uas
Same as
[13.rr-auth-invite-uas](#13.rr-auth-invite-uas), but authentication changes
are stored in dialog.

#### 17.dialog-auth-reinvite-uas
Places a call where the UAS authenticates for the in-dialog reINVITE.

#### 18.dialog-auth-bye-uas
Places a call where the UAS authenticates for the in-dialog BYE.

#### 19.dialog-auth-invite-bye-uas
Places a call where the UAS authenticates the initial INVITE and the BYE
messages.

#### 20.dialog-auth-invite-reinvite-bye-uas
Places a call where the UAS authenticates the initial INVITE, reINVITE and the
BYE messages.

#### 21.dialog-auth-bye-uac
Places a call where the UAC authenticates for the in-dialog BYE.

#### 22.dialog-auth-reinvite-uac
Places a call where the UAC authenticates for the in-dialog reINVITE.

#### 23.dialog-auth-reinvite-bye-uac
Places a call where the UAC authenticates for both in-dialog reINVITE and BYE.

#### 24.dialog-auth-reinvite-uac-reinvite-uas
Places a call where both UAC and UAS authenticates for the in-dialog reINVITE.

#### 25.dialog-auth-reinvite-uas-reinvite-uac
Same as
[24.dialog-auth-reinvite-uac-reinvite-uas](#24dialog-auth-reinvite-uac-reinvite-uas),
but reINVITEs are sent in reversed order.

#### 26.dialog-auth-reinvite-uac-reinvite-uas-bye-uas
Places a call where both UAC and UAS authenticates for the in-dialog reINVITE
and the BYE is authenticated by the UAS.

#### 27.dialog-auth-reinvite-uac-reinvite-uas-bye-uac
Same as
[26.dialog-auth-reinvite-uac-reinvite-uas-bye-uas](#26dialog-auth-reinvite-uac-reinvite-uas-bye-uas),
but BYE is authenticated by the UAC.

### Stir and shaken

:warning: Scenarios are being created for French regulations

#### 01.auth-simple
A basic stir and shaken authentication<br>
It use a compatible Self-Signed STIR/SHAKEN Certificate [(info here)](https://blog.opensips.org/2022/10/31/how-to-generate-self-signed-stir-shaken-certificates)<br>
:warning: This scenario use a specific version of [opensips-cli](https://hub.docker.com/r/allomediadocker/opensips-cli)
(more explanations in scenario's README)

#### 02.auth-diverted-cached
Same as
[01.auth-simple](#01auth-simple), but add processing of Diversion header, public key caching, store private key in separate file (more explanations in scenario's README)<br>

#### 03.auth-issue-bypass-token
Same as
[01.auth-simple](#01auth-simple), $var(cert) deleted to force stir_shaken_auth function in error and automatically add P-Identity-Bypass header. (more explanations in scenario's README)<br>

#### 04.verify-200
Places a call with correct Identity header

#### 05.verify-200-anonymous
Places a call with correct Identity header but with `From` Anonymous

#### 06.verify-error-400-wrong-from
Places a call with wrong orig in conf (more explanations in scenario's README)

#### 07.verify-error-400-wrong-from-no-kill-call
Places a call with wrong orig in conf, but not kill call (more explanations in scenario's README)

#### 08.verify-error-403-wrong-date
Places a call with wrong Date header (more explanations in scenario's README)

#### 09.verify-error-403-wrong-iat
Places a call with wrong iat token (more explanations in scenario's README)

#### 10.verify-error-428-no-identity
Places a call without Identity header (more explanations in scenario's README)

#### 11.verify-error-436-no-info
Places a call without Identity's info param (more explanations in scenario's README)

#### 12.verify-error-436-token-no-4-params
Places a call without 4 params in Identity header (more explanations in scenario's README)

#### 13.verify-error-436-x5u-diff-info
Places a call with x5u and info are different (more explanations in scenario's README)

#### 14.verify-error-437-no-alg
Places a call without alg identity param (more explanations in scenario's README)

#### 15.verify-error-437-wrong-alg
Places a call with wrong alg identity param (more explanations in scenario's README)

#### 16.verify-error-437-wrong-header-alg
Places a call without alg token param (more explanations in scenario's README)

#### 17.verify-error-437-wrong-header-typ
Places a call without typ token param (more explanations in scenario's README)

#### 18.verify-error-437-cert-expired
Places a call with expired certificate (more explanations in scenario's README)

#### 19.verify-error-437-cert-in-future
Places a call with certificate starts in 2025 (more explanations in scenario's README)

#### 20.verify-error-438-identity-more-4-params
Places a call with 5 params in Identity header (more explanations in scenario's README)

#### 21.verify-error-438-no-ppt
Places a call without ppt identity param (more explanations in scenario's README)

#### 22.verify-error-438-wrong-ppt
Places a call with wrong ppt identity param (more explanations in scenario's README)

#### 23.verify-error-438-wrong-header-ppt
Places a call without ppt token param (more explanations in scenario's README)

#### 24.verify-error-438-wrong-attest
Places a call with wrong attest (more explanations in scenario's README)

#### 25.verify-error-438-orig-diff-from
Places a call with orig and from are different (more explanations in scenario's README)

#### 26.verify-error-438-dest-diff-to
Places a call with dest and To are different (more explanations in scenario's README)

#### 27.acc-stats-200
Places a call with correct Identity and push stats in ACC (more explanations in scenario's README)

#### 28.acc-stats-error-403-wrong-iat
Places a call with wrong iat token and push stats in ACC (more explanations in scenario's README)

#### 29.acc-stats-error-403-no-kill-call
Places a call with wrong iat token, but not kill call and push stats in ACC (more explanations in scenario's README)

### Accounting

Tests accounting functionalities.

#### 01.db-transaction

Places a call and checks the transcation accounting information in a database backend.

#### 02.db-transaction-failed

Places a call and checks the failed transcation accounting information in a database backend.

#### 03.db-cdr

Places a call and checks the CDR accounting information in a database backend.

### Presence

Tests presence functionalities.

#### 01.presence

Tests a basic PUBLISH-SUBSCRIBE-NOTIFY sequence for the "presence" event, using
xml bodies.

### Permissions

Tests the behavior of the permissions module.

#### 01.check-address

Tests if a call is accepted based on the source address.

#### 02.check-address-fail

Tests if a call is rejected based on the source address.

## Execution

Install the `sipssert` tool and run it in the main directory.
```
sipssert *
```

You can optionally run only one tests set:
```
sipssert registration
```
