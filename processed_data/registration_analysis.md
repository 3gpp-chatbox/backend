<<<<<<< HEAD
# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment: Device used by the end user to access the 5G network."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function: Responsible for registration, connection management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function: Responsible for session management, PDU session establishment, modification and release."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function: Responsible for user plane traffic forwarding, policy enforcement and traffic measurement."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function: Provides policy rules for session management and mobility management."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function: Service discovery function."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network."
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the 5G network."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the 5G network."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure by sending a REGISTRATION REQUEST message to the AMF.",
  "trigger": "UE powers on and needs to access the 5GS.",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "Timer T3510 starts."
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure by sending an AUTHENTICATION REQUEST message to the UE.",
  "trigger": "Valid Registration Request received by AMF.",
  "conditions": [
    "UE identity needs to be verified"
  ],
  "timing": "Timer T3560 starts."
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE sends an AUTHENTICATION RESPONSE message to the AMF.",
  "trigger": "Receiving Authentication Request from AMF.",
  "conditions": [
    "UE successfully calculates the authentication response."
  ],
  "timing": "After UE calculates the authentication response."
}

{
  "sequence_number": 4,
  "step_name": "Security Mode Control Procedure",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Security Mode Command",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF initiates the security mode control procedure to take a 5G NAS security context into use.",
  "trigger": "Successful authentication of the UE.",
  "conditions": [
    "AMF needs to establish secure communication with the UE."
  ],
  "timing": "After successful authentication."
}

{
  "sequence_number": 5,
  "step_name": "Security Mode Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Security Mode Complete",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE sends a SECURITY MODE COMPLETE message to the AMF.",
  "trigger": "Receiving Security Mode Command from AMF.",
  "conditions": [
    "UE successfully initializes security."
  ],
  "timing": "After UE successfully initializes security."
}

{
  "sequence_number": 6,
  "step_name": "Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF sends a REGISTRATION ACCEPT message to the UE.",
  "trigger": "Successful completion of security mode control procedure.",
  "conditions": [
    "AMF authorizes the UE to register."
  ],
  "timing": "After successful security mode control."
}

{
  "sequence_number": 7,
  "step_name": "Registration Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Complete",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "UE sends a REGISTRATION COMPLETE message to the AMF.",
  "trigger": "Receiving Registration Accept from AMF.",
  "conditions": [
    "UE successfully processes the Registration Accept message."
  ],
  "timing": "After UE processes the Registration Accept message."
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection management, mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Data plane handling"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates registration and communicates with the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Forwards user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or needs to access the 5GS",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs to be verified"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "UE sends authentication response to the AMF",
  "trigger": "Receiving Authentication Request",
  "conditions": [
    "UE successfully calculates authentication response"
  ],
  "timing": "T3520 starts if UE does not accept the server certificate"
}

