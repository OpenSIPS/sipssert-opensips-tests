# Diagram
```mermaid
sequenceDiagram
    uac-sipp-stir-shaken->>+opensips: With identity header
    opensips->>+uas-sipp: Without identity header
    uas-sipp-->>-opensips: 200 OK
    opensips-->>-uac-sipp-stir-shaken: 200 OK (with Reason)
```

# Explanations:
- We forced wrong orig number format
```php
stir_shaken_verify($var(cert), $var(err_code), $var(err_reason), "++4", "$tU");
```

- In opensips.cfg (during the tests phase)
```php
$var(kill_calls) = false;
```

- Result
Not kill call but just add reason header into `200 OK` to UAC
```php
Reason: SIP; cause=400; text="Bad Request"
```
