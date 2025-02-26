# Extracted Data from processed_data\semantic_chunks.md (Chunk 1)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 3)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 5)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 6)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 7)

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
  "description": "Session Management Function - Manages user sessions"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 8)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 10)

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
  "description": "UE is in the initial state, not registered"
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
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and in limited service"
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "FINAL",
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
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF initiates authentication procedure",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity verification required"
  ],
  "timing": "T3560 starts"
}

{
  "sequence_number": 3,
  "step_name": "Authentication Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "AMF rejects authentication",
  "trigger": "Authentication fails",
  "conditions": [
    "UE identity verification failed"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 4,
  "step_name": "SNPN Selection",
  "source_element": "UE",
  "destination_element": "N/A",
  "message": "SNPN Selection",
  "source_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "destination_state": "5GMM-NULL",
  "description": "UE performs SNPN selection",
  "trigger": "Authentication Reject received",
  "conditions": [
    "SNPN access operation mode"
  ],
  "timing": "N/A"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 11)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 12)

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

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control, selection of UPF"
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
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the 5G network"
}

{
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

## Registration Flow

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 13)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to connect to the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Responsible for registration, authentication, authorization, and mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Responsible for session management, PDU session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules to the SMF"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 14)

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
  "trigger": "UE powers on and has at least one active PDN connection which the UE intends to transfer to TNGF or N3IWF connected to 5GCN",
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 15)

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
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control, selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement, traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control plane function(s)"
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
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating with the 5G network"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the 5G network"
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
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
  "message": "Authentication Reject",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "AMF rejects authentication",
  "trigger": "Authentication fails",
  "conditions": [
    "USIM considered invalid"
  ],
  "timing": "Timers stopped"
}

{
  "sequence_number": 4,
  "step_name": "Registration Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED",
  "description": "AMF rejects registration",
  "trigger": "Various reasons like PLMN not allowed, tracking area not allowed, etc.",
  "conditions": [
    "Various conditions based on the cause value"
  ],
  "timing": "N/A"
}

{
  "sequence_number": 5,
  "step_name": "Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts registration",
  "trigger": "Successful authentication and authorization",
  "conditions": [
    "UE authorized to access the network"
  ],
  "timing": "N/A"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 16)

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
  "description": "User Plane Function - responsible for user plane traffic forwarding"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 17)

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
  "description": "UE is in a null state, typically after power-on or USIM insertion."
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
  "description": "UE initiates registration procedure by sending a REGISTRATION REQUEST message to the AMF, starting timer T3510.",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services after unavailability period.",
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
  "source_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "destination_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "description": "AMF may initiate authentication procedure.",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs verification"
  ],
  "timing": "T3560 starts"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 18)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 19)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 20)

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
  "name": "5GMM-REGISTERING-AUTHENTICATING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of authenticating during registration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service"
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
  "step_name": "Registration Rejection",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "AMF rejects the registration request",
  "trigger": "Registration fails",
  "conditions": [
    "N1 mode not allowed"
  ],
  "timing": "T3346 expires or is stopped"
}

{
  "sequence_number": 4,
  "step_name": "Registration Rejection",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "description": "AMF rejects the registration request",
  "trigger": "Registration fails",
  "conditions": [
    "Roaming not allowed"
  ],
  "timing": "N/A"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 21)

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
  "description": "Network Repository Function - Provides service discovery"
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
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
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
  "description": "UE is registered but service is not allowed"
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
  "name": "5GMM-CONNECTED mode with RRC inactive indication",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode with RRC inactive indication"
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
  "step_name": "UE Authentication Response",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Authentication Response",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE sends authentication response to AMF",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE successfully authenticated"
  ],
  "timing": "After UE authentication procedure"
}

{
  "sequence_number": 4,
  "step_name": "AMF Security Mode Command",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Security Mode Command",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF initiates security mode setup",
  "trigger": "Successful authentication",
  "conditions": [
    "Integrity protection and ciphering required"
  ],
  "timing": "After successful authentication"
}

{
  "sequence_number": 5,
  "step_name": "UE Security Mode Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Security Mode Complete",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERING",
  "description": "UE completes security mode setup",
  "trigger": "Security Mode Command received",
  "conditions": [
    "Security mode setup successful"
  ],
  "timing": "After successful security mode setup"
}