{
  "sequence_number": 4,
  "step_name": "Security Mode Command",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Security Mode Command",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF initiates security mode control procedure to establish secure communication",
  "trigger": "Successful authentication",
  "conditions": [
    "UE supports the selected security algorithms"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 5,
  "step_name": "Security Mode Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Security Mode Complete",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE confirms the security mode control procedure",
  "trigger": "Receiving Security Mode Command",
  "conditions": [
    "UE successfully configures security"
  ],
  "timing": "AMF stops T3560"
}

{
  "sequence_number": 6,
  "step_name": "Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF confirms the registration of the UE",
  "trigger": "Successful security mode control procedure",
  "conditions": [
    "UE authorized to access the network"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection, mobility, and access control"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Routes and forwards user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - initiates the registration procedure and communicates with the network."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, authentication, and mobility."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data packets."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules for session management."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network."
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating to the network."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages UE sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has limited service"
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has no SUPI"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "AMF rejects authentication",
  "trigger": "Authentication fails",
  "conditions": [],
  "timing": "N/A"
}

{
  "sequence_number": 4,
  "step_name": "Registration Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "AMF rejects registration",
  "trigger": "Registration fails",
  "conditions": [],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates and participates in the registration procedure."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Routes user plane traffic."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Provides service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered."
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and searching for a PLMN."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and in limited service."
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "FINAL",
  "description": "UE is deregistered and has no SUPI."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure by sending a Registration Request message to the AMF.",
  "trigger": "UE powers on or selects a new PLMN/SNPN.",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates the authentication procedure by sending an Authentication Request message to the UE.",
  "trigger": "Valid Registration Request received.",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE responds to the authentication request with an Authentication Response message.",
  "trigger": "Authentication Request received.",
  "conditions": [
    "UE successfully performs authentication procedure"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 4,
  "step_name": "AMF Identity Request (Conditional)",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Identity Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF requests the UE's identity if needed.",
  "trigger": "AMF needs UE identity.",
  "conditions": [
    "SUCI not available",
    "UE identity required"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 5,
  "step_name": "UE Identity Response (Conditional)",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Identity Response",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE responds to the identity request with an Identity Response message.",
  "trigger": "Identity Request received.",
  "conditions": [
    "UE provides requested identity"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 6,
  "step_name": "AMF Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts the registration and sends a Registration Accept message to the UE.",
  "trigger": "Authentication successful and authorization complete.",
  "conditions": [
    "UE authorized to register",
    "Network resources available"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, IP address allocation, and UPF selection"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing and forwarding, policy enforcement, and traffic measurement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the control plane functions"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the 5G network"
}

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, PDU session establishment, modification and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the SMF"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating to the network"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and has limited service"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering and authenticating"
}

{
  "name": "PDU SESSION ACTIVE",
  "type": "INTERMEDIATE",
  "description": "PDU session is established and active"
}

{
  "name": "PROCEDURE TRANSACTION INACTIVE",
  "type": "INTERMEDIATE",
  "description": "No procedure transaction is active"
}

{
  "name": "PDU SESSION MODIFICATION PENDING",
  "type": "INTERMEDIATE",
  "description": "PDU session modification is pending"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or moves to a new tracking area",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the network"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is attempting registration after deregistration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is searching for a PLMN after deregistration"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is in limited service state after deregistration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "AUTHENTICATION REJECT",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "Authentication is rejected by the network",
  "trigger": "Authentication fails",
  "conditions": [],
  "timing": "Timers T3510, T3516, T3517, T3519, T3520 or T3521 are stopped"
}

{
  "sequence_number": 4,
  "step_name": "Registration Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "REGISTRATION REJECT",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "Registration is rejected by the network",
  "trigger": "Network rejects registration",
  "conditions": [],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, IP address allocation, and UPF selection"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing and forwarding, policy enforcement, and traffic measurement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the SMF"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the 5G network"
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure to register to the network for 5GS services and establish a 5GMM context.",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates and participates in the registration procedure."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Routes user plane traffic."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery."
}

## States

{
  "name": "5GMM-DEREGISTERED",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is attempting to register but has not yet succeeded."
}

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE when powered off or USIM is removed."
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is attempting to update its registration but has not yet succeeded."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is searching for a PLMN to register with."
}

{
  "name": "5GMM-REGISTERED.NON-ALLOWED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but not allowed to use certain services."
}

{
  "name": "5GMM-REGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but no cell is available."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is in limited service state."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-DEREGISTERED",
  "destination_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "description": "UE initiates registration procedure by sending a REGISTRATION REQUEST message to the AMF.",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services after unavailability period.",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "destination_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "description": "AMF initiates authentication procedure.",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "No 5GMM context has been established"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INITIAL",
  "description": "No 5GMM context has been established and the UE location is unknown to the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "A 5GMM context has been established"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED-INITIATED",
  "type": "INTERMEDIATE",
  "description": "UE has requested release of the 5GMM context by starting the de-registration procedure and is waiting for a response from the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-DEREGISTERED",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure to establish a 5GMM context.",
  "trigger": "UE powers on and needs to access the network",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure to verify UE identity.",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates and participates in the registration procedure."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INITIAL",
  "description": "UE is deregistered from the network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network."
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network during registration."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode with the network."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN."
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has no SUPI."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration."
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is registered and attempting registration update."
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode."
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and no cell is available."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-DEREGISTERED",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure to register for 5GS services, emergency services, or SMS over NAS.",
  "trigger": "UE powers on, moves from GERAN/UTRAN to NG-RAN, or needs to come out of unavailability period.",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure to verify UE identity.",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or inter-system change from S1 mode to N1 mode or RRC Connection failure or change in 5GMM capability or change in UE's usage setting or UE needs to change the slice(s) it is currently registered to",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user data traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "State during the registration procedure"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "State during the authentication procedure"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered with limited service"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-REGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but no cell is available"
}

{
  "name": "5GMM-REGISTERED.NON-ALLOWED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but not allowed service"
}

{
  "name": "5GMM-REGISTERED.NORMAL-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered with normal service"
}

{
  "name": "5GMM-ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is attempting registration update"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, connection, mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards and routes user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "State during the registration procedure"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "State during authentication procedure"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered"
}

{
  "name": "5GMM-REGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but no cell is available"
}

{
  "name": "5GMM-REGISTERED.NORMAL-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered and in normal service"
}

{
  "name": "5GMM-REGISTERED.NON-ALLOWED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but not allowed service"
}

{
  "name": "5GMM-COMMON-PROCEDURE-INITIATED",
  "type": "INTERMEDIATE",
  "description": "A common procedure is initiated"
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is attempting registration update"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or inter-system change from S1 mode to N1 mode or UE changes 5GMM capability or UE's usage setting changes or UE needs to change the slice(s) it is currently registered to",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs to be verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is attempting to register after being deregistered"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is searching for a PLMN after being deregistered"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is in limited service after being deregistered"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to connect to the 5G network."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Responsible for registration, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network."
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network."
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

{
  "name": "AUSF",
  "type": "Network Element",
  "description": "Authentication Server Function - authenticates the UE"
}

{
  "name": "AAA server",
  "type": "Network Element",
  "description": "Authentication, Authorization, and Accounting server"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3520 starts"
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE responds to the authentication request",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE successfully processes the authentication challenge"
  ],
  "timing": "T3520 stops"
}

{
  "sequence_number": 4,
  "step_name": "AMF Authentication Result",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Result",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF informs UE of authentication result",
  "trigger": "Authentication procedure completed",
  "conditions": [
    "Authentication successful"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 5,
  "step_name": "AMF Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts the registration request",
  "trigger": "Authentication successful and other conditions met",
  "conditions": [
    "UE authorized to access the network"
  ],
  "timing": "T3510 stops"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates registration and communicates with the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE access and mobility"
}

{
  "name": "AUSF",
  "type": "Network Element",
  "description": "Authentication Server Function - Authenticates the UE"
}

{
  "name": "SEAF",
  "type": "Network Element",
  "description": "Security Anchor Function - Derives security keys"
}

{
  "name": "AAA server of the CH or the DCS",
  "type": "Network Element",
  "description": "AAA server of the Credentials Holder (CH) or the Default Credentials Server (DCS)"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "AUTHENTICATION REQUEST (EAP-request)",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure using EAP",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "AUTHENTICATION RESPONSE (EAP-response)",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "UE responds to the authentication request",
  "trigger": "Received AUTHENTICATION REQUEST (EAP-request)",
  "conditions": [
    "USIM present",
    "SNN check successful",
    "Sequence number in AUTN is correct",
    "No other errors during EAP-AKA' challenge handling"
  ],
  "timing": "T3520 starts"
}

{
  "sequence_number": 4,
  "step_name": "Authentication Result/Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "AUTHENTICATION RESULT (EAP-success) or AUTHENTICATION REJECT (EAP-failure)",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF sends the result of the authentication",
  "trigger": "Successful or unsuccessful authentication",
  "conditions": [
    "Authentication successful or failed"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "State during the registration procedure"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "State during the authentication procedure"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the network"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and initiates PLMN search"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Reject Handling",
  "source_element": "UE",
  "destination_element": "N/A",
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "UE handles Authentication Reject message",
  "trigger": "Authentication Reject received",
  "conditions": [
    "Authentication failed"
  ],
  "timing": "T3510, T3517, T3519, T3521 timers stopped"
}

{
  "sequence_number": 4,
  "step_name": "SNPN Authentication Reject Handling",
  "source_element": "UE",
  "destination_element": "N/A",
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "UE handles Authentication Reject message for SNPN",
  "trigger": "Authentication Reject received",
  "conditions": [
    "Authentication failed",
    "UE registered for onboarding services in SNPN or performing initial registration for onboarding services in SNPN"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE sends authentication response to AMF",
  "trigger": "Receiving Authentication Request",
  "conditions": [
    "Valid Authentication Request"
  ],
  "timing": "T3520 stops"
}

{
  "sequence_number": 4,
  "step_name": "Authentication Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "AMF rejects authentication",
  "trigger": "Invalid Authentication Response",
  "conditions": [
    "Authentication fails"
  ],
  "timing": "T3510, T3517, T3519, T3521 stops"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verification needed"
  ],
  "timing": "T3520 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, authentication, and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control plane functions for policy enforcement and QoS"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement and QoS handling"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control plane functions"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating to the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (PDU session establishment, modification, release)"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the SMF and other network functions"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service"
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and no cell is available"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Provides network function discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "State while registration is in progress"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "State after successful registration"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "State after deregistration with limited service"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "State after deregistration and PLMN search is initiated"
}

{
  "name": "EMM-DEREGISTERED",
  "type": "FINAL",
  "description": "EPS Mobility Management - Deregistered state"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "State while registration and authentication is in progress"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "AAA-S",
  "type": "Network Element",
  "description": "AAA Server"
}

{
  "name": "NSSAAF",
  "type": "Network Element",
  "description": "Network Slice-Specific Authentication and Authorization Function"
}

## States

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Network Slice-Specific Authentication Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "UE sends the NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE message to the AMF",
  "trigger": "UE completes network slice-specific authentication",
  "conditions": [
    "UE has successfully authenticated for the network slice"
  ],
  "timing": "After UE completes network slice-specific authentication"
}

{
  "sequence_number": 2,
  "step_name": "AMF processes EAP response",
  "source_element": "AMF",
  "destination_element": "AAA-S",
  "message": "EAP-response message",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "AMF passes the EAP-response message to the AAA-S via the NSSAAF",
  "trigger": "Receipt of NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE message",
  "conditions": [
    "Valid EAP-response message received"
  ],
  "timing": "After receiving NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE message"
}

{
  "sequence_number": 3,
  "step_name": "AMF creates NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "source_element": "AMF",
  "destination_element": "N/A",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "AMF creates a NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "trigger": "Initiate network slice-specific EAP result message transport procedure",
  "conditions": [
    "EAP-success or EAP-failure message provided by the AAA-S"
  ],
  "timing": "After receiving EAP-success or EAP-failure message"
}

{
  "sequence_number": 4,
  "step_name": "AMF sends NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "AMF sends the NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message to the UE",
  "trigger": "AMF creates NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "conditions": [
    "Valid NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message created"
  ],
  "timing": "After creating NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message"
}

{
  "sequence_number": 5,
  "step_name": "UE processes EAP result",
  "source_element": "UE",
  "destination_element": "Upper Layers",
  "message": "EAP-success or EAP-failure message",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "UE passes the EAP-success or EAP-failure message to the upper layers",
  "trigger": "Receipt of NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "conditions": [
    "Valid NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message received"
  ],
  "timing": "After receiving NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates registration and communicates with the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "State during the registration procedure"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "State after successful registration"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "State during authentication procedure"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, IP address allocation, and UPF selection"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing and forwarding, policy enforcement, and traffic measurement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the SMF"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure by sending a Registration Request message to the AMF. The UE includes various capabilities in the 5GMM capability IE of the REGISTRATION REQUEST message.",
  "trigger": "UE powers on and attempts to connect to the 5G network",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, mobility management, authentication and authorization"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting to register"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "REGISTRATION REQUEST",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or needs to register",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "Registration Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "REGISTRATION REJECT",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "description": "AMF rejects the registration request",
  "trigger": "Initial registration request cannot be accepted",
  "conditions": [
    "Congestion",
    "CAG restrictions",
    "N1 mode not allowed",
    "No network slices available",
    "Serving network not authorized",
    "Temporarily not authorized for this SNPN",
    "Permanently not authorized for this SNPN",
    "Selected N3IWF is not compatible with the allowed NSSAI",
    "Selected TNGF is not compatible with the allowed NSSAI",
    "UE security capabilities invalid or unacceptable"
  ],
  "timing": "T3510 stops"
}

{
  "sequence_number": 3,
  "step_name": "Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "REGISTRATION ACCEPT",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts the registration request",
  "trigger": "Initial registration request accepted",
  "conditions": [],
  "timing": "T3550 starts"
}

{
  "sequence_number": 4,
  "step_name": "Registration Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "REGISTRATION COMPLETE",
  "source_state": "5GMM-REGISTERED",
  "destination_state": "5GMM-REGISTERED",
  "description": "UE confirms the registration",
  "trigger": "Reception of REGISTRATION ACCEPT",
  "conditions": [],
  "timing": "T3550 stops"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & management"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement and traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control the behavior of the network"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration"
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and no cell is available"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function"
}

## States

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Registration Reject due to CAG restrictions from CAG cell",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "REGISTRATION REJECT (5GMM cause #76, CAG information list)",
  "source_state": "N/A",
  "destination_state": "5GMM-DEREGISTERED.LIMITED-SERVICE/5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "UE receives registration reject from CAG cell due to CAG restrictions",
  "trigger": "Network determines UE is not authorized for the CAG cell",
  "conditions": [
    "UE receives 5GMM cause #76 from a CAG cell",
    "UE receives CAG information list"
  ],
  "timing": "Upon receiving REGISTRATION REJECT"
}

{
  "sequence_number": 2,
  "step_name": "Registration Reject due to CAG restrictions from non-CAG cell",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "REGISTRATION REJECT (5GMM cause #76, CAG information list)",
  "source_state": "N/A",
  "destination_state": "5GMM-DEREGISTERED.LIMITED-SERVICE/5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "UE receives registration reject from non-CAG cell due to CAG restrictions",
  "trigger": "Network determines UE is only allowed to access 5GS via CAG cells",
  "conditions": [
    "UE receives 5GMM cause #76 from a non-CAG cell",
    "UE receives CAG information list"
  ],
  "timing": "Upon receiving REGISTRATION REJECT"
}

{
  "sequence_number": 3,
  "step_name": "Registration Reject due to Wireline access area not allowed",
  "source_element": "W-AGF",
  "destination_element": "UE",
  "message": "REGISTRATION REJECT (5GMM cause #77)",
  "source_state": "N/A",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "UE receives registration reject from wireline access network because wireline access area is not allowed",
  "trigger": "Network determines UE is in a wireline access area not allowed",
  "conditions": [
    "UE receives 5GMM cause #77 from a wireline access network"
  ],
  "timing": "Upon receiving REGISTRATION REJECT"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages UE sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, authentication, and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (session establishment, modification, and release), UE IP address allocation & control, selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement, traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control network behavior"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on or inter-system change from S1 mode to N1 mode",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs to be verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (PDU session establishment, modification, release)"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control network behavior"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "REGISTRATION REQUEST",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure by sending a REGISTRATION REQUEST message to the AMF. The UE may include various IEs in the REGISTRATION REQUEST message based on its capabilities and configuration, such as 5GMM capability IE, UE radio capability ID, WUS assistance information, UE specific DRX parameters, UAS services support, NR paging subgrouping support, and request to keep user plane resources of the old non-3GPP access.",
  "trigger": "UE powers on and needs to attach to the 5G network",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "UE sends the REGISTRATION REQUEST message"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE registration and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function"
}

## States

{
  "name": "5GMM-IDLE",
  "type": "INITIAL",
  "description": "5GMM Idle mode"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "5GMM Connected mode"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "5GMM Registered mode"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Service Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "SERVICE REQUEST",
  "source_state": "5GMM-IDLE",
  "destination_state": "5GMM-CONNECTED",
  "description": "UE initiates service request procedure",
  "trigger": "UE has uplink signalling or user data pending, or receives paging",
  "conditions": [
    "5GS update status is 5U1 UPDATED",
    "TAI of current serving cell is in TAI list",
    "No 5GMM specific procedure ongoing"
  ],
  "timing": "T3517 starts"
}

{
  "sequence_number": 2,
  "step_name": "Service Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "SERVICE ACCEPT",
  "source_state": "5GMM-CONNECTED",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts the service request",
  "trigger": "AMF processes the SERVICE REQUEST message",
  "conditions": [
    "UE is allowed to access the TA",
    "UE passes CAG restrictions"
  ],
  "timing": "T3517 stops"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, IP address allocation"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane data transfer"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules for session management"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered in the 5G network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered in the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (establishment, modification, release), UE IP address allocation & selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement and traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control the behavior of the SMF and other network functions"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery function that allows network functions to discover each other"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the 5G network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, PDU session establishment, modification and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to the SMF"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection management, mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering and authenticating"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection, and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Routes user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

## States

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "PDU Session Authentication Command",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION AUTHENTICATION COMMAND <EAP-request message A>",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "SMF sends an EAP-request message to the UE to initiate PDU session authentication and authorization.",
  "trigger": "DN requires authentication and authorization of the UE for a PDU session.",
  "conditions": [],
  "timing": "Start T3590"
}

{
  "sequence_number": 2,
  "step_name": "PDU Session Authentication Complete",
  "source_element": "UE",
  "destination_element": "SMF",
  "message": "PDU SESSION AUTHENTICATION COMPLETE <EAP-response message to EAP-request message A>",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "UE responds with an EAP-response message to the SMF.",
  "trigger": "UE receives an EAP-request message from the SMF.",
  "conditions": [
    "Upper layers provide an EAP-response message"
  ],
  "timing": "Stop T3590, Start T3590"
}

{
  "sequence_number": 3,
  "step_name": "PDU Session Authentication Command (Retransmission)",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION AUTHENTICATION COMMAND <EAP-request message B>",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "SMF sends another EAP-request message to the UE to continue PDU session authentication and authorization.",
  "trigger": "DN requires authentication and authorization of the UE for a PDU session.",
  "conditions": [],
  "timing": "Stop T3590, Start T3590"
}

{
  "sequence_number": 4,
  "step_name": "PDU Session Authentication Complete (Retransmission)",
  "source_element": "UE",
  "destination_element": "SMF",
  "message": "PDU SESSION AUTHENTICATION COMPLETE <EAP-response message to EAP-request message B>",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "UE responds with another EAP-response message to the SMF.",
  "trigger": "UE receives an EAP-request message from the SMF.",
  "conditions": [
    "Upper layers provide an EAP-response message"
  ],
  "timing": "Stop T3590"
}

{
  "sequence_number": 5,
  "step_name": "PDU Session Establishment Accept/Reject or PDU Session Authentication Result/Release Command",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION ESTABLISHMENT ACCEPT <EAP-success message> OR PDU SESSION ESTABLISHMENT REJECT <EAP-failure message> OR PDU SESSION AUTHENTICATION RESULT <EAP-success message> OR PDU SESSION RELEASE COMMAND <EAP-failure message> OR REMOTE UE REPORT RESPONSE <EAP-success message or EAP-failure message>",
  "source_state": "N/A",
  "destination_state": "N/A",
  "description": "SMF sends either PDU SESSION ESTABLISHMENT ACCEPT/REJECT, PDU SESSION AUTHENTICATION RESULT/RELEASE COMMAND or REMOTE UE REPORT RESPONSE based on the success or failure of the authentication and authorization.",
  "trigger": "Completion of DN authentication and authorization.",
  "conditions": [
    "Authentication successful or failed"
  ],
  "timing": "N/A"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (establishment, modification, release), UE IP address allocation, selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing and forwarding, policy enforcement, traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control network behavior"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, and mobility management"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the network"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verification needed"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "UE sends authentication response to the network",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE successfully calculates authentication response"
  ],
  "timing": "After processing Authentication Request"
}

{
  "sequence_number": 4,
  "step_name": "AMF Authentication Result",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Result",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF sends the result of EAP authentication to the UE",
  "trigger": "Authentication Response received",
  "conditions": [
    "EAP authentication performed"
  ],
  "timing": "After EAP authentication"
}

{
  "sequence_number": 5,
  "step_name": "UE Authentication Failure",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Failure",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "UE indicates that authentication of the network has failed",
  "trigger": "Authentication of the network failed",
  "conditions": [
    "Authentication of the network failed"
  ],
  "timing": "After authentication failure"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages UE sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection, mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, connection, and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, connection, and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards and routes user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE access and mobility"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

## States

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Authentication Request",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "AUTHENTICATION REQUEST message",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 2,
  "step_name": "Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "AUTHENTICATION RESPONSE message",
  "source_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "destination_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "description": "UE responds to authentication request",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE successfully authenticates"
  ],
  "timing": "Before T3560 expires"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Failure",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "AUTHENTICATION FAILURE message",
  "source_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "destination_state": "5GMM-NULL",
  "description": "UE sends authentication failure",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE fails to authenticate"
  ],
  "timing": "Before T3560 expires"
}

