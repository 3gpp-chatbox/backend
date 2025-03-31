```mermaid
graph LR
    start((Start)) --> 1(UE sends REGISTRATION REQUEST);
    1 --> 2(UE: Start/Stop Timers);
    2 --> 3{AMF: Common Procedures?};
    3 --> 4{AMF: Registration Accepted?};

    4 -- Yes: Send REGISTRATION ACCEPT --> 5(AMF sends REGISTRATION ACCEPT);
    4 -- No: Send REGISTRATION REJECT --> 9(AMF sends REGISTRATION REJECT);

    5 --> 6(UE: Receive REGISTRATION ACCEPT);
    5 -- 5G-GUTI or SOR IE included --> 5G_GUTI(AMF: Start T3550);
    5G_GUTI --> end_success((End Success));
    6 --> 7{UE: REGISTRATION COMPLETE?};

    7 -- Yes: Send REGISTRATION COMPLETE --> 8(UE sends REGISTRATION COMPLETE);
    7 -- No: Do not send REGISTRATION COMPLETE --> end_success;

    8 --> 10(AMF: Stop T3550, 5GMM-REGISTERED);
    9 --> 11(UE: Actions based on 5GMM cause);

    10 --> end_success;
    11 --> end_failure((End Failure));

    2 -- T3510 Starts --> 12{UE: T3510 Timeout?};
    12 -- Timeout --> 13{UE: Retry < 5?};

    13 -- Yes: Start T3511 --> end_failure;
    13 -- No: Retry = 5 --> 14{UE: T3502 != 0?};

    14 -- Yes: Start T3502 --> end_failure;
    14 -- No: T3502 = 0 --> end_failure;

    classDef process fill:#f9f,stroke:#333,stroke-width:2px
    classDef decision fill:#ccf,stroke:#333,stroke-width:2px
    classDef end fill:#cfc,stroke:#333,stroke-width:2px
    class 1,2,5,6,8,9,10,11,5G_GUTI process
    class 3,4,7,12,13,14 decision
    class start,end_success,end_failure end
```