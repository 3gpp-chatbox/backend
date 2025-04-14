```mermaid
graph TD;
  %% Procedure: Registration procedure for initial registration
  A(UE_Deregistered);
  %% Type: state
  %% Description: UE is in 5GMM-DEREGISTERED state.
  B(UE_Attempting_Initial_Registration);
  %% Type: state
  %% Description: UE has sent REGISTRATION REQUEST and is waiting for a response (Timer T3510 running).
  C(UE_Sending_RegComplete);
  %% Type: state
  %% Description: UE has received REGISTRATION ACCEPT requiring acknowledgement and is preparing/sending REGISTRATION COMPLETE.
  D(UE_Registered);
  %% Type: state
  %% Description: UE is successfully registered with the network (5GMM-REGISTERED state).
  E(UE_Registration_Rejected);
  %% Type: state
  %% Description: UE registration attempt was rejected by the network or failed due to maximum retries or other failures.
  F(AMF_Idle);
  %% Type: state
  %% Description: AMF is idle with respect to this UE's registration procedure.
  G(AMF_Processing_Initial_Registration);
  %% Type: state
  %% Description: AMF has received REGISTRATION REQUEST and is processing it (e.g., performing authentication, security).
  H(AMF_Waiting_Registration_Complete);
  %% Type: state
  %% Description: AMF has sent REGISTRATION ACCEPT requiring acknowledgement and is waiting for REGISTRATION COMPLETE (Timer T3550 running).
  I(AMF_Registered);
  %% Type: state
  %% Description: AMF considers the UE successfully registered (5GMM-REGISTERED state).
  J(E_REGISTRATION_REQUEST);
  %% Type: event
  %% Description: REGISTRATION REQUEST message is sent by UE / received by AMF.
  K(E_REGISTRATION_ACCEPT_ReqComplete);
  %% Type: event
  %% Description: REGISTRATION ACCEPT message requiring REGISTRATION COMPLETE is sent by AMF / received by UE.
  L(E_REGISTRATION_ACCEPT_NoComplete);
  %% Type: event
  %% Description: REGISTRATION ACCEPT message not requiring REGISTRATION COMPLETE is sent by AMF / received by UE.
  M(E_REGISTRATION_REJECT);
  %% Type: event
  %% Description: REGISTRATION REJECT message is sent by AMF / received by UE.
  N(E_REGISTRATION_COMPLETE);
  %% Type: event
  %% Description: REGISTRATION COMPLETE message is sent by UE / received by AMF.
  O(E_T3510_Timeout_Retry);
  %% Type: event
  %% Description: UE's T3510 timer expires before receiving a response, and retry counter is less than 5.
  P(E_T3510_Timeout_Max);
  %% Type: event
  %% Description: UE's T3510 timer expires, and retry counter reaches 5.
  Q(E_T3550_Timeout_Retry);
  %% Type: event
  %% Description: AMF's T3550 timer expires (1st to 4th time) while waiting for REGISTRATION COMPLETE.
  R(E_T3550_Timeout_Max);
  %% Type: event
  %% Description: AMF's T3550 timer expires for the 5th time while waiting for REGISTRATION COMPLETE.
  S(E_Failure_UE);
  %% Type: event
  %% Description: Abnormal case occurs at the UE side (e.g., lower layer failure, TAI change).
  T(E_Failure_AMF);
  %% Type: state
  %% Description: Abnormal case occurs at the AMF side (e.g., lower layer failure).
  A --> J;
  %% Type: trigger
  %% Description: Triggered by UE initiating initial registration by sending REGISTRATION REQUEST message.
  J --> B;
  %% Type: condition
  %% Description: Transition occurs after UE sends REGISTRATION REQUEST and starts timer T3510.
  F --> J;
  %% Type: trigger
  %% Description: Triggered by AMF receiving a REGISTRATION REQUEST message from the UE.
  J --> G;
  %% Type: condition
  %% Description: Transition occurs when AMF receives the REGISTRATION REQUEST and starts processing it, potentially initiating common procedures.
  G --> K;
  %% Type: trigger
  %% Description: Triggered by AMF accepting the registration and sending REGISTRATION ACCEPT that requires a REGISTRATION COMPLETE response (e.g., due to GUTI reallocation, SOR container, Operator-defined access category definitions, CAG info, UE radio capability ID, PEIPS info, NSAG info, NSSAI update, On-demand NSSAI, Alternative NSSAI, Truncated 5G-S-TMSI config, Service-level-AA pending).
  K --> H;
  %% Type: condition
  %% Description: Transition occurs after AMF sends REGISTRATION ACCEPT requiring COMPLETE and starts timer T3550.
  G --> L;
  %% Type: trigger
  %% Description: Triggered by AMF accepting the registration and sending REGISTRATION ACCEPT that does not require a REGISTRATION COMPLETE response.
  L --> I;
  %% Type: condition
  %% Description: Transition occurs after AMF sends REGISTRATION ACCEPT not requiring COMPLETE; AMF enters registered state.
  G --> M;
  %% Type: trigger
  %% Description: Triggered by AMF rejecting the registration request due to various reasons (e.g., congestion, not allowed, no slices available).
  M --> F;
  %% Type: condition
  %% Description: Transition occurs after AMF sends REGISTRATION REJECT.
  B --> K;
  %% Type: trigger
  %% Description: Triggered by UE receiving a REGISTRATION ACCEPT message that requires a REGISTRATION COMPLETE response.
  K --> C;
  %% Type: condition
  %% Description: Transition occurs after UE receives REGISTRATION ACCEPT requiring COMPLETE, stops T3510, resets counters, and prepares to send REGISTRATION COMPLETE.
  B --> L;
  %% Type: trigger
  %% Description: Triggered by UE receiving a REGISTRATION ACCEPT message that does not require a REGISTRATION COMPLETE response.
  L --> D;
  %% Type: condition
  %% Description: Transition occurs after UE receives REGISTRATION ACCEPT not requiring COMPLETE, stops T3510, resets counters, and enters 5GMM-REGISTERED state.
  B --> M;
  %% Type: trigger
  %% Description: Triggered by UE receiving a REGISTRATION REJECT message from the AMF.
  M --> E;
  %% Type: condition
  %% Description: Transition occurs after UE receives REGISTRATION REJECT, stops T3510, and processes the rejection based on the 5GMM cause value.
  C --> N;
  %% Type: trigger
  %% Description: Triggered by UE sending the REGISTRATION COMPLETE message to acknowledge reception of specific IEs in REGISTRATION ACCEPT.
  N --> D;
  %% Type: condition
  %% Description: Transition occurs after UE sends REGISTRATION COMPLETE; UE remains in 5GMM-REGISTERED state.
  H --> N;
  %% Type: trigger
  %% Description: Triggered by AMF receiving the REGISTRATION COMPLETE message from the UE.
  N --> I;
  %% Type: condition
  %% Description: Transition occurs after AMF receives REGISTRATION COMPLETE, stops timer T3550, and enters 5GMM-REGISTERED state.
  B --> O;
  %% Type: trigger
  %% Description: Triggered by expiration of timer T3510 at the UE when the registration attempt counter is less than 5.
  O --> B;
  %% Type: condition
  %% Description: Transition occurs when UE restarts the initial registration procedure after T3510 timeout (implicitly includes T3511 logic).
  B --> P;
  %% Type: trigger
  %% Description: Triggered by expiration of timer T3510 at the UE when the registration attempt counter is equal to 5.
  P --> E;
  %% Type: condition
  %% Description: Transition occurs when UE aborts registration after 5 attempts due to T3510 expiry, deletes context, and enters a deregistered state (e.g., 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION or PLMN-SEARCH).
  B --> S;
  %% Type: trigger
  %% Description: Triggered by abnormal cases at UE like lower layer failure, TAI change, or protocol error before receiving response.
  C --> S;
  %% Type: trigger
  %% Description: Triggered by abnormal cases at UE like lower layer failure or TAI change after receiving ACCEPT but before sending COMPLETE.
S --> I;
  H --> Q;
  %% Type: trigger
  %% Description: Triggered by expiration of timer T3550 at the AMF (1st to 4th time).
  Q --> H;
  %% Type: condition
  %% Description: Transition occurs when AMF retransmits REGISTRATION ACCEPT and restarts timer T3550.
  H --> R;
  %% Type: trigger
  %% Description: Triggered by expiration of timer T3550 at the AMF for the 5th time.
  R --> I;
  %% Type: condition
  %% Description: Transition occurs when AMF aborts the procedure after 5 T3550 expiries and enters 5GMM-REGISTERED state, keeping old and new GUTIs temporarily valid.
  H --> T;
  %% Type: trigger
  %% Description: Triggered by abnormal cases at AMF like lower layer failure before receiving REGISTRATION COMPLETE.
  T --> I;
  %% Type: condition
  %% Description: Transition occurs when AMF aborts the procedure due to failure and enters 5GMM-REGISTERED state, keeping old and new GUTIs temporarily valid.
  ```