{
  "sequence_number": 4,
  "step_name": "Security Mode Command",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "SECURITY MODE COMMAND message",
  "source_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "destination_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "description": "AMF initiates security mode procedure",
  "trigger": "Successful Authentication",
  "conditions": [
    "UE security capabilities known"
  ],
  "timing": "After Authentication"
}

{
  "sequence_number": 5,
  "step_name": "Security Mode Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "SECURITY MODE COMPLETE message",
  "source_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "destination_state": "5GMM-REGISTERED",
  "description": "UE completes security mode procedure",
  "trigger": "Security Mode Command received",
  "conditions": [
    "Security mode setup successful"
  ],
  "timing": "Before T3560 expires"
}

{
  "sequence_number": 6,
  "step_name": "Security Mode Reject",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "SECURITY MODE REJECT message",
  "source_state": "5GMM-COMMON-PROCEDURE-INITIATED",
  "destination_state": "5GMM-NULL",
  "description": "UE rejects security mode procedure",
  "trigger": "Security Mode Command received",
  "conditions": [
    "Security mode setup failed"
  ],
  "timing": "Before T3560 expires"
}

{
  "sequence_number": 7,
  "step_name": "Configuration Update Command",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "CONFIGURATION UPDATE COMMAND message with \"acknowledgement requested\" set in the Acknowledgement bit of the Configuration update indication IE",
  "source_state": "5GMM-REGISTERED",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF sends configuration update command",
  "trigger": "Registration complete",
  "conditions": [
    "Configuration needs to be updated"
  ],
  "timing": "After Security Mode Complete"
}

