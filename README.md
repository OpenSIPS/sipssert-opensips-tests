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

## Execution

Install the `sipssert` tool and run it in the main directory.
```
sipssert *
```

You can optionally run only one tests set:
```
sipssert registration
```