{
  "sequence_number": 6,
  "step_name": "AMF Registration Accept",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Accept",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-REGISTERED",
  "description": "AMF accepts the registration request",
  "trigger": "Successful security mode setup",
  "conditions": [
    "UE authorized to access the network"
  ],
  "timing": "T3550 starts"
}

{
  "sequence_number": 7,
  "step_name": "UE Registration Complete",
  "source_element": "UE",
  "destination_element": "AMF",
  "message": "Registration Complete",
  "source_state": "5GMM-REGISTERED",
  "destination_state": "5GMM-REGISTERED",
  "description": "UE confirms the registration",
  "trigger": "Registration Accept received",
  "conditions": [
    "Registration successful"
  ],
  "timing": "After Registration Accept"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 22)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 23)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 25)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 26)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 27)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 28)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates registration and communicates with the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages UE registration, authentication, and mobility"
}

{
  "name": "AUSF",
  "type": "Network Element",
  "description": "Authentication Server Function - Authenticates the UE"
}

{
  "name": "SEAF",
  "type": "Network Element",
  "description": "Security Anchor Function - Derives KAMF from KSEAF"
}

{
  "name": "AAA server of the CH or the DCS",
  "type": "Network Element",
  "description": "AAA server of the Credentials Holder (CH) or the Default Credentials Server (DCS) - Acts as EAP server"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered in the network"
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
  "description": "AMF initiates authentication procedure by sending an EAP-Request message",
  "trigger": "Valid Registration Request received",
  "conditions": [
    "UE identity needs to be verified"
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
  "description": "UE responds to the authentication request with an EAP-Response message",
  "trigger": "Receiving AUTHENTICATION REQUEST (EAP-request)",
  "conditions": [
    "UE processes EAP-request message"
  ],
  "timing": "T3520 starts if authentication fails, stops if running"
}

{
  "sequence_number": 4,
  "step_name": "Authentication Result/Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "AUTHENTICATION RESULT (EAP-success) or AUTHENTICATION REJECT (EAP-failure)",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF sends the result of the authentication procedure to the UE",
  "trigger": "Authentication procedure completes",
  "conditions": [
    "Authentication successful or unsuccessful"
  ],
  "timing": "N/A"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 29)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to register"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration and mobility"
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
  "description": "State after deregistration"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "State after deregistration and PLMN search"
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
  "timing": "Upon reception of Authentication Reject"
}

{
  "sequence_number": 4,
  "step_name": "SNPN Selection after Authentication Reject",
  "source_element": "UE",
  "destination_element": "N/A",
  "message": "SNPN Selection",
  "source_state": "5GMM-DEREGISTERED",
  "destination_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "description": "UE performs SNPN selection after authentication reject for onboarding services",
  "trigger": "Authentication Reject received during onboarding services registration",
  "conditions": [
    "SNPN-specific attempt counter exceeds maximum value"
  ],
  "timing": "After Authentication Reject"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 30)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 31)

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
  "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
  "description": "UE responds to authentication request",
  "trigger": "Authentication Request received",
  "conditions": [
    "UE successfully processes authentication challenge"
  ],
  "timing": "UE processes authentication challenge"
}

{
  "sequence_number": 4,
  "step_name": "AMF Security Mode Command",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Security Mode Command",
  "source_state": "5GMM-REGISTERING-AUTHENTICATING",
  "destination_state": "5GMM-REGISTERING",
  "description": "AMF initiates security mode control procedure",
  "trigger": "Successful authentication",
  "conditions": [
    "Authentication procedure successful"
  ],
  "timing": "After successful authentication"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 32)

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
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control plane functions for policy enforcement and charging"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement and traffic usage reporting"
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 33)

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
  "description": "User Plane Function - Routes and forwards user plane data"
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
  "trigger": "UE powers on and needs to register to the network",
  "conditions": [
    "UE in coverage area",
    "Valid USIM"
  ],
  "timing": "UE sends the Registration Request message"
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
  "timing": "AMF sends the Authentication Request message"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 34)

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

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "State after deregistration with limited service"
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "FINAL",
  "description": "State after deregistration with no cell available"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "State after deregistration and PLMN search"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 35)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates the registration procedure"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Manages registration, authentication, and mobility"
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
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and in limited service mode"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
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
  "trigger": "UE powers on or after PLMN/SNPN selection",
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
  "step_name": "Registration Reject",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "Registration Reject",
  "source_state": "5GMM-REGISTERING",
  "destination_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "description": "AMF rejects the registration request",
  "trigger": "Authentication failure or other reasons",
  "conditions": [
    "Integrity protection passed",
    "Operating in SNPN access mode"
  ],
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
  "description": "AMF rejects the registration request",
  "trigger": "Authentication failure or other reasons",
  "conditions": [
    "Registration request is not for onboarding services in SNPN",
    "3GPP access"
  ],
  "timing": "N/A"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 37)

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
  "step_name": "AMF Receives NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "source_element": "NSSAAF",
  "destination_element": "AMF",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "source_state": null,
  "destination_state": null,
  "description": "AMF receives the NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE message from NSSAAF",
  "trigger": "NSSAAF completes authentication",
  "conditions": [
    "Authentication with AAA-S complete"
  ],
  "timing": "Timer T3575 stopped",
  "relationship_type": "RECEIVES_MESSAGE_FROM"
}