{
  "sequence_number": 8,
  "step_name": "Configuration Update Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "CONFIGURATION UPDATE COMPLETE message",
  "source_state": "5GMM-REGISTERED",
  "destination_state": "5GMM-REGISTERED",
  "description": "UE sends configuration update complete",
  "trigger": "Configuration Update Command received",
  "conditions": [
    "Configuration updated successfully"
  ],
  "timing": "Before T3555 expires"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages UE sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE access and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages UE registration, connection, and mobility"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - forwards and routes user plane data"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-CONNECTED",
  "type": "FINAL",
  "description": "UE is registered and has a connection"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Transition to 5GMM-CONNECTED",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "N/A",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-CONNECTED",
  "description": "Transition to 5GMM-CONNECTED mode",
  "trigger": "Authentication complete",
  "conditions": [
    "Authentication successful"
  ],
  "timing": "T3511 stops"
}

# Extracted Data from processed_data\semantic_chunks.md

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, connection management, mobility, and access control"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Routes and forwards user plane traffic"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered in the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered in the network"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "Initial Registration Request",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Request",
  "source_state": "5GMM-NULL",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE initiates registration procedure",
  "trigger": "UE powers on",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "T3510 starts"
}

{
  "sequence_number": 2,
  "step_name": "AMF Authentication",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Request",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verified"
  ],
  "timing": "T3560 starts"
}
=======
# 5G Initial Registration Analysis

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required by the network
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the user
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully calculates authentication response
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode control procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities need to be negotiated
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode control
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security Mode Command processed successfully
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts registration
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode control successful Registration accepted
- **Conditions**:
  - Authentication and security procedures completed successfully
  - Registration is accepted by the network
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept processed successfully
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure successful
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully configures security
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure successful
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context does not exist
  - Authentication required
