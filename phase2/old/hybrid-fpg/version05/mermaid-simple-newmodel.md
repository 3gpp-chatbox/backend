```mermaid
graph TD;
  state_ue_deregistered["UE State: 5GMM-DEREGISTERED"];
  event_ue_initiate_reg["UE Initiates Registration Procedure"];
  event_ue_sends_reg_req["UE Sends REGISTRATION REQUEST message to AMF"];
  event_ue_starts_t3510["UE Starts Timer T3510"];
  event_ue_stops_timers["UE Stops Timers T3502, T3511 (if running)"];
  event_ue_starts_t3519["UE Starts Timer T3519 (if SUCI included and timer not running)"];
  event_amf_receives_reg_req["AMF Receives REGISTRATION REQUEST message"];
  state_amf_processing["AMF Processing Registration Request (Common Procedures)"];
  event_amf_accepts_reg["AMF Accepts Initial Registration Request"];
  event_amf_rejects_reg["AMF Rejects Initial Registration Request"];
  event_amf_sends_reg_accept["AMF Sends REGISTRATION ACCEPT message to UE"];
  event_amf_starts_t3550["AMF Starts Timer T3550 (if ACK required)"];
  state_amf_common_proc_initiated["AMF State: 5GMM-COMMON-PROCEDURE-INITIATED"];
  event_ue_receives_reg_accept["UE Receives REGISTRATION ACCEPT message"];
  event_ue_stops_t3510["UE Stops Timer T3510"];
  state_ue_registered["UE State: 5GMM-REGISTERED"];
  event_ue_sends_reg_complete["UE Sends REGISTRATION COMPLETE message to AMF (if required)"];
  event_amf_receives_reg_complete["AMF Receives REGISTRATION COMPLETE message"];
  event_amf_stops_t3550["AMF Stops Timer T3550"];
  state_amf_registered["AMF State: 5GMM-REGISTERED"];
  event_amf_sends_reg_reject["AMF Sends REGISTRATION REJECT message to UE"];
  event_ue_receives_reg_reject["UE Receives REGISTRATION REJECT message"];
  state_ue_processing_reject["UE Processing REGISTRATION REJECT based on cause"];
  event_t3510_expiry["Timer T3510 Expires"];
  state_ue_attempting_reg["UE State: 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION"];
  event_ue_starts_t3511["UE Starts Timer T3511"];
  event_t3511_expiry["Timer T3511 Expires"];
  event_ue_starts_t3502["UE Starts Timer T3502"];
  state_ue_plmn_search["UE State: 5GMM-DEREGISTERED.PLMN-SEARCH"];
  event_t3550_expiry["Timer T3550 Expires"];
  state_end_success["Registration Procedure Successfully Completed"];
  state_end_failure["Registration Procedure Failed or Aborted"];
  state_ue_deregistered -->|UE decides to initiate initial registration| event_ue_initiate_reg;
  event_ue_initiate_reg -->|UE constructs and sends REGISTRATION REQUEST| event_ue_sends_reg_req;
  event_ue_sends_reg_req -->|Triggered by sending REGISTRATION REQUEST| event_ue_starts_t3510;
  event_ue_sends_reg_req -->|Triggered by sending REGISTRATION REQUEST| event_ue_stops_timers;
  event_ue_sends_reg_req -->|If SUCI is included and T3519 not running| event_ue_starts_t3519;
  event_ue_sends_reg_req -->|Message transmission over N1 interface| event_amf_receives_reg_req;
  event_amf_receives_reg_req -->|AMF begins processing the request| state_amf_processing;
  state_amf_processing -->|AMF determines the request is acceptable after common procedures| event_amf_accepts_reg;
  state_amf_processing -->|AMF determines the request is not acceptable| event_amf_rejects_reg;
  event_amf_accepts_reg -->|AMF sends the REGISTRATION ACCEPT message| event_amf_sends_reg_accept;
  event_amf_sends_reg_accept -->|If REGISTRATION ACCEPT includes IEs requiring acknowledgement| event_amf_starts_t3550;
  event_amf_starts_t3550 -->|AMF enters state waiting for REGISTRATION COMPLETE| state_amf_common_proc_initiated;
  event_amf_sends_reg_accept -->|Message transmission over N1 interface| event_ue_receives_reg_accept;
  event_ue_receives_reg_accept -->|UE stops timer upon receiving ACCEPT| event_ue_stops_t3510;
  event_ue_stops_t3510 -->|UE resets counter, enters 5GMM-REGISTERED, sets status| state_ue_registered;
  state_ue_registered -->|If REGISTRATION ACCEPT requires acknowledgement| event_ue_sends_reg_complete;
  state_ue_registered -->|If REGISTRATION ACCEPT does not require acknowledgement| state_end_success;
  event_ue_sends_reg_complete -->|Message transmission over N1 interface| event_amf_receives_reg_complete;
  event_amf_receives_reg_complete -->|AMF stops timer upon receiving COMPLETE| event_amf_stops_t3550;
  event_amf_stops_t3550 -->|AMF enters 5GMM-REGISTERED state| state_amf_registered;
  state_amf_registered -->|AMF side registration complete| state_end_success;
  state_amf_common_proc_initiated -->|Waiting for REGISTRATION COMPLETE| event_amf_receives_reg_complete;
  event_amf_rejects_reg -->|AMF sends the REGISTRATION REJECT message| event_amf_sends_reg_reject;
  event_amf_sends_reg_reject -->|Message transmission over N1 interface| event_ue_receives_reg_reject;
  event_ue_receives_reg_reject -->|UE stops timer upon receiving REJECT| event_ue_stops_t3510;
  event_ue_stops_t3510 -->|UE processes the reject cause| state_ue_processing_reject;
  state_ue_processing_reject -->|"Based on specific reject cause (e.g., #3, #6, #7, #11, #27, etc.) leading to failure/deregistration"| state_end_failure;
  state_ue_processing_reject -->|"Based on specific reject cause (e.g., #22, #62) leading to retry attempt"| state_ue_attempting_reg;
  state_ue_processing_reject -->|"Based on specific reject cause (e.g., #11, #73, #74, #75) leading to PLMN search"| state_ue_plmn_search;
  event_ue_starts_t3510 -->|Timer T3510 runs out before response received| event_t3510_expiry;
  event_t3510_expiry -->|Registration attempt counter < 5| event_ue_starts_t3511;
  event_ue_starts_t3511 -->|UE enters state to wait for T3511 expiry| state_ue_attempting_reg;
  state_ue_attempting_reg -->|Timer T3511 runs out| event_t3511_expiry;
  event_t3511_expiry -->|UE re-attempts registration procedure| event_ue_sends_reg_req;
  event_t3510_expiry -->|Registration attempt counter reaches 5| event_ue_starts_t3502;
  event_ue_starts_t3502 -->|UE enters PLMN search or waits for T3502 expiry| state_ue_plmn_search;
  state_ue_plmn_search -->|"Further actions (PLMN selection, T3502 expiry) outside scope or lead to failure"| state_end_failure;
  state_amf_common_proc_initiated -->|Timer T3550 runs out before COMPLETE received| event_t3550_expiry;
  event_t3550_expiry -->|Retransmission counter < 5| event_amf_sends_reg_accept;
  event_t3550_expiry -->|5th expiry, AMF aborts waiting and enters registered state| state_amf_registered;
```


***error :
 state_ue_processing_reject -->|Based on specific reject cause (e.g., #11, #73, #74, #75) leading to PLMN search| state_ue_plmn_search;
 should be 
state_ue_processing_reject -->|"Based on specific reject cause (e.g., #11, #73, #74, #75) leading to PLMN search"| state_ue_plmn_search;

***