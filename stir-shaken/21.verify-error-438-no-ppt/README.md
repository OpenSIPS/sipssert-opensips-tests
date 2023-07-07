# Diagram
```mermaid
sequenceDiagram
    uac-sipp-stir-shaken->>+opensips: With identity header
    opensips-->>-uac-sipp-stir-shaken: 438 Invalid Identity Header
```

# Explanations:
No `ppt` param in Identity header
```
Identity: [stir_and_shaken_jwt];info=<[stir_and_shaken_info]>;alg=[stir_shaken_alg]
```

*Test from **MAN_Mode_operatoire_Mecanisme_de_Confiance_v1.7_20230616.pdf** (P59 / line 18)*

# Future