- **Timing**: Upon receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE responds with authentication information
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: Upon receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully sets up security mode
- **Timing**: Upon receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete
- **Conditions**:
  - Security mode procedure successful
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: Upon receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start T3560

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has processed the Authentication Request
- **Conditions**:
  - UE has calculated the authentication response
- **Timing**: Stop T3520

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode control procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish secure communication
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode activation
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has activated the security mode
- **Conditions**:
  - Security mode command received and processed successfully
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF has validated the registration request and security is established
- **Conditions**:
  - Authentication and security mode procedures successful
  - UE authorized to access the network
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms successful registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE has received the Registration Accept message
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: Stop T3513

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security Mode Command received and processed successfully
- **Timing**: After receiving Security Mode Command from AMF

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration process
- **Conditions**:
  - Authentication and security procedures are successful
- **Timing**: After successful security mode procedure

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required
- **Timing**: Start Authentication procedure

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode control procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode procedure

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE has successfully configured security
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has received Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF receives Authentication Request from AMF
- **Timing**: After receiving Authentication Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful Authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures successful
  - UE authorized to access the network
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received Registration requirements met
- **Conditions**:
  - Security Mode Complete received
  - Registration requirements met
- **Timing**: N/A

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully authenticates

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete UE authorized
- **Conditions**:
  - Security mode procedure complete
  - UE authorized

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by the network

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context does not exist Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: After sending Authentication Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully generates authentication response
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security context
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Registration successful
  - UE authorized
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context does not exist Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete Registration successful
- **Conditions**:
  - Security mode setup complete
  - Registration successful
- **Timing**: Stop T3510

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information for the UE
- **Timing**: After AMF forwards Authentication Request to AUSF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: On successful security mode setup

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security setup
  - Registration accepted by the network
- **Timing**: After successful security mode setup and registration completion

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication is successful
  - AMF has security capabilities
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE has applied the security configuration
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure is complete Registration successful
- **Conditions**:
  - Registration is successful
- **Timing**: Stop T3510

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has received the Registration Accept message
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors to authenticate the UE
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has completed security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After Security Mode Command is processed

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF has completed registration procedures
- **Conditions**:
  - Registration successful
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE has processed the Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context does not exist Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE configures security UE activates security
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure AMF assigns 5G-GUTI
- **Conditions**:
  - Registration successful
  - UE authorized
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept UE stores registration information
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the UE
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security mode setup
  - Network resources allocated
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by the network
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request from UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF receives Authentication Response from UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command from AMF
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF receives Security Mode Complete from UE
- **Conditions**:
  - Registration successful
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - Registration accepted by the network
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication was successful
  - AMF has received security capabilities from the UE
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE has successfully configured security
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure is complete
  - Registration is successful
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has received the Registration Accept message
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request from UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF forwards authentication request to AUSF
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command from AMF
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure successful
- **Conditions**:
  - Security Mode procedure successful
  - Registration successful
