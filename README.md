# OpenSIPS Tests

This project contains a set of tests that are being performed to test the
behavior of the [OpenSIPS](https://www.opensips.org) SIP Server under certain
scenarios.

Tests are being executed by the [SIPssert](https://github.com/OpenSIPS/sipssert) tool

## Tests

There are multiple tests sets available, depending on what is their main
testing focus:

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

Similar to [01.record-route](01record-route), but establishes a call for two
UAs that are using different protocols (i.e. UDP vs TCP), using double
Record-Routing.

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

Simiar to [01.th-no-dialog](#01th-no-dialog) and [01.th-dialog](01.th-dialog)
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
Same as [03.refer-unattended-uac](03refer-unattended-uac), but transfers from
the UAS side.

#### 05.refer-unattended-uac-fail
Same as [03.refer-unattended-uac](03refer-unattended-uac), but the transfer
fails, checking that all the entities are properly removed.

#### 06.refer-unattended-uas-fail
Same as [05.refer-unattended-uac-fail](05refer-unattended-uac-fail), but the
transfer is attempted from the UAS side.

#### 07.refer-unattended-uac-notify
Same as [04.refer-unattended-uac](03refer-unattended-uac), but enables RFC3515
NOTIFYs.

#### 08.refer-unattended-uas-notify
Same as [04.refer-unattended-uas](04refer-unattended-uas), but enables RFC3515
NOTIFYs.

#### 09.refer-unattended-uac-notify-fail
Attempts a call transfer, but fails, checking that the call remains alive.

#### 10.refer-unattended-uas-notify-fail
Same as
[09.refer-unattended-uac-notify-fail](09refer-unattended-uac-notify-fail), but
tries to transfer from UAS, which fails, then checks that the call remains
alive.

#### 11.refer-unattended-uac-prov
Same as [03.refer-unattended-uac](03refer-unattended-uac), but provides a
provisional media to the remaining participant.

#### 12.refer-unattended-uas-prov
Same as [04.refer-unattended-uas](04refer-unattended-uac), but provides a
provisional media to the remaining participant.

#### 13.refer-unattended-uac-prov-fail
Same as [03.refer-unattended-uac](03refer-unattended-uac), but provides a
provisional media to the remaining participant, and the transfer fails.

#### 14.refer-unattended-uas-prov-fail
Same as [04.refer-unattended-uas](04refer-unattended-uac), but provides a
provisional media to the remaining participant, and the transfer fails.

#### 15.refer-unattended-uac-prov-notify-fail
Same as
[09.refer-unattended-uac-notify-fail](09refer-unattended-uac-notify-fail), but
provides a provisional media to the remaining participant.

#### 16.refer-unattended-uas-prov-notify-fail
Same as
[10.refer-unattended-uas-notify-fail](10refer-unattended-uas-notify-fail), but
provides a provisional media to the remaining participant.

## Execution

Install the `sipssert` tool and run it in the main directory.
```
sipssert *
```

You can optionally run only one tests set:
```
sipssert registration
```
