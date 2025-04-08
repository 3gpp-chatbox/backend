```mermaid
graph TD
    start(Start) --> 1[UE sends REGISTRATION REQUEST]
    1 --> timer_T3510_start[Start T3510]
    1 -- "Condition: If timer T3502 is running" --> timer_T3502_stop[Stop T3502]
    1 -- "Condition: If timer T3511 is running" --> timer_T3511_stop[Stop T3511]
    timer_T3510_start --> 2[AMF processes REGISTRATION REQUEST]
    2 --> 3[AMF sends REGISTRATION ACCEPT]
    3 --> timer_T3550_start[Start T3550]
    timer_T3550_start --> 4[UE receives REGISTRATION ACCEPT]
    4 --> timer_T3510_stop[Stop T3510]
    timer_T3510_stop --> decision_need_to_send_registration_complete{Change of network slicing information?}
    decision_need_to_send_registration_complete -- Yes --> 5[AMF receives REGISTRATION COMPLETE]
    decision_need_to_send_registration_complete -- No --> end(End)
    5 --> timer_T3550_stop[Stop T3550]
    timer_T3550_stop --> end(End)
    
    style start fill:#f9f,stroke:#333,stroke-width:2px
    style end fill:#f9f,stroke:#333,stroke-width:2px
```