- **Timing**: After successful security mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the UE
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with the UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command and applies security
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Authentication and security procedures are successful
  - UE is authorized to register
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has successfully processed the Registration Accept message
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security mode
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security mode

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete AMF accepts registration
- **Conditions**:
  - UE is authorized to register
- **Timing**: After security mode complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration requirements met
- **Conditions**:
  - Successful security mode procedure
  - UE authorized to register
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has received Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has processed the Authentication Request
- **Conditions**:
  - UE has completed authentication procedure
- **Timing**: After receiving Authentication Request from AMF

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After receiving Authentication Response from UE

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE has completed security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command from AMF

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF has accepted the registration request
- **Conditions**:
  - Registration successful
  - UE authorized to access the network
- **Timing**: After receiving Security Mode Complete from UE

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE has received the Registration Accept message
- **Conditions**:
  - UE has successfully registered with the network
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Registration Request received Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist or is invalid
  - Authentication is required by the network
- **Timing**: Start T3560

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: Authentication required
- **Conditions**:
  - AUSF needs authentication vectors to authenticate the UE
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication Request received
- **Conditions**:
  - UE has processed the authentication challenge
- **Timing**: Stop T3560

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - AMF needs to establish security with the UE
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Security Mode Command received and processed
- **Conditions**:
  - UE has successfully configured security
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received Registration successful
- **Conditions**:
  - Registration successful
  - AMF has allocated resources for the UE
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration Accept received
- **Conditions**:
  - UE has successfully registered with the network
- **Timing**: Stop T3510

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: After receiving Registration Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: After Security Mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start T3560

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
  - UE can successfully generate authentication response
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command Security setup successful
- **Conditions**:
  - UE receives Security Mode Command
  - Security setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received Registration successful
- **Conditions**:
  - Security Mode Complete received
  - Registration successful
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start T3520

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to authenticate the UE
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: Stop T3520

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start T3513

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command and successfully applies security
- **Conditions**:
  - Security mode setup successful
- **Timing**: Stop T3513

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete AMF accepts registration
- **Conditions**:
  - Registration successful
  - UE context established in AMF
- **Timing**: Start T3511

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: Stop T3511

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received Registration successful
- **Conditions**:
  - All required information obtained
  - Registration authorized
- **Timing**: Start T3550

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms successful registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: Stop T3510

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors for the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful registration
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE provides authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup with UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - AMF needs to establish secure communication with UE
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully configures security
- **Timing**: On receipt of Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete AMF authorizes registration
- **Conditions**:
  - Security mode procedure successful
  - UE authorized to register
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms successful registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE to establish security
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - AMF selects security algorithms
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - UE successfully sets up security
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure is complete AMF registers UE
- **Conditions**:
  - Authentication and security successful
  - UE context established in AMF
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start Authentication procedure

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to authenticate the UE
- **Timing**: Part of Authentication procedure

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: Part of Authentication procedure

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode procedure

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command Security setup complete
- **Conditions**:
  - UE successfully sets up security
- **Timing**: End Security Mode procedure

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration process
- **Conditions**:
  - Registration successful
- **Timing**: End Registration procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure successful
  - UE authorized to register
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: After sending Authentication Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete AMF registers UE
- **Conditions**:
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - Registration accepted by UE
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Upon receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Upon receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command and applies security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Upon receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Prerequisite steps completed
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Prerequisite steps completed
- **Timing**: Upon receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session the initial registration request cannot be accepted by the network
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command Security setup complete
- **Conditions**:
  - Security setup complete
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: Stop T3550

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: Stop T3510

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context does not exist Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received
- **Conditions**:
  - Security Mode Complete received
- **Timing**: Start T3520

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: Stop T3520

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information from UDM
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security mode configuration successful
- **Timing**: After Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security configuration
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful Authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode command successfully processed
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers the UE
- **Conditions**:
  - Authentication and security procedures successful
  - UE context established
- **Timing**: After successful Security Mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept message successfully processed
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful security mode procedure
  - All registration checks passed
- **Timing**: After successful security mode procedure

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context does not exist
  - Authentication is required

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs to authenticate the UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the authentication challenge

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication is successful
  - AMF has security capabilities of the UE

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup is successful

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete Registration successful
- **Conditions**:
  - Security mode procedure is complete
  - Registration is successful

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration is accepted by the network

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure complete
  - All necessary information obtained
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration acceptance
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has applied the security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Registration successful
  - Security context established
- **Timing**: After security mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by the network
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command and applies security
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE has successfully registered
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security successful
  - Registration parameters validated
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by AMF
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information for the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Authentication and security procedures successful
  - UE context established in AMF
- **Timing**: After security mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE applies security configuration
- **Conditions**:
  - UE applies security configuration
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - AMF completes registration procedure
- **Timing**: Stop T3510

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode command successfully processed
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Successful authentication and security mode procedure
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept message successfully processed
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode command successfully processed
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication and security setup
  - UE context established
- **Timing**: After security mode complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the subscriber
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup successful Registration successful
- **Conditions**:
  - UE is authorized
  - Network resources allocated
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete
- **Conditions**:
  - Successful security mode procedure
  - Network authorizes registration
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: N/A

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: Stop T3510

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF triggers AUSF to request authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish secure communication
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful Authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security Mode Command received and processed successfully
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete AMF authorizes registration
- **Conditions**:
  - Security Mode procedure successful
  - UE is authorized to register
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors to authenticate the UE
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with the UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has successfully configured security
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF has successfully registered the UE
- **Conditions**:
  - Authentication and security procedures successful
  - UE authorized to access the network
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE has successfully registered with the network
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context does not exist
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers the UE
- **Conditions**:
  - Successful registration with the network
- **Timing**: After security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security mode
- **Conditions**:
  - Security mode successfully applied
