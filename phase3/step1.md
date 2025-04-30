# Registration procedure for initial registration

```mermaid
graph LR
    classDef state fill:#e6f3ff,stroke:#333,stroke-width:2px,color:#000;
    classDef action fill:#ffebee,stroke:#333,stroke-width:1px,color:#000;
    classDef condition fill:#fff9e6,stroke:#333,stroke-width:1px,color:#000;
    classDef decision fill:#e6ffe6,stroke:#333,stroke-width:1px,color:#000;

    n1["5GMM-DEREGISTERED"]
    class n1 state
    n2["Stop T3502(if running), Stop T3511(if running), Send REGISTRATION REQUEST, Start T3510"]
    class n2 action
    n3["5GMM-REGISTERED-INITIATED"]
    class n3 state
    n4["Stop T3510, Reset counters, Store context, Set 5GS update status 5U1 UPDATED"]
    class n4 action
    n5{"Need to send REGISTRATION COMPLETE?"}
    class n5 condition
    n6["Send REGISTRATION COMPLETE"]
    class n6 action
    n7["5GMM-REGISTERED"]
    class n7 state
    n8{"Handle REGISTRATION REJECT based on Cause"}
    class n8 decision
    n9["Action for REJECT Cause #3/#6/#7"]
    class n9 action
    n10["5GMM-DEREGISTERED.NO-SUPI"]
    class n10 state
    n11["Action for REJECT Cause #11/#73"]
    class n11 action
    n12["5GMM-DEREGISTERED.PLMN-SEARCH"]
    class n12 state
    n13["Action for REJECT Cause #12/#13/#15/#78"]
    class n13 action
    n14["5GMM-DEREGISTERED.LIMITED-SERVICE"]
    class n14 state
    n15["Action for REJECT Cause #22"]
    class n15 action
    n16["5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION"]
    class n16 state
    n17["Action for REJECT Cause #27/#72"]
    class n17 action
    n18["Action for REJECT Cause #31"]
    class n18 action
    n19["5GMM-DEREGISTERED.NO-CELL-AVAILABLE"]
    class n19 state
    n20["Action for REJECT Cause #62/#79/#80/#81/#82"]
    class n20 action
    n21["Action for REJECT Cause #74/#75"]
    class n21 action
    n22["Action for REJECT Cause #76"]
    class n22 action
    n23["Handle Abnormal Case (T3510 expiry / Lower Layer Failure / Abnormal Reject)"]
    class n23 action
    n24{"Not Emergency Registration AND Not Emergency PDU Session Handoff"}
    class n24 condition
    n25["Increment registration attempt counter (unless = 5)"]
    class n25 action
    n26{"registration attempt counter < 5"}
    class n26 condition
    n27["Start T3511"]
    class n27 action
    n28{"registration attempt counter = 5"}
    class n28 condition
    n29["Delete context, Set 5GS update status 5U2 NOT UPDATED, Start T3502 (if value > 0)"]
    class n29 action
    n30["Abort procedure, Re-initiate procedure"]
    class n30 action
    n31{"New TAI in TAI List?"}
    class n31 condition
    n32["Abort procedure, Initiate Mobility Registration Update"]
    class n32 action
    n1-->|"Trigger: Need for Initial Registration"| n2
    n2-->|"Action Complete"| n3
    n3-->|"Receive REGISTRATION ACCEPT"| n4
    n4-->|"Action Complete"| n5
    n5-->|"Yes"| n6
    n5-->|"No"| n7
    n6-->|"Action Complete"| n7
    n3-->|"Receive REGISTRATION REJECT"| n8
    n8-->|"Cause #3/#6/#7"| n9
    n9-->|"Action Complete"| n10
    n8-->|"Cause #11/#73"| n11
    n11-->|"Action Complete"| n12
    n8-->|"Cause #12/#13/#15/#78"| n13
    n13-->|"Action Complete (Enter LIMITED-SERVICE)"| n14
    n13-->|"Action Complete (Enter PLMN-SEARCH)"| n12
    n8-->|"Cause #22"| n15
    n15-->|"Action Complete"| n16
    n8-->|"Cause #27/#72"| n17
    n17-->|"Action Complete"| n14
    n8-->|"Cause #31"| n18
    n18-->|"Action Complete"| n19
    n8-->|"Cause #62/#79/#80/#81/#82"| n20
    n20-->|"Action Complete (Enter ATTEMPTING-REGISTRATION)"| n16
    n20-->|"Action Complete (Enter PLMN-SEARCH)"| n12
    n8-->|"Cause #74/#75"| n21
    n21-->|"Action Complete"| n12
    n8-->|"Cause #76"| n22
    n22-->|"Action Complete (Enter LIMITED-SERVICE)"| n14
    n22-->|"Action Complete (Enter PLMN-SEARCH)"| n12
    n3-->|"T3510 expires"| n23
    n3-->|"Lower layer failure/release"| n23
    n3-->|"Receive REGISTRATION REJECT (Abnormal Case)"| n23
    n23-->|"Action Complete"| n24
    n24-->|"Condition met"| n25
    n25-->|"Action Complete"| n26
    n26-->|"Condition met"| n27
    n27-->|"Action Complete"| n16
    n25-->|"Action Complete"| n28
    n28-->|"Condition met"| n29
    n29-->|"Action Complete (Enter ATTEMPTING-REGISTRATION)"| n16
    n29-->|"Action Complete (Enter PLMN-SEARCH)"| n12
    n16-->|"T3511 expires"| n1
    n16-->|"T3346 expires"| n1
    n16-->|"T3502 expires (value was > 0)"| n1
    n3-->|"TAI Change before REG ACCEPT/REJECT"| n30
    n30-->|"Action Complete"| n1
    n6-->|"TAI Change after ACCEPT, before COMPLETE sent"| n31
    n31-->|"Yes (Continue sending COMPLETE)"| n6
    n31-->|"No"| n32
    n32-->|"Action Complete (Leads to Mobility Update)"| n1
    n3-->|"REGISTRATION REQUEST transmission failure"| n1
    n3-->|"UE initiated de-registration required"| n1
    n3-->|"Receive DEREGISTRATION REQUEST (Ignore De-reg, Continue Reg)"| n3
```