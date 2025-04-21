# Registration procedure for initial registration

```mermaid
graph LR
    classDef state fill:#e6f3ff,stroke:#333,stroke-width:2px,color:#000;
    classDef event fill:#ffebee,stroke:#333,stroke-width:1px,color:#000;

    node1["5GMM-DEREGISTERED"]
    class node1 state
    node2["Event_InitialRegistration_Trigger"]
    class node2 event
    node3["5GMM-REGISTERED-INITIATED"]
    class node3 state
    node4["Receive_REGISTRATION_ACCEPT"]
    class node4 event
    node5["5GMM-REGISTERED"]
    class node5 state
    node6["5GMM-REGISTERED.LIMITED-SERVICE"]
    class node6 state
    node7["5GMM-REGISTERED.PLMN-SEARCH"]
    class node7 state
    node8["Receive_REGISTRATION_REJECT"]
    class node8 event
    node9["5GMM-DEREGISTERED.NO-SUPI"]
    class node9 state
    node10["5GMM-DEREGISTERED.PLMN-SEARCH"]
    class node10 state
    node11["5GMM-DEREGISTERED.LIMITED-SERVICE"]
    class node11 state
    node12["5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION"]
    class node12 state
    node13["5GMM-DEREGISTERED.NO-CELL-AVAILABLE"]
    class node13 state
    node14["Event_T3510_Expiry"]
    class node14 event
    node15["Event_LowerLayer_Failure"]
    class node15 event
    node16["Event_UE_Deregistration_Required"]
    class node16 event
    node17["Receive_DEREGISTRATION_REQUEST"]
    class node17 event
    node18["Event_TAI_Change"]
    class node18 event
    node19["Event_Localized_Service_Access_Disallowed"]
    class node19 event
    node20["Event_T3511_Expiry"]
    class node20 event
    node21["Event_T3346_Expiry"]
    class node21 event
    node22["Event_REG_COMPLETE_Tx_Failure"]
    class node22 event
    node23["Event_TAI_Change_After_Accept"]
    class node23 event
    node24["Event_Access_Barred"]
    class node24 event
    node25["Event_REG_REQUEST_Tx_Failure"]
    class node25 event
    node26["Event_SOR_Requires_Release"]
    class node26 event
    node28["Event_REG_COMPLETE_Tx_Failure_TAI_Change"]
    class node28 event
    5GMM-DEREGISTERED --> Event_InitialRegistration_Trigger
    Event_InitialRegistration_Trigger --> 5GMM-REGISTERED-INITIATED
    5GMM-REGISTERED-INITIATED --> Receive_REGISTRATION_ACCEPT
    Receive_REGISTRATION_ACCEPT --> 5GMM-REGISTERED
    Receive_REGISTRATION_ACCEPT --> 5GMM-REGISTERED.LIMITED-SERVICE
    Receive_REGISTRATION_ACCEPT --> 5GMM-REGISTERED.PLMN-SEARCH
    5GMM-REGISTERED-INITIATED --> Receive_REGISTRATION_REJECT
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.NO-SUPI
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.NO-CELL-AVAILABLE
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    5GMM-REGISTERED-INITIATED --> Event_T3510_Expiry
    Event_T3510_Expiry --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Event_T3510_Expiry --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Event_T3510_Expiry --> 5GMM-DEREGISTERED.PLMN-SEARCH
    5GMM-REGISTERED-INITIATED --> Event_LowerLayer_Failure
    Event_LowerLayer_Failure --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Event_LowerLayer_Failure --> 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION
    Event_LowerLayer_Failure --> 5GMM-DEREGISTERED.PLMN-SEARCH
    5GMM-REGISTERED-INITIATED --> Event_UE_Deregistration_Required
    Event_UE_Deregistration_Required --> 5GMM-DEREGISTERED
    5GMM-REGISTERED-INITIATED --> Receive_DEREGISTRATION_REQUEST
    Receive_DEREGISTRATION_REQUEST --> 5GMM-REGISTERED-INITIATED
    5GMM-REGISTERED-INITIATED --> Event_TAI_Change
    Event_TAI_Change --> 5GMM-DEREGISTERED
    5GMM-REGISTERED-INITIATED --> Event_Localized_Service_Access_Disallowed
    Event_Localized_Service_Access_Disallowed --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    Event_Localized_Service_Access_Disallowed --> 5GMM-DEREGISTERED.PLMN-SEARCH
    5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION --> Event_T3511_Expiry
    Event_T3511_Expiry --> 5GMM-DEREGISTERED
    5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION --> Event_T3346_Expiry
    Event_T3346_Expiry --> 5GMM-DEREGISTERED
    5GMM-REGISTERED --> Event_REG_COMPLETE_Tx_Failure
    Event_REG_COMPLETE_Tx_Failure --> 5GMM-REGISTERED
    5GMM-REGISTERED --> Event_TAI_Change_After_Accept
    Event_TAI_Change_After_Accept --> 5GMM-REGISTERED
    5GMM-DEREGISTERED --> Event_Access_Barred
    Event_Access_Barred --> 5GMM-DEREGISTERED
    5GMM-REGISTERED-INITIATED --> Event_REG_REQUEST_Tx_Failure
    Event_REG_REQUEST_Tx_Failure --> 5GMM-DEREGISTERED
    5GMM-REGISTERED --> Event_SOR_Requires_Release
    Event_SOR_Requires_Release --> 5GMM-DEREGISTERED
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.PLMN-SEARCH
    Receive_REGISTRATION_REJECT --> 5GMM-DEREGISTERED.LIMITED-SERVICE
    5GMM-REGISTERED --> Event_REG_COMPLETE_Tx_Failure_TAI_Change
    Event_REG_COMPLETE_Tx_Failure_TAI_Change --> 5GMM-REGISTERED
```