- **Timing**: After applying security mode

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication and security mode setup
- **Timing**: After security mode complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security context with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security mode setup successful
  - UE context established in AMF
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE responds with authentication information
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE supports the authentication method

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete UE context established
- **Conditions**:
  - UE context established
  - Security mode setup complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Successful authentication and security setup
- **Conditions**:
  - Successful authentication and security setup
  - All necessary network functions are configured
- **Timing**: After security mode complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration acceptance
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs authentication vectors
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration requirements met
- **Conditions**:
  - Security mode procedure complete
  - Registration requirements met
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration acceptance
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully calculates authentication response
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete All necessary procedures are completed
- **Conditions**:
  - Registration successful
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration is complete
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After AMF forwards Authentication Request to AUSF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Successful security mode procedure
  - Registration successful
- **Timing**: After successful security mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully authenticates
- **Timing**: After UE completes authentication procedure

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to secure communication
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After UE completes security mode setup

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration of the UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Registration successful
- **Timing**: After AMF completes registration procedure

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration is complete
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After UE receives Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete AMF authorizes registration
- **Conditions**:
  - UE is authorized to register
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE completes authentication procedure
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - UE completes security mode setup
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - AMF completes registration procedure
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE receives Registration Accept from AMF
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF triggers AUSF to request authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command from AMF

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Successful registration
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Security context does not exist
- **Timing**: After receiving Registration Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete
- **Conditions**:
  - UE is authorized to access the network
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Registration Request received Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication required
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication Request received
- **Conditions**:
  - UE has processed Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Command received and processed
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration Accept received
- **Conditions**:
  - Registration Accept received
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to authenticate the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Successful authentication and security mode setup
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context does not exist
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE has processed the Authentication Request
- **Timing**: After receiving Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE has applied the security configuration
- **Conditions**:
  - Security mode setup is complete
- **Timing**: After receiving Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF has completed registration procedures
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE has received and processed the Registration Accept message
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish secure communication with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After processing Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures successful
  - UE authorized to access the network
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - No authentication vectors available
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE responds with authentication information
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully sets up security
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete
- **Conditions**:
  - Security mode procedure successful
  - All necessary information obtained
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms successful registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request from UE Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication and security setup

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE receives Security Mode Command
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - No valid authentication vectors available
- **Timing**: After receiving Registration Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security context with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully sets up security
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security setup successful
  - UE authorized to register
- **Timing**: After security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start Authentication procedure

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF requests authentication vectors from AUSF
- **Conditions**:
  - Authentication required
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode procedure

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete AMF registers UE
- **Conditions**:
  - Registration successful
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: Stop T3510

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures successful
  - UE authorized to access the network
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information for the UE
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes the Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After processing Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures are successful
  - UE is authorized to register
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes the Registration Accept message
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish secure communication
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode command processed successfully
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers UE
- **Conditions**:
  - Successful authentication and security mode procedure
- **Timing**: After security mode procedure

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF triggers authentication
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete
- **Conditions**:
  - Security mode procedure successful
  - UE context established in AMF
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start Authentication procedure

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE receives Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode procedure

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - UE completes security mode setup
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - AMF completes registration procedure
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE receives Registration Accept
- **Timing**: Stop T3510

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security context
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures are successful
  - UE is authorized to access the network
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After UE completes authentication calculations

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully sets up security
- **Conditions**:
  - Security mode setup successful
- **Timing**: After UE configures security

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers the UE
- **Conditions**:
  - Successful authentication and security mode setup
- **Timing**: After successful security mode setup

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration accept
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context does not exist Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF needs to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security setup
  - UE context established in AMF
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully applies security configuration
- **Conditions**:
  - Security mode command received and processed successfully
- **Timing**: On receipt of Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedures
- **Conditions**:
  - Successful authentication and security mode setup
- **Timing**: After successful security mode setup

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes the Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with the UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies the security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers the UE
- **Conditions**:
  - Authentication and security procedures are successful
  - UE is authorized to access the network
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes the Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities need to be negotiated
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security mode setup successful
  - UE authorized to register
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE supports the authentication method
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities required
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command from AMF
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - UE is authorized to access the network
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms the registration
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - Registration Accept received successfully
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete AMF accepts registration
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes the Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with the UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully applies the security configuration
- **Conditions**:
  - Security mode setup successful
- **Timing**: After applying security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers the UE
- **Conditions**:
  - Authentication and security procedures complete
  - UE authorized to access the network
- **Timing**: After security mode complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes the Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Registration Request received Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start Authentication procedure

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF requests authentication vectors from AUSF
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication Request received
- **Conditions**:
  - UE has processed Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode procedure

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Security Mode Command received and processed
- **Conditions**:
  - Security Mode Command processed successfully
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Security Mode procedure complete
  - Registration successful
- **Timing**: N/A

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration Accept received
- **Conditions**:
  - Registration Accept received
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors for the UE
- **Conditions**:
  - AUSF needs to retrieve authentication information
- **Timing**: After AMF triggers authentication

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF accepts the registration request
- **Conditions**:
  - Authentication and security procedures successful
  - UE authorized to access the network
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: Start Authentication timer

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: N/A

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: N/A

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: Stop Authentication timer

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: Start Security Mode timer

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: Stop Security Mode timer

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode procedure complete Registration successful
- **Conditions**:
  - Successful registration with the network
- **Timing**: N/A

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and determines authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication vectors to authenticate the UE
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes the Authentication Request
- **Timing**: After UE completes authentication procedure

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - UE successfully applies the security configuration
- **Timing**: After UE configures security

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication and security setup
- **Timing**: After successful registration procedure

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes the Registration Accept message
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup successful AMF completes registration
- **Conditions**:
  - Registration successful