{
  "sequence_number": 2,
  "step_name": "AMF Creates NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_state": null,
  "destination_state": null,
  "description": "AMF creates a NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message",
  "trigger": "Receipt of NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "conditions": [
    "EAP-success or EAP-failure message available"
  ],
  "timing": "Immediately after receiving NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "relationship_type": "CREATES_MESSAGE"
}

{
  "sequence_number": 3,
  "step_name": "AMF Sends NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_state": null,
  "destination_state": null,
  "description": "AMF sends the NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message to the UE",
  "trigger": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message created",
  "conditions": [
    "UE is reachable"
  ],
  "timing": "Immediately after creating NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 4,
  "step_name": "UE Receives NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_element": "AMF",
  "destination_element": "UE",
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "source_state": null,
  "destination_state": null,
  "description": "UE receives the NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message from the AMF",
  "trigger": "AMF sends NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "conditions": [
    "UE is reachable"
  ],
  "timing": "Upon receipt of NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "relationship_type": "RECEIVES_MESSAGE_FROM"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 38)

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
  "description": "Network Repository Function - Provides service discovery"
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered"
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "FINAL",
  "description": "UE is deregistered, no SUPI available"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered, searching for PLMN"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered, limited service available"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "FINAL",
  "description": "UE is deregistered, attempting registration"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 39)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, mobility management, authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control, selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement, traffic usage reporting"
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered to the network"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 40)

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
  "description": "Session Management Function - responsible for session management (PDU sessions)"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane data transfer"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 41)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 42)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
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
  "description": "Initial state of the UE before registration"
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering to the network"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 43)

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
  "description": "UE is in the process of authenticating to the network"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 44)

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
  "timing": "Upon receiving REGISTRATION REJECT",
  "relationship_type": "SENDS_MESSAGE_TO"
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
  "timing": "Upon receiving REGISTRATION REJECT",
  "relationship_type": "SENDS_MESSAGE_TO"
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
  "timing": "Upon receiving REGISTRATION REJECT",
  "relationship_type": "SENDS_MESSAGE_TO"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 45)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 46)

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
  "description": "Session Management Function - responsible for session management (session establishment, modification and release), UE IP address allocation & control, selection of UPF"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for packet routing & forwarding, policy enforcement, traffic usage reporting"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules to control data flow and access to network resources"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 47)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 48)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 49)

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
  "description": "Session Management Function - responsible for session management, IP address allocation"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane traffic forwarding and QoS enforcement"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules for session management and charging"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - service discovery"
}

## States

{
  "name": "5GMM-IDLE",
  "type": "INITIAL",
  "description": "UE is in idle mode"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
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
  "trigger": "UE has uplink signalling or user data pending, or receives a paging request",
  "conditions": [
    "5GS update status is 5U1 UPDATED",
    "TAI of the current serving cell is included in the TAI list",
    "No 5GMM specific procedure is ongoing"
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
  "trigger": "AMF validates the service request",
  "conditions": [
    "UE is authorized to access the network"
  ],
  "timing": "T3517 stops"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 50)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 51)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 52)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 53)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 54)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, connection management, mobility"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 55)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 56)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 57)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 58)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Initiates and responds to PDU session procedures"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Manages PDU sessions"
}

