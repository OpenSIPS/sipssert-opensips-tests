# OpenSIPS Tests

This project contains a set of tests that are being performed to test the
behavior of the [OpenSIPS](https://www.opensips.org) SIP Server under certain
scenarios.

Tests are being executed by the [SIPssert](https://github.com/OpenSIPS/sipssert) tool

## Tests

The current tests are available:

### 01.registration-no-db

Performs registrations tests when no database is involved. Verification steps are:
1. Register to OpenSIPS using sipp
2. Check the registration exists using OpenSIPS CLI
3. Unregister using sipp
4. Check the registration dissapeared

### 02.registration-db

Performs registrations tests using MySQL database. Verification steps are:
1. Register to OpenSIPS using sipp
2. Check the registration exists using OpenSIPS CLI
3. Check the registration exists in DB after flush timeout passes
4. Unregister using sipp
5. Check the registration dissapeared
6. Checks the database is empty after timer flush

### 03.registration-expire

Same as [02.registration-db](#02registration-db), but leaves the contact to expire.
1. Checks through MI that the registration was removed
2. Checks the database is empty after timer flush

## Execution

Install the `sipssert` tool and run it in the main directory.
```
sipssert .
```