- **Timing**: After Security Mode Complete

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by UE
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Registration Request received Security context not established
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AMF requests authentication vectors from AUSF
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication Request received
- **Conditions**:
  - Authentication Request received
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities needed
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE completes security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Security Mode Command received
- **Conditions**:
  - Security Mode Command received
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode setup complete Registration accepted
- **Conditions**:
  - Security procedures complete
  - UE authorized
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration Accept received
- **Conditions**:
  - Registration Accept received
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and needs to authenticate the UE
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs to retrieve authentication information for the UE
- **Timing**: After AMF forwards Authentication Request to AUSF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After UE processes Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish secure communication with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - UE successfully applies security configuration
- **Timing**: After UE applies security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security procedures are successful
  - UE is authorized to register
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After UE processes Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After UE completes authentication calculations

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - UE successfully configures security
- **Timing**: After UE configures security

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Authentication and security successful
  - Registration successful
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After UE receives Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF receives Authentication Request from AMF
- **Timing**: On receipt of Authentication Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security with UE
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security mode setup successful
- **Timing**: On successful security configuration

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF successfully registers UE
- **Conditions**:
  - Authentication and security procedures complete
  - UE context established in AMF
- **Timing**: After successful security mode setup

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully computes authentication response
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF initiates security mode procedure
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to secure communication
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms security mode setup
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF accepts the registration request
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication
  - Successful security mode setup
  - UE context established
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE confirms registration completion
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request to UE

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: After receiving Authentication Request from AMF

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes security mode setup
- **Conditions**:
  - Security mode setup successful
- **Timing**: After receiving Security Mode Command from AMF

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration successful
- **Conditions**:
  - Successful registration and security setup
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: After receiving Registration Accept from AMF

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF requires authentication information
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF receives Authentication Response
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security Mode Complete received
- **Conditions**:
  - Registration successful
  - All necessary parameters are available
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by the network
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request Security context not exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: After receiving Registration Request

#### 3. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - AUSF needs authentication vectors
- **Timing**: After receiving Authentication Request from AMF

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request from AMF
- **Conditions**:
  - UE receives Authentication Request from AMF
- **Timing**: After receiving Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Security Mode Command from AMF
- **Conditions**:
  - UE receives Security Mode Command from AMF
- **Timing**: After receiving Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete Registration successful
- **Conditions**:
  - Security mode procedure complete
  - Registration successful
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept from AMF
- **Conditions**:
  - UE receives Registration Accept from AMF
- **Timing**: After receiving Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - UE is not yet registered and has a valid PLMN
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request and authentication is required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: N/A

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - AMF requires authentication vectors to authenticate the UE
- **Timing**: N/A

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE successfully processes the Authentication Request
- **Timing**: N/A

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF selects security algorithms
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: N/A

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE successfully configures security
- **Conditions**:
  - Security mode setup successful
- **Timing**: N/A

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: AMF completes registration procedure
- **Conditions**:
  - Successful authentication and security setup
  - UE context established in AMF
- **Timing**: Stop T3510

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - UE successfully processes Registration Accept
- **Timing**: N/A

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF receives Registration Request
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After sending Authentication Request

#### 4. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE receives Authentication Request
- **Conditions**:
  - UE successfully processes Authentication Request
- **Timing**: On receipt of Authentication Request

#### 5. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE to activate security
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful AMF needs to establish security
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 6. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete to AMF after security activation
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Security Mode Command
- **Conditions**:
  - Security mode setup successful
- **Timing**: On receipt of Security Mode Command

#### 7. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Security mode procedure complete AMF completes registration
- **Conditions**:
  - Registration successful
  - UE context established
- **Timing**: After Security Mode Complete

#### 8. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration accepted by the network
- **Timing**: On receipt of Registration Accept

---

## Initial Registration
Complete 5G Initial Registration procedure

### Network Elements
- **UE**: User Equipment initiating registration
- **AMF**: Access and Mobility Management Function
- **AUSF**: Authentication Server Function
- **UDM**: Unified Data Management
- **PCF**: Policy Control Function
- **NSSF**: Network Slice Selection Function
- **SMSF**: SMS Forwarding Function
- **GGSF**: Gateway GPRS Support Function
- **HSS**: Home Subscriber Server
- **SMF**: Session Management Function

### Procedure Flow

#### 1. Registration Request
- **Source**: UE
- **Target**: AMF
- **Description**: UE initiates registration procedure
- **Source State**: 5GMM-DEREGISTERED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE sends Registration Request to AMF UE power on UE out of coverage UE needs to establish an emergency PDU session UE needs to establish an emergency PDU session
- **Conditions**:
  - No current registration exists
  - UE in 5GMM-DEREGISTERED state
- **Timing**: Start T3510

#### 2. Authentication Request
- **Source**: AMF
- **Target**: UE
- **Description**: AMF requests authentication information from UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: No security context exists Authentication required
- **Conditions**:
  - Security context not exists
  - Authentication required
- **Timing**: On receipt of Registration Request

#### 3. Authentication Vector Request
- **Source**: AMF
- **Target**: AUSF
- **Description**: AMF requests authentication vectors from AUSF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: AMF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Registration Request

#### 4. Authentication Vector Request
- **Source**: AUSF
- **Target**: UDM
- **Description**: AUSF requests authentication vectors from UDM
- **Source State**: N/A
- **Target State**: N/A
- **Trigger**: AUSF needs authentication vectors
- **Conditions**:
  - Authentication required
- **Timing**: After receiving Authentication Vector Request from AMF

#### 5. Authentication Response
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends authentication response to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE completes authentication procedure
- **Conditions**:
  - UE has processed Authentication Request
- **Timing**: After processing Authentication Request

#### 6. Security Mode Command
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends security mode command to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: Authentication successful Security capabilities received
- **Conditions**:
  - Authentication successful
  - Security capabilities received
- **Timing**: After successful authentication

#### 7. Security Mode Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends security mode complete message to AMF
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED-INITIATED
- **Trigger**: UE has applied security configuration
- **Conditions**:
  - Security Mode Command received and processed
- **Timing**: After applying security configuration

#### 8. Registration Accept
- **Source**: AMF
- **Target**: UE
- **Description**: AMF sends registration accept message to UE
- **Source State**: 5GMM-REGISTERED-INITIATED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: Registration successful
- **Conditions**:
  - Registration successful
- **Timing**: After successful security mode procedure

#### 9. Registration Complete
- **Source**: UE
- **Target**: AMF
- **Description**: UE sends registration complete message to AMF
- **Source State**: 5GMM-REGISTERED
- **Target State**: 5GMM-REGISTERED
- **Trigger**: UE receives Registration Accept
- **Conditions**:
  - Registration Accept received
- **Timing**: After receiving Registration Accept

---
>>>>>>> f6782aa2945b2d8857cc56efcdb82409178f0d5a

