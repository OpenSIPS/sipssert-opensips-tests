# Diagram
```mermaid
sequenceDiagram
    uac-sipp-stir-shaken->>+opensips: With identity header
    opensips-->>-uac-sipp-stir-shaken: 403 Stale Date
```

# Explanations:
We forced future Date header in UAC
```php
Date: Tue, 22 Sep 2150 23:29:00 GMT
```