## States

{
  "name": "PDU SESSION ACTIVE",
  "type": "FINAL",
  "description": "PDU session is established and active"
}

{
  "name": "PROCEDURE TRANSACTION INACTIVE",
  "type": "FINAL",
  "description": "No active procedure transaction"
}

## Registration Flow

{
  "sequence_number": 1,
  "step_name": "PDU Session Authentication Command",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION AUTHENTICATION COMMAND <EAP-request message A>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "SMF sends authentication request to UE",
  "trigger": "DN requires authentication and authorization of the UE",
  "conditions": [],
  "timing": "Start T3590",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 2,
  "step_name": "PDU Session Authentication Complete",
  "source_element": "UE",
  "destination_element": "SMF",
  "message": "PDU SESSION AUTHENTICATION COMPLETE <EAP-response message to EAP-request message A>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "UE responds to authentication request with EAP response",
  "trigger": "Receipt of EAP-request message from SMF",
  "conditions": [],
  "timing": "Stop T3590",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 3,
  "step_name": "PDU Session Authentication Command (Retransmission)",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION AUTHENTICATION COMMAND <EAP-request message B>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "SMF retransmits authentication request to UE",
  "trigger": "DN requires authentication and authorization of the UE",
  "conditions": [],
  "timing": "Start T3590",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 4,
  "step_name": "PDU Session Authentication Complete (Retransmission)",
  "source_element": "UE",
  "destination_element": "SMF",
  "message": "PDU SESSION AUTHENTICATION COMPLETE <EAP-response message to EAP-request message B>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "UE responds to authentication request with EAP response",
  "trigger": "Receipt of EAP-request message from SMF",
  "conditions": [],
  "timing": "Stop T3590",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 5,
  "step_name": "PDU Session Establishment Accept/Reject",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION ESTABLISHMENT ACCEPT <EAP-success message> OR PDU SESSION ESTABLISHMENT REJECT <EAP-failure message>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "SMF sends PDU session establishment accept or reject based on authentication result",
  "trigger": "Successful or unsuccessful DN authentication",
  "conditions": [],
  "timing": "N/A",
  "relationship_type": "SENDS_MESSAGE_TO"
}

{
  "sequence_number": 6,
  "step_name": "PDU Session Authentication Result/Release Command",
  "source_element": "SMF",
  "destination_element": "UE",
  "message": "PDU SESSION AUTHENTICATION RESULT <EAP-success message> OR PDU SESSION RELEASE COMMAND <EAP-failure message>",
  "source_state": "PDU SESSION ACTIVE",
  "destination_state": "PDU SESSION ACTIVE",
  "description": "SMF sends PDU session authentication result or release command based on authentication result",
  "trigger": "Successful or unsuccessful DN authentication",
  "conditions": [],
  "timing": "N/A",
  "relationship_type": "SENDS_MESSAGE_TO"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 59)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 61)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, mobility management, and access authentication and authorization"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, including session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane data transfer, packet routing & forwarding, policy rule enforcement and traffic usage reporting"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 63)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 66)

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

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, including PDU session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - responsible for user plane data forwarding and routing"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - provides policy rules for session management and charging"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - provides service discovery and NF instance selection"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 68)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - device used by the end user to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, reachability management, authentication, and authorization"
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
    "UE identity verified"
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
  "trigger": "AMF completes EAP authentication",
  "conditions": [
    "EAP authentication successful"
  ],
  "timing": "After AMF completes EAP authentication"
}

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 69)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 70)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 71)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 74)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 77)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 80)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - manages registration, connection management, mobility"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 81)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 87)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 102)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 113)

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 119)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to connect to the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Responsible for registration, authentication, and mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Responsible for session management, including PDU session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Responsible for user plane data forwarding and routing"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules for session management and QoS control"
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function - Provides service discovery and selection functionality"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 121)

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
  "description": "Policy Control Function - provides policy rules to the SMF and other network functions"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 122)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to connect to the 5G network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - Responsible for registration, authentication, and mobility management"
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - Responsible for PDU session management"
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function - Responsible for user plane data transfer"
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function - Provides policy rules for session management"
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
  "description": "UE is not registered in the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered in the 5G network"
}

## Registration Flow

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

