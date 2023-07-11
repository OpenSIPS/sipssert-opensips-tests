# Diagram
```mermaid
sequenceDiagram
    uac-sipp-stir-shaken->>+opensips: With identity header
    opensips-->>-uac-sipp-stir-shaken: 437 Unsupported Credential
```

# Explanations:
Wrong `typ` in token's header, change it in scenario.yml
```yml
stir_shaken_typ: "poussport"
```

*Test from **MAN_Mode_operatoire_Mecanisme_de_Confiance_v1.7_20230616.pdf** (P59 / line 11)*

# Future
