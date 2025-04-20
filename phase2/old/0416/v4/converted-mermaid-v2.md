```mermaid
graph LR
    state_deregistered
    event_initiate_registration
    event_receive_accept
    state_registered
    event_receive_reject
    event_t3510_expiry
    state_attempting_registration
    event_t3511_expiry
    event_t3502_expiry
    state_plmn_search
    state_limited_service
    state_registered_plmn_search
    state_no_supi
    state_no_cell_available
    event_lower_layer_failure
    event_tai_change_before_response
    event_reg_complete_required
    event_tai_change_after_accept_before_complete
    event_reg_complete_tx_failure_tai_change
    event_reg_complete_tx_failure_no_tai_change
    event_reg_request_tx_failure
    event_t3346_expiry
    event_t3526_expiry
    event_access_barred
    event_access_barred_after_request
    event_dereg_request_collision
    event_ue_initiated_dereg_required
    event_t3447_running
    event_access_localized_services_not_allowed
    state_deregistered -->|"UE_Decides_Initial_Registration"| event_initiate_registration
    event_initiate_registration -->|"Send_REGISTRATION_REQUEST"| state_deregistered
    state_deregistered -->|"Receive_REGISTRATION_ACCEPT"| event_receive_accept
    event_receive_accept -->|"Process_REGISTRATION_ACCEPT"| state_registered
    state_registered -->|"Check_If_REGISTRATION_COMPLETE_Required"| event_reg_complete_required
    event_reg_complete_required -->|"Send_REGISTRATION_COMPLETE"| state_registered
    state_deregistered -->|"Receive_REGISTRATION_REJECT"| event_receive_reject
    event_receive_reject -->|"Process_REJECT_Cause_3_6_7"| state_no_supi
    event_receive_reject -->|"Process_REJECT_Cause_11"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_12"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_13_LimitedService"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_13_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_15"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_22"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Cause_27"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_31"| state_no_cell_available
    event_receive_reject -->|"Process_REJECT_Cause_36"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_62_Retry"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Cause_62_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_62_LimitedService"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_72"| state_deregistered
    event_receive_reject -->|"Process_REJECT_Cause_73"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_74"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_75"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_76_LimitedService"| state_limited_service
    event_receive_reject -->|"Process_REJECT_Cause_76_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_77"| state_deregistered
    event_receive_reject -->|"Process_REJECT_Cause_78"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_79_Retry"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Cause_79_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_80"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_81_Retry"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Cause_81_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_82_Retry"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Cause_82_PLMNSearch"| state_plmn_search
    event_receive_reject -->|"Process_REJECT_Cause_5_Emergency"| state_no_supi
    event_receive_reject -->|"Process_REJECT_Other_Emergency"| state_deregistered
    state_deregistered -->|"Timer_T3510_Expires"| event_t3510_expiry
    event_t3510_expiry -->|"Handle_T3510_Expiry_Retry"| state_attempting_registration
    event_t3510_expiry -->|"Handle_T3510_Expiry_MaxAttempts_Attempting"| state_attempting_registration
    event_t3510_expiry -->|"Handle_T3510_Expiry_MaxAttempts_PLMNSearch"| state_plmn_search
    state_attempting_registration -->|"Timer_T3511_Expires"| event_t3511_expiry
    event_t3511_expiry -->|"Restart_Initial_Registration"| state_deregistered
    state_attempting_registration -->|"Timer_T3502_Expires"| event_t3502_expiry
    event_t3502_expiry -->|"Handle_T3502_Expiry_Attempting"| state_attempting_registration
    event_t3502_expiry -->|"Handle_T3502_Expiry_PLMNSearch"| state_plmn_search
    state_deregistered -->|"Lower_Layer_Failure_Occurs"| event_lower_layer_failure
    event_lower_layer_failure -->|"Handle_LowerLayerFailure_Retry"| state_attempting_registration
    event_lower_layer_failure -->|"Handle_LowerLayerFailure_MaxAttempts_Attempting"| state_attempting_registration
    event_lower_layer_failure -->|"Handle_LowerLayerFailure_MaxAttempts_PLMNSearch"| state_plmn_search
    state_deregistered -->|"TAI_Changes"| event_tai_change_before_response
    event_tai_change_before_response -->|"Abort_And_Reinitiate_Registration"| state_deregistered
    state_registered -->|"TAI_Changes"| event_tai_change_after_accept_before_complete
    event_tai_change_after_accept_before_complete -->|"Send_REGISTRATION_COMPLETE"| state_registered
    event_tai_change_after_accept_before_complete -->|"Abort_Initial_Registration_Initiate_Mobility_Update"| state_deregistered
    state_registered -->|"REG_COMPLETE_Tx_Failure_Occurs"| event_reg_complete_tx_failure_tai_change
    event_reg_complete_tx_failure_tai_change -->|"Resend_REGISTRATION_COMPLETE"| state_registered
    event_reg_complete_tx_failure_tai_change -->|"Abort_Initial_Registration_Initiate_Mobility_Update"| state_deregistered
    state_registered -->|"REG_COMPLETE_Tx_Failure_Occurs"| event_reg_complete_tx_failure_no_tai_change
    event_reg_complete_tx_failure_no_tai_change -->|"Rerun_REGISTRATION_COMPLETE_Transmission (Implementation Specific)"| state_registered
    state_deregistered -->|"REG_REQUEST_Tx_Failure_Occurs"| event_reg_request_tx_failure
    event_reg_request_tx_failure -->|"Abort_And_Reinitiate_Registration"| state_deregistered
    state_attempting_registration -->|"Timer_T3346_Expires"| event_t3346_expiry
    event_t3346_expiry -->|"Allow_Initial_Registration"| state_deregistered
    state_deregistered -->|"Access_Barred_Indication_Received"| event_access_barred
    event_access_barred -->|"Do_Not_Start_Registration"| state_deregistered
    state_deregistered -->|"Access_Barred_Indication_Received"| event_access_barred_after_request
    event_access_barred_after_request -->|"Handle_AccessBarredAfterRequest_Retry"| state_attempting_registration
    event_access_barred_after_request -->|"Handle_AccessBarredAfterRequest_MaxAttempts_Attempting"| state_attempting_registration
    event_access_barred_after_request -->|"Handle_AccessBarredAfterRequest_MaxAttempts_PLMNSearch"| state_plmn_search
    state_deregistered -->|"Receive_DEREGISTRATION_REQUEST"| event_dereg_request_collision
    event_dereg_request_collision -->|"Abort_Deregistration_Continue_Registration"| state_deregistered
    state_deregistered -->|"UE_Needs_Deregistration"| event_ue_initiated_dereg_required
    event_ue_initiated_dereg_required -->|"Abort_Registration_Perform_Deregistration"| state_deregistered
    state_deregistered -->|"Check_T3447_Status"| event_t3447_running
    event_t3447_running -->|"Do_Not_Start_Registration_With_FollowOn"| state_deregistered
    state_deregistered -->|"Check_Localized_Service_Allowance"| event_access_localized_services_not_allowed
    event_access_localized_services_not_allowed -->|"Abort_Registration_Enter_LimitedService"| state_limited_service
    event_access_localized_services_not_allowed -->|"Abort_Registration_Enter_PLMNSearch"| state_plmn_search
    event_receive_accept -->|"Process_ACCEPT_CAG_Restriction_LimitedService"| state_limited_service
    event_receive_accept -->|"Process_ACCEPT_CAG_Restriction_PLMNSearch"| state_registered_plmn_search
    event_receive_accept -->|"Process_ACCEPT_Registration_Result_Dereg_Other_Access"| state_deregistered
    event_receive_accept -->|"Process_ACCEPT_SOR_Failure_Attempt_Other_PLMN"| state_registered
    event_receive_accept -->|"Process_ACCEPT_SOR_Success_Attempt_Other_PLMN"| state_registered
    event_receive_reject -->|"Process_REJECT_Other_Abnormal"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Other_Abnormal_MaxAttempts_Attempting"| state_attempting_registration
    event_receive_reject -->|"Process_REJECT_Other_Abnormal_MaxAttempts_PLMNSearch"| state_plmn_search
```