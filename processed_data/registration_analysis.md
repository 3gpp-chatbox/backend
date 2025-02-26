# Extracted Data from processed_data\semantic_chunks.md (Chunk 1)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Device used by the end user to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules to other network functions."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that supports service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network."
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode after registration."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE has an established connection with the network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from the network."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts to access the 5G network.",
  "condition": "UE is powered on and within coverage.",
  "timing": "Initial step of the registration procedure."
}

{
  "step": 2,
  "message": "AUTHENTICATION REQUEST",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication procedure.",
  "condition": "UE identity needs to be verified.",
  "timing": "After receiving the REGISTRATION REQUEST message."
}

{
  "step": 3,
  "message": "AUTHENTICATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "Authentication fails.",
  "condition": "UE fails to authenticate.",
  "timing": "After authentication procedure."
}

{
  "step": 4,
  "message": "SECURITY MODE COMMAND",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates security mode control procedure.",
  "condition": "Secure exchange of NAS messages needs to be established.",
  "timing": "After successful authentication."
}

{
  "step": 5,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF accepts the registration request.",
  "condition": "Authentication and security mode control are successful.",
  "timing": "After successful security mode control procedure."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management."
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with PCF to obtain policy rules."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF uses NRF for service discovery."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts to access the 5G network."
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication procedure."
}

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "Authentication fails."
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "AMF initiates security mode control procedure."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "AMF accepts the registration request."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE is powered on and within coverage."
}

{
  "state": "5GMM-REGISTERING",
  "condition": "UE identity needs to be verified."
}

{
  "state": "5GMM-DEREGISTERED",
  "condition": "UE fails to authenticate."
}

{
  "state": "5GMM-REGISTERING",
  "condition": "Secure exchange of NAS messages needs to be established."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "Authentication and security mode control are successful."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of the registration procedure."
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After receiving the REGISTRATION REQUEST message."
}

{
  "state": "5GMM-DEREGISTERED",
  "timing": "After authentication procedure."
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After successful authentication."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful security mode control procedure."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 3)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, reachability management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Responsible for session management, including session establishment, modification and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Responsible for user plane handling, including packet routing and forwarding."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy rules to control network behavior."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery function."
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE communicates with AMF for registration and mobility management via the N1 interface."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 5)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 6)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Core network element responsible for registration, authentication, and mobility management"
}

{
  "name": "AUSF",
  "type": "Authentication Server Function",
  "description": "Core network element responsible for authentication"
}

{
  "name": "SEAF",
  "type": "Security Anchor Function",
  "description": "Core network element responsible for security anchoring"
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

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts to register with the network",
  "condition": "UE is powered on and attempting network access",
  "timing": "Initial step of the registration procedure"
}

{
  "step": 2,
  "message": "AUTHENTICATION REQUEST",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication procedure",
  "condition": "AMF requires authentication of the UE",
  "timing": "After receiving the REGISTRATION REQUEST"
}

{
  "step": 3,
  "message": "AUTHENTICATION RESPONSE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE responds to authentication challenge",
  "condition": "UE successfully calculates authentication response",
  "timing": "After receiving the AUTHENTICATION REQUEST"
}

{
  "step": 4,
  "message": "SECURITY MODE COMMAND",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates security mode control procedure",
  "condition": "Authentication is successful and AMF needs to establish secure communication",
  "timing": "After successful authentication"
}

{
  "step": 5,
  "message": "SECURITY MODE COMPLETE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE completes security mode control procedure",
  "condition": "UE successfully configures security parameters",
  "timing": "After receiving the SECURITY MODE COMMAND"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses"
}

{
  "element1": "AMF",
  "element2": "AUSF",
  "relationship": "AMF interacts with AUSF for authentication purposes"
}

{
  "element1": "AUSF",
  "element2": "SEAF",
  "relationship": "AUSF interacts with SEAF to obtain security keys"
}

{
  "element1": "SEAF",
  "element2": "AMF",
  "relationship": "SEAF provides security keys to the AMF"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST"
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "AMF sends AUTHENTICATION REQUEST"
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "AMF sends SECURITY MODE COMMAND"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "UE sends SECURITY MODE COMPLETE"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE is within network coverage"
}

{
  "state": "5GMM-REGISTERING",
  "condition": "UE successfully authenticates with the network"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE successfully configures security parameters"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial registration attempt"
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After receiving REGISTRATION REQUEST"
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After successful authentication"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful security mode control"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 7)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, authentication and authorization."
}

## States

## Transitions

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests and other NAS messages to the AMF. AMF authenticates the UE and manages its connection."
}

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 8)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access 5G services."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access control."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules for session management and charging."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that stores and provides information about available network functions."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network and can access 5G services."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network."
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE powers on and attempts to register with the network.",
  "condition": "UE must be within the coverage area of a 5G network.",
  "timing": "Initial step of the registration procedure."
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication of the UE.",
  "condition": "UE identity needs to be verified by the network.",
  "timing": "After the AMF receives the Registration Request from the UE."
}

{
  "step": 3,
  "message": "Security Mode Command",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates security mode control procedure.",
  "condition": "Successful authentication.",
  "timing": "After successful authentication."
}

{
  "step": 4,
  "message": "Security Mode Complete",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE completes security mode control procedure.",
  "condition": "Successful security mode setup.",
  "timing": "After receiving Security Mode Command."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests and other NAS messages to the AMF, and receives responses from the AMF."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with the SMF to manage PDU sessions for the UE."
}

{
  "element1": "AMF",
  "element2": "UPF",
  "relationship": "AMF interacts with the UPF to establish user plane connectivity for the UE."
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with the PCF to obtain policy rules for the UE's session."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF discovers other network functions (e.g., SMF) through the NRF."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE powers on and attempts to register with the network."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful completion of the registration procedure."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be within the coverage area of a 5G network."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "Successful authentication and security mode setup."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of the registration procedure."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "Final step of the registration procedure."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 10)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN or SNPN."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has limited service."
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has no SUPI."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "Unknown",
  "to_state": "Unknown",
  "trigger": "UE attempts to register with the network.",
  "condition": "UE must be in a coverage area.",
  "timing": "Initial registration attempt."
}

{
  "step": 2,
  "message": "AUTHENTICATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Unknown",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "Network rejects authentication.",
  "condition": "Authentication fails.",
  "timing": "After authentication procedure."
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Unknown",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Network rejects registration.",
  "condition": "Registration is not allowed.",
  "timing": "After registration request."
}

{
  "step": 4,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Unknown",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects registration.",
  "condition": "Registration is not allowed.",
  "timing": "After registration request."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE and manages its registration status."
}

## Triggers

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Registration reject, authentication reject, or other failures."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Registration reject, authentication reject, or other failures."
}

{
  "state": "5GMM-DEREGISTERED.NO-SUPI",
  "trigger": "Authentication failure."
}

## Conditions

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "UE is not allowed to register in the current PLMN/SNPN."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "UE is not allowed to register in the current PLMN/SNPN."
}

{
  "state": "5GMM-DEREGISTERED.NO-SUPI",
  "condition": "Authentication failure."
}

## Timing

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "Occurs after a registration or authentication failure."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "Occurs after a registration or authentication failure."
}

{
  "state": "5GMM-DEREGISTERED.NO-SUPI",
  "timing": "Occurs after an authentication failure."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 11)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
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

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE powers on and attempts to register with the network",
  "condition": "UE must be in a coverage area and select a PLMN or SNPN",
  "timing": "Initial step of the registration procedure"
}

{
  "step": 2,
  "message": "AUTHENTICATION REQUEST",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication of the UE",
  "condition": "UE identity needs to be verified",
  "timing": "After receiving the REGISTRATION REQUEST"
}

{
  "step": 3,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF successfully authenticates and authorizes the UE",
  "condition": "Authentication and authorization are successful",
  "timing": "After successful authentication"
}

{
  "step": 4,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "AMF rejects the registration request",
  "condition": "Authentication or authorization fails, or other network policies prevent registration",
  "timing": "After authentication or authorization failure"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses (accept or reject)"
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to manage PDU sessions and network slices"
}

{
  "element1": "AMF",
  "element2": "UPF",
  "relationship": "AMF interacts with UPF to manage user plane traffic"
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with PCF to obtain policy control information"
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF uses NRF for service discovery"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "AMF sends REGISTRATION ACCEPT"
}

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "AMF sends REGISTRATION REJECT"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE is in coverage and selects a PLMN/SNPN"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "Authentication and authorization are successful"
}

{
  "state": "5GMM-DEREGISTERED",
  "condition": "Authentication or authorization fails, or network policies prevent registration"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful authentication"
}

{
  "state": "5GMM-DEREGISTERED",
  "timing": "After authentication or authorization failure"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 12)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy control for the network"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 13)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages registration, connection, and mobility"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy rules"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
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
  "description": "User Equipment: Mobile device attempting to access the network."
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function: Manages registration, connection, and mobility."
}

{
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function: Manages PDU sessions."
}

{
  "name": "UPF",
  "type": "Network Element",
  "description": "User Plane Function: Routes and forwards user plane data."
}

{
  "name": "PCF",
  "type": "Network Element",
  "description": "Policy Control Function: Provides policy rules for session management."
}

{
  "name": "NRF",
  "type": "Network Element",
  "description": "Network Repository Function: Service discovery."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
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
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access 5G services."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access control."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules to the control plane functions."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that supports service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "Initial state of the UE when it is not registered with the network."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service state."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts initial registration.",
  "condition": "UE is powered on and attempting to access the network.",
  "timing": "First step in the registration procedure."
}

{
  "step": 2,
  "message": "AUTHENTICATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "Network rejects authentication.",
  "condition": "Authentication procedure is not accepted by the network.",
  "timing": "After the UE sends the REGISTRATION REQUEST and the network initiates authentication."
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects registration.",
  "condition": "PLMN not allowed, tracking area not allowed, etc.",
  "timing": "After the UE sends the REGISTRATION REQUEST."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management during registration."
}

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "UE attempts initial registration."
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "Network rejects authentication or registration."
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE is powered on and attempting to access the network."
}

{
  "state": "5GMM-REGISTERING",
  "condition": "Authentication procedure is not accepted by the network or PLMN not allowed, tracking area not allowed, etc."
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "First step in the registration procedure."
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After the UE sends the REGISTRATION REQUEST and the network initiates authentication."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 16)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, connection management, mobility management, and access control"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management, including PDU session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for providing policy rules to the SMF and other network functions"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element that provides service discovery and selection capabilities"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
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
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access control."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules for session management and mobility management."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that provides service discovery and selection capabilities."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is in an initial state, not registered with the network."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is attempting to register after a previous registration attempt failed."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is searching for a PLMN to register with."
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is attempting to update its registration with the network."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is in a state where it can only access limited services."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services after unavailability period.",
  "condition": "UE needs to access 5GS services or emergency services.",
  "timing": "Initial step of the registration procedure."
}

{
  "step": 2,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects the registration request.",
  "condition": "Various reasons, including PLMN not allowed, N1 mode not allowed, etc.",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

{
  "step": 3,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network accepts the registration request.",
  "condition": "UE is authorized to access the network.",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives registration accept or reject messages from the AMF."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management during the registration procedure."
}

## Triggers

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services after unavailability period."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects the registration request."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network accepts the registration request."
}

## Conditions

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "condition": "UE needs to access 5GS services or emergency services."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "Various reasons, including PLMN not allowed, N1 mode not allowed, etc."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE is authorized to access the network."
}

## Timing

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "timing": "Initial step of the registration procedure."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 18)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, authentication, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function responsible for service discovery"
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
  "name": "5GMM-DEREGISTERED-INITIATED",
  "type": "INTERMEDIATE",
  "description": "UE has requested release of the 5GMM context and is waiting for a response from the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "A 5GMM context has been established"
}

## Transitions

{
  "step": 1,
  "message": "Initial registration requested",
  "from_element": "UE",
  "to_element": "Network",
  "from_state": "5GMM-DEREGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE starts the initial registration procedure",
  "condition": "UE camps on a suitable cell or an acceptable cell in a PLMN",
  "timing": "When the UE needs to establish a 5GMM context"
}

{
  "step": 2,
  "message": "UE enters state 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "from_element": "UE",
  "to_element": "Network",
  "from_state": "5GMM-DEREGISTERED.eCALL-INACTIVE",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "UE receives a request from upper layers to establish an eCall over IMS",
  "condition": "UE needs to establish an eCall over IMS",
  "timing": "At the earliest opportunity"
}

{
  "step": 3,
  "message": "UE enters state 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "from_element": "UE",
  "to_element": "Network",
  "from_state": "5GMM-DEREGISTERED.eCALL-INACTIVE",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "UE receives a request from upper layers to establish a call to an HPLMN designated non-emergency MSISDN or URI for test or terminal reconfiguration service",
  "condition": "UE needs to establish a non-emergency call",
  "timing": "Once the registration procedure is completed"
}

{
  "step": 4,
  "message": "UE enters state 5GMM-NULL",
  "from_element": "UE",
  "to_element": "Network",
  "from_state": "5GMM-DEREGISTERED.eCALL-INACTIVE",
  "to_state": "5GMM-NULL",
  "trigger": "UE is deactivated (e.g. powered off) by the user",
  "condition": "UE is powered off",
  "timing": "When the UE is powered off"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF"
}

{
  "element1": "AMF",
  "element2": "UE",
  "relationship": "AMF authenticates the UE"
}

## Triggers

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "UE starts the initial registration procedure"
}

{
  "state": "5GMM-DEREGISTERED.eCALL-INACTIVE",
  "trigger": "USIM is removed, coverage is lost, UE is deactivated, UE receives a request from upper layers to establish an eCall over IMS, UE receives a request from upper layers to establish a call to an HPLMN designated non-emergency MSISDN or URI for test or terminal reconfiguration service"
}

## Conditions

{
  "state": "5GMM-DEREGISTERED",
  "condition": "UE camps on a suitable cell or an acceptable cell in a PLMN"
}

{
  "state": "5GMM-DEREGISTERED.eCALL-INACTIVE",
  "condition": "Valid subscriber data are available for the UE before it enters the substates, except for the substate 5GMM-DEREGISTERED.NO-SUPI"
}

## Timing

{
  "state": "5GMM-DEREGISTERED",
  "timing": "When the UE needs to establish a 5GMM context"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "timing": "At the earliest opportunity, Once the registration procedure is completed"
}

{
  "state": "5GMM-NULL",
  "timing": "When the UE is powered off"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 19)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - Mobile device attempting to access the network"
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
  "description": "User Plane Function - Routes user data"
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
  "description": "Initial state, UE is not registered"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INITIAL",
  "description": "UE is deregistered from the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
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
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN"
}

{
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and SUPI is not available"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration"
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is registered and attempting registration update"
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and no cell is available"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-DEREGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services",
  "condition": "UE selects a PLMN or SNPN",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request/Response (if needed)",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

{
  "step": 3,
  "message": "Registration Accept",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF accepts the registration request",
  "condition": "Authentication is successful and other network policies are met",
  "timing": "After authentication (if any)"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF and receives registration responses from AMF. AMF authenticates the UE."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to manage PDU sessions for the UE."
}

{
  "element1": "AMF",
  "element2": "UPF",
  "relationship": "AMF interacts with UPF to route user data for the UE."
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with PCF to obtain policy rules for the UE."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF uses NRF for service discovery."
}

## Triggers

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "UE performs initial registration for 5GS services, emergency services, SMS over NAS, moves from GERAN/UTRAN to NG-RAN, performs initial registration for onboarding services in SNPN, disaster roaming services, or to resume normal services"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful completion of the initial registration procedure"
}

## Conditions

{
  "state": "5GMM-DEREGISTERED",
  "condition": "UE selects a PLMN or SNPN"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "Authentication is successful and other network policies are met"
}

## Timing

{
  "state": "5GMM-DEREGISTERED",
  "timing": "Initial state before registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "Final state after successful registration"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 20)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "N/A",
  "trigger": "UE needs to register to the network",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration request messages to the AMF."
}

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "UE needs to register to the network"
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE must be in coverage area"
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "Initial step of registration"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 21)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane data forwarding and routing."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules for session management and mobility management."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that provides service discovery and selection capabilities."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the 5G network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode."
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered with limited service."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and searching for a PLMN."
}

{
  "name": "5GMM-REGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but no cell is available."
}

{
  "name": "5GMM-REGISTERED.NON-ALLOWED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but service is not allowed."
}

{
  "name": "5GMM-REGISTERED-INITIATED",
  "type": "INTERMEDIATE",
  "description": "UE initiated registration."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE powers on and attempts to register to the network.",
  "condition": "UE must be in a coverage area and have a valid USIM.",
  "timing": "Initial step of the registration procedure."
}

{
  "step": 2,
  "message": "AUTHENTICATION REQUEST",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "AMF initiates authentication of the UE.",
  "condition": "UE identity needs to be verified.",
  "timing": "After receiving the REGISTRATION REQUEST from the UE."
}

{
  "step": 3,
  "message": "AUTHENTICATION RESPONSE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE responds to the authentication request.",
  "condition": "UE successfully completes the authentication procedure.",
  "timing": "After receiving the AUTHENTICATION REQUEST from the AMF."
}

{
  "step": 4,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF accepts the registration request.",
  "condition": "UE is successfully authenticated and authorized.",
  "timing": "After successful authentication and authorization."
}

{
  "step": 5,
  "message": "REGISTRATION COMPLETE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE confirms the registration acceptance.",
  "condition": "UE successfully receives the REGISTRATION ACCEPT message.",
  "timing": "After receiving the REGISTRATION ACCEPT from the AMF."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives registration responses from the AMF. The AMF manages the UE's registration status."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to establish and manage PDU sessions for the UE."
}

{
  "element1": "AMF",
  "element2": "UPF",
  "relationship": "AMF interacts with UPF to manage user plane resources for the UE."
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with PCF to obtain policy rules for the UE's session and mobility management."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF uses NRF to discover and select appropriate network functions."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts to register to the network."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful completion of the registration procedure."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in a coverage area and have a valid USIM."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE must be successfully authenticated and authorized by the network."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of the registration procedure."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful authentication and authorization."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 22)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules to the SMF and other network functions."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that provides service discovery and selection capabilities."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the network."
}

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode."
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode."
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is deregistered from the network."
}

{
  "name": "5GMM-REGISTERED.NO-CELL-AVAILABLE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but no cell is available."
}

{
  "name": "5GMM-REGISTERED.NORMAL-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered and has normal service."
}

{
  "name": "5GMM-REGISTERED.NON-ALLOWED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is registered but has non-allowed service."
}

{
  "name": "5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE",
  "type": "INTERMEDIATE",
  "description": "UE is registered and attempting registration update."
}

{
  "name": "5GMM-COMMON-PROCEDURE-INITIATED",
  "type": "INTERMEDIATE",
  "description": "A common 5GMM procedure has been initiated."
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
  "type": "User Equipment",
  "description": "Mobile device used to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Not explicitly mentioned in the provided text, but a core network element responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Not explicitly mentioned in the provided text, but a core network element responsible for user plane handling"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Not explicitly mentioned in the provided text, but a core network element responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Not explicitly mentioned in the provided text, but a core network element responsible for service discovery"
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
  "name": "5GMM-REGISTERED-INITIATED",
  "type": "INTERMEDIATE",
  "description": "UE has initiated registration"
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
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE needs to register with the network (initial registration)",
  "condition": "UE is powered on and needs to access the network",
  "timing": "Initial step of registration procedure"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Successful completion of authentication and security procedures",
  "condition": "UE identity is verified and security context is established",
  "timing": "After the AMF receives the Registration Request and performs authentication"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE and manages its registration status."
}

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "UE needs to register with the network (initial registration)"
}

{
  "state": "5GMM-REGISTERING",
  "trigger": "Successful completion of authentication and security procedures"
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE is powered on and needs to access the network"
}

{
  "state": "5GMM-REGISTERING",
  "condition": "UE identity is verified and security context is established"
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "Initial step of registration procedure"
}

{
  "state": "5GMM-REGISTERING",
  "timing": "After the AMF receives the Registration Request and performs authentication"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 26)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "5G Core Network Element",
  "description": "Access and Mobility Management Function. Responsible for registration, authentication, and mobility management."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 27)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, authentication and authorization."
}

{
  "name": "AUSF",
  "type": "Authentication Server Function",
  "description": "Network function responsible for authentication of the UE."
}

{
  "name": "AAA server",
  "type": "Authentication, Authorization, and Accounting server",
  "description": "Server responsible for authentication, authorization, and accounting."
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
  "description": "State of the UE during the registration procedure."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "State of the UE after successful registration."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

{
  "step": 3,
  "message": "AUTHENTICATION RESULT or AUTHENTICATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF completes authentication procedure",
  "condition": "Authentication must be successful",
  "timing": "After UE responds to Authentication Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses."
}

{
  "element1": "AMF",
  "element2": "AUSF",
  "relationship": "AMF interacts with AUSF for authentication of the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends Registration Request"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful authentication and registration procedure"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in a coverage area and have valid credentials"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE must successfully authenticate with the network"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Occurs immediately after the UE attempts to access the network"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "Occurs after successful completion of the registration and authentication procedures"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 28)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management"
}

{
  "name": "AUSF",
  "type": "Authentication Server Function",
  "description": "Network element responsible for authentication"
}

{
  "name": "SEAF",
  "type": "Security Anchor Functionality",
  "description": "Provides security anchor functionality"
}

{
  "name": "AAA server of the CH or the DCS",
  "type": "Authentication, Authorization, and Accounting Server of the Credentials Holder or the Default Credentials Server",
  "description": "Network element responsible for authentication, authorization, and accounting"
}

{
  "name": "5G-RG",
  "type": "5G Residential Gateway",
  "description": "Acts on behalf of an AUN3 device"
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network"
}

## Transitions

{
  "step": 1,
  "message": "AUTHENTICATION REQUEST",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "AMF initiates authentication procedure",
  "condition": "UE needs to be authenticated",
  "timing": "After initial contact"
}

{
  "step": 2,
  "message": "AUTHENTICATION RESPONSE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "UE responds to authentication request",
  "condition": "UE successfully processes authentication challenge",
  "timing": "After receiving AUTHENTICATION REQUEST"
}

{
  "step": 3,
  "message": "AUTHENTICATION RESULT or AUTHENTICATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "AMF provides authentication result",
  "condition": "Authentication successful or failed",
  "timing": "After AMF validates authentication response"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests and receives authentication challenges from the AMF"
}

{
  "element1": "AMF",
  "element2": "AUSF",
  "relationship": "AMF interacts with AUSF for authentication of the UE"
}

{
  "element1": "AUSF",
  "element2": "SEAF",
  "relationship": "AUSF provides KSEAF to the SEAF"
}

{
  "element1": "SEAF",
  "element2": "AMF",
  "relationship": "SEAF provides ngKSI and the KAMF to the AMF"
}

{
  "element1": "AMF",
  "element2": "AAA server of the CH or the DCS",
  "relationship": "AMF interacts with AAA server of the CH or the DCS for authentication of the UE"
}

{
  "element1": "5G-RG",
  "element2": "AUN3 device",
  "relationship": "5G-RG acts on behalf of the AUN3 device"
}

## Triggers

{
  "state": "N/A",
  "trigger": "AMF initiates authentication procedure"
}

{
  "state": "N/A",
  "trigger": "UE responds to authentication request"
}

{
  "state": "N/A",
  "trigger": "AMF provides authentication result"
}

## Conditions

{
  "state": "N/A",
  "condition": "UE needs to be authenticated"
}

{
  "state": "N/A",
  "condition": "UE successfully processes authentication challenge"
}

{
  "state": "N/A",
  "condition": "Authentication successful or failed"
}

## Timing

{
  "state": "N/A",
  "timing": "After initial contact"
}

{
  "state": "N/A",
  "timing": "After receiving AUTHENTICATION REQUEST"
}

{
  "state": "N/A",
  "timing": "After AMF validates authentication response"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 29)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the network."
}

## States

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and needs to perform PLMN/SNPN selection."
}

## Transitions

{
  "step": 1,
  "message": "Authentication Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Unknown",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of AUTHENTICATION REJECT message",
  "condition": "UE is registered for onboarding services in SNPN or performing initial registration for onboarding services in SNPN and the SNPN-specific attempt counter for the SNPN sending the AUTHENTICATION REJECT message has a value greater than or equal to a UE implementation-specific maximum value.",
  "timing": "After the UE has sent a registration request and the network has initiated authentication."
}

{
  "step": 2,
  "message": "Authentication Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Unknown",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of AUTHENTICATION REJECT message",
  "condition": "The AUTHENTICATION REJECT message has been successfully integrity checked by the NAS and the UE is performing initial registration for onboarding services in SNPN.",
  "timing": "After the UE has sent a registration request and the network has initiated authentication."
}

## Network Element Relationships

## Triggers

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of AUTHENTICATION REJECT message"
}

## Conditions

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "UE is registered for onboarding services in SNPN or performing initial registration for onboarding services in SNPN and the SNPN-specific attempt counter for the SNPN sending the AUTHENTICATION REJECT message has a value greater than or equal to a UE implementation-specific maximum value."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "The AUTHENTICATION REJECT message has been successfully integrity checked by the NAS and the UE is performing initial registration for onboarding services in SNPN."
}

## Timing

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After the UE has sent a registration request and the network has initiated authentication."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 30)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management."
}

{
  "name": "5G-RG",
  "type": "5G Residential Gateway",
  "description": "Acts on behalf of the AUN3 device"
}

{
  "name": "W-AGF",
  "type": "Wireless Access Gateway Function",
  "description": "Acts on behalf of the N5GC device"
}

## States

{
  "name": "5GMM-DEREGISTERED",
  "type": "FINAL",
  "description": "UE is not registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "AUTHENTICATION REJECT",
  "from_element": "Network",
  "to_element": "W-AGF or 5G-RG",
  "from_state": "Any",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "Network fails to authenticate the N5GC or AUN3 device",
  "condition": "EAP-failure message received in an AUTHENTICATION REJECT message",
  "timing": "After authentication failure"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, AMF authenticates the UE."
}

{
  "element1": "5G-RG",
  "element2": "AMF",
  "relationship": "5G-RG acts on behalf of AUN3 device and communicates with AMF for authentication"
}

{
  "element1": "W-AGF",
  "element2": "AMF",
  "relationship": "W-AGF acts on behalf of N5GC device and communicates with AMF for authentication"
}

## Triggers

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "Reception of AUTHENTICATION REJECT message by W-AGF or 5G-RG"
}

## Conditions

{
  "state": "5GMM-DEREGISTERED",
  "condition": "EAP-failure message received in an AUTHENTICATION REJECT message"
}

## Timing

{
  "state": "5GMM-DEREGISTERED",
  "timing": "Occurs after the network sends an AUTHENTICATION REJECT message to the W-AGF or 5G-RG"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 31)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, authentication, and mobility management"
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
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERING",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

{
  "step": 3,
  "message": "Authentication Failure",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-NULL",
  "trigger": "Authentication fails after timer T3520 expires or after consecutive EAP-based authentication failures",
  "condition": "Authentication check fails",
  "timing": "After Authentication Request"
}

{
  "step": 4,
  "message": "Security Mode Command",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF sends Security Mode Command after successful authentication",
  "condition": "UE has an emergency PDU session established or is establishing one, and receives the SECURITY MODE COMMAND message before the timeout of timer T3520",
  "timing": "After Authentication Request and Authentication Response"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests and authentication responses to the AMF, and the AMF sends authentication requests and security mode commands to the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access or Network initiates authentication"
}

{
  "state": "5GMM-NULL",
  "trigger": "Authentication fails after timer T3520 expires or after consecutive EAP-based authentication failures"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "AMF sends Security Mode Command after successful authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area or UE identity verification required"
}

{
  "state": "5GMM-NULL",
  "condition": "Authentication check fails"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE has an emergency PDU session established or is establishing one, and receives the SECURITY MODE COMMAND message before the timeout of timer T3520"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration or After UE sends Registration Request"
}

{
  "state": "5GMM-NULL",
  "timing": "After Authentication Request"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After Authentication Request and Authentication Response"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 32)

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
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and needs to perform PLMN selection"
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and can only access limited services"
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and attempting registration"
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts to register to the network",
  "condition": "UE is powered on and within network coverage",
  "timing": "Initial registration attempt"
}

{
  "step": 2,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF accepts the registration request",
  "condition": "Authentication and authorization are successful",
  "timing": "After successful authentication and authorization"
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "AMF rejects the registration request",
  "condition": "Registration is not allowed due to PLMN restrictions",
  "timing": "After AMF determines registration is not allowed"
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF rejects the registration request",
  "condition": "Registration is not allowed due to CAG restrictions",
  "timing": "After AMF determines registration is not allowed"
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "AMF rejects the registration request",
  "condition": "Registration is not allowed due to UAS restrictions",
  "timing": "After AMF determines registration is not allowed"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives registration accept or reject messages from the AMF."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to manage PDU sessions during registration."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "AMF sends REGISTRATION ACCEPT"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "AMF sends REGISTRATION REJECT with specific cause values"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF sends REGISTRATION REJECT with specific cause values"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "AMF sends REGISTRATION REJECT with specific cause values"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE is within network coverage and attempts to register"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE is successfully authenticated and authorized"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "Registration is rejected due to PLMN restrictions"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "Registration is rejected due to CAG restrictions"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "condition": "Registration is rejected due to UAS restrictions"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration procedure"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful authentication and authorization"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After AMF determines registration is not allowed"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After AMF determines registration is not allowed"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "timing": "After AMF determines registration is not allowed"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 33)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access authentication/authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Responsible for session management, including session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Responsible for user plane data transfer and routing."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy rules for session management and mobility management."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery function."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area.",
  "timing": "Initial step of registration."
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests and other NAS messages to the AMF."
}

{
  "element1": "AMF",
  "element2": "UE",
  "relationship": "AMF authenticates the UE and manages its mobility."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management."
}

{
  "element1": "SMF",
  "element2": "UPF",
  "relationship": "SMF controls the UPF for user plane data transfer."
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF retrieves policy rules from PCF."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF uses NRF for service discovery."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends Registration Request to AMF."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful authentication and registration procedure."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in a coverage area and have a valid subscription."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE must successfully authenticate with the network."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Occurs immediately after the UE attempts to access the network."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "Occurs after successful completion of the registration procedure."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 34)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered in the 5G network."
}

{
  "name": "5GMM-REGISTERING",
  "type": "INTERMEDIATE",
  "description": "UE is in the process of registering with the 5G network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE has completed the registration procedure."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and has limited service."
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "FINAL",
  "description": "UE is deregistered and no cell is available."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and searching for a PLMN."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access.",
  "condition": "UE must be in coverage area.",
  "timing": "Initial step of registration."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST to AMF."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area to initiate registration."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Occurs at the beginning of the registration procedure."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 35)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and performing PLMN selection."
}

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-NULL",
  "trigger": "UE powers on and attempts to register with the network.",
  "condition": "UE must be within coverage area of a 5G network.",
  "timing": "Initial step of the registration procedure."
}

{
  "step": 2,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects the registration request.",
  "condition": "Registration is not allowed for the UE in the current PLMN or SNPN.",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Network rejects the registration request.",
  "condition": "Registration is not allowed for the UE in the current PLMN or SNPN.",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF responds with registration accept or reject messages."
}

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "UE powers on and attempts to register with the network."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Network rejects the registration request."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Network rejects the registration request."
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE must be within coverage area of a 5G network."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "Registration is not allowed for the UE in the current PLMN or SNPN."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "Registration is not allowed for the UE in the current PLMN or SNPN."
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "Initial step of the registration procedure."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After the AMF receives the REGISTRATION REQUEST."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 37)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device attempting to access the network"
}

{
  "name": "AMF",
  "type": "Network Element",
  "description": "Access and Mobility Management Function - responsible for registration, connection management, and mobility management"
}

{
  "name": "AAA-S",
  "type": "Network Element",
  "description": "Authentication, Authorization, and Accounting Server"
}

{
  "name": "NSSAAF",
  "type": "Network Element",
  "description": "Network Slice-Specific Authentication and Authorization Function"
}

## States

## Transitions

{
  "step": 1,
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "UE completes network slice-specific authentication",
  "condition": "UE has performed network slice-specific authentication",
  "timing": "After network slice-specific authentication is complete"
}

{
  "step": 2,
  "message": "NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "AMF receives EAP-success or EAP-failure message from AAA-S",
  "condition": "AMF has received the result of network slice-specific authentication",
  "timing": "After AMF receives authentication result from AAA-S"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends NETWORK SLICE-SPECIFIC AUTHENTICATION COMPLETE message to AMF"
}

{
  "element1": "AMF",
  "element2": "AAA-S",
  "relationship": "AMF provides EAP-response message to AAA-S via NSSAAF"
}

{
  "element1": "AMF",
  "element2": "UE",
  "relationship": "AMF sends NETWORK SLICE-SPECIFIC AUTHENTICATION RESULT message to UE"
}

{
  "element1": "AAA-S",
  "element2": "AMF",
  "relationship": "AAA-S provides EAP-success or EAP-failure message to AMF via NSSAAF"
}

## Triggers

{
  "state": "N/A",
  "trigger": "UE completes network slice-specific authentication"
}

{
  "state": "N/A",
  "trigger": "AMF receives EAP-success or EAP-failure message from AAA-S"
}

## Conditions

{
  "state": "N/A",
  "condition": "UE has performed network slice-specific authentication"
}

{
  "state": "N/A",
  "condition": "AMF has received the result of network slice-specific authentication"
}

## Timing

{
  "state": "N/A",
  "timing": "After network slice-specific authentication is complete"
}

{
  "state": "N/A",
  "timing": "After AMF receives authentication result from AAA-S"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 38)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane traffic forwarding"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element responsible for service discovery"
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
  "name": "5GMM-DEREGISTERED.NO-SUPI",
  "type": "FINAL",
  "description": "UE is deregistered and SUPI is not available"
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
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "FINAL",
  "description": "UE is deregistered and attempting registration"
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts to register with the network",
  "condition": "UE needs to access 5GS services",
  "timing": "Initial step of registration"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST message"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE needs to access 5GS services"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 39)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration management, connection management, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane handling"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element responsible for service discovery"
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
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
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

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE powers on and attempts to access the network",
  "condition": "UE must be within network coverage",
  "timing": "Initial step of the registration procedure"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF manages the UE's registration status."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends REGISTRATION REQUEST to AMF"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be within network coverage to send REGISTRATION REQUEST"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Occurs at the beginning of the registration procedure"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 40)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration management, connection management, and mobility management"
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
  "description": "UE is in the process of registering with the 5G network"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration request to AMF"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 41)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management"
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
  "description": "UE is in the process of registering with the 5G network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the 5G network"
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
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and in limited service mode"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts initial registration",
  "condition": "UE is powered on and attempting to connect to the network",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Registration Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "AMF rejects the registration request due to congestion",
  "condition": "General NAS level mobility management congestion control",
  "timing": "After AMF receives Registration Request"
}

{
  "step": 3,
  "message": "Registration Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "AMF rejects the registration request due to serving network not authorized",
  "condition": "Serving network not authorized",
  "timing": "After AMF receives Registration Request"
}

{
  "step": 4,
  "message": "Registration Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF rejects the registration request due to N1 mode not allowed",
  "condition": "N1 mode not allowed",
  "timing": "After AMF receives Registration Request"
}

{
  "step": 5,
  "message": "Registration Reject",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF rejects the registration request due to all S-NSSAI(s) in the allowed NSSAI and configured NSSAI are rejected and at least one S-NSSAI is rejected due to S-NSSAI not available in the current registration area",
  "condition": "all S-NSSAI(s) in the allowed NSSAI and configured NSSAI are rejected and at least one S-NSSAI is rejected due to S-NSSAI not available in the current registration area",
  "timing": "After AMF receives Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates and manages the UE's connection to the network."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE sends a Registration Request message"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "AMF sends a Registration Reject message due to congestion"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "AMF sends a Registration Reject message due to serving network not authorized"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF sends a Registration Reject message due to N1 mode not allowed"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF sends a Registration Reject message due to all S-NSSAI(s) in the allowed NSSAI and configured NSSAI are rejected and at least one S-NSSAI is rejected due to S-NSSAI not available in the current registration area"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE is powered on and attempting to connect to the network"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "condition": "General NAS level mobility management congestion control"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "Serving network not authorized"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "N1 mode not allowed"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "all S-NSSAI(s) in the allowed NSSAI and configured NSSAI are rejected and at least one S-NSSAI is rejected due to S-NSSAI not available in the current registration area"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "timing": "After AMF receives Registration Request"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After AMF receives Registration Request"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After AMF receives Registration Request"
}

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After AMF receives Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 42)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "FINAL",
  "description": "UE is deregistered and can only access limited services."
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "FINAL",
  "description": "UE is deregistered and needs to perform PLMN selection."
}

{
  "name": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "type": "FINAL",
  "description": "UE is deregistered but attempting registration."
}

{
  "name": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "type": "FINAL",
  "description": "UE is deregistered and no cell is available."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Any",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "AMF rejects registration due to tracking area restrictions or SNPN access restrictions.",
  "condition": "UE is not operating in SNPN access mode and Forbidden TAI(s) for the list of '5GS forbidden tracking areas for regional provision of service' IE is not included in the REGISTRATION REJECT message or UE is operating in SNPN access mode.",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "step": 2,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Any",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "AMF rejects registration due to PLMN not allowed or IAB-node operation not authorized.",
  "condition": "UE is not operating in SNPN access mode.",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "step": 3,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Any",
  "to_state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "AMF rejects registration due to congestion or UAS services not allowed or UE does not access 5GCN over non-3GPP access using the TNGF or has not indicated support for slice-based TNGF selection.",
  "condition": "None specified",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "step": 4,
  "message": "REGISTRATION REJECT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "Any",
  "to_state": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "trigger": "AMF rejects registration due to redirection to EPC required.",
  "condition": "UE has indicated support for CIoT optimizations or not indicated support for S1 mode or received by a UE over non-3GPP access.",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF sends registration reject messages to the UE."
}

## Triggers

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Reception of REGISTRATION REJECT message with specific cause values and conditions related to tracking area restrictions or SNPN access restrictions."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of REGISTRATION REJECT message with specific cause values and conditions related to PLMN not allowed or IAB-node operation not authorized."
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "trigger": "Reception of REGISTRATION REJECT message with specific cause values and conditions related to congestion or UAS services not allowed or UE does not access 5GCN over non-3GPP access using the TNGF or has not indicated support for slice-based TNGF selection."
}

{
  "state": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "trigger": "Reception of REGISTRATION REJECT message with specific cause values and conditions related to redirection to EPC required."
}

## Conditions

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "UE is not operating in SNPN access mode and Forbidden TAI(s) for the list of '5GS forbidden tracking areas for regional provision of service' IE is not included in the REGISTRATION REJECT message or UE is operating in SNPN access mode."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "UE is not operating in SNPN access mode."
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "condition": "None specified"
}

{
  "state": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "condition": "UE has indicated support for CIoT optimizations or not indicated support for S1 mode or received by a UE over non-3GPP access."
}

## Timing

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "state": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

{
  "state": "5GMM-DEREGISTERED.NO-CELL-AVAILABLE",
  "timing": "After UE sends Registration Request and AMF determines registration is not allowed."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 44)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

## States

{
  "name": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and has limited service"
}

{
  "name": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered and needs to perform PLMN selection"
}

{
  "name": "EMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from EPS"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from 5GMM"
}

## Transitions

{
  "step": 1,
  "message": "Registration Reject with cause #76 from CAG cell",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Reception of Registration Reject with cause #76 from a CAG cell",
  "condition": "Entry in CAG information list for current PLMN does not include an indication that the UE is only allowed to access 5GS via CAG cells OR entry includes the indication and one or more CAG-IDs are authorized based on the updated allowed CAG list",
  "timing": "After UE attempts registration"
}

{
  "step": 2,
  "message": "Registration Reject with cause #76 from CAG cell",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of Registration Reject with cause #76 from a CAG cell",
  "condition": "Entry in CAG information list for current PLMN includes an indication that the UE is only allowed to access 5GS via CAG cells and no CAG-ID is authorized based on the updated allowed CAG list",
  "timing": "After UE attempts registration"
}

{
  "step": 3,
  "message": "Registration Reject with cause #76 from CAG cell",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Reception of Registration Reject with cause #76 from a CAG cell",
  "condition": "CAG information list does not include an entry for the current PLMN",
  "timing": "After UE attempts registration"
}

{
  "step": 4,
  "message": "Registration Reject with cause #76 from non-CAG cell",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Reception of Registration Reject with cause #76 from a non-CAG cell",
  "condition": "One or more CAG-IDs are authorized based on the allowed CAG list for the current PLMN",
  "timing": "After UE attempts registration"
}

{
  "step": 5,
  "message": "Registration Reject with cause #76 from non-CAG cell",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of Registration Reject with cause #76 from a non-CAG cell",
  "condition": "No CAG-ID is authorized based on the allowed CAG list for the current PLMN",
  "timing": "After UE attempts registration"
}

{
  "step": 6,
  "message": "Registration Reject with cause #77 from wireline access",
  "from_element": "Network",
  "to_element": "UE",
  "from_state": "ANY",
  "to_state": "5GMM-DEREGISTERED",
  "trigger": "Reception of Registration Reject with cause #77 from a wireline access network",
  "condition": "Message received over wireline access network",
  "timing": "After UE attempts registration"
}

## Network Element Relationships

## Triggers

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "trigger": "Reception of Registration Reject with cause #76 and specific CAG conditions"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "trigger": "Reception of Registration Reject with cause #76 and specific CAG conditions"
}

{
  "state": "5GMM-DEREGISTERED",
  "trigger": "Reception of Registration Reject with cause #77 from wireline access"
}

## Conditions

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "condition": "Specific CAG conditions related to allowed CAG list and CAG information list"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "condition": "Specific CAG conditions related to allowed CAG list and CAG information list"
}

{
  "state": "5GMM-DEREGISTERED",
  "condition": "Message received over wireline access network"
}

## Timing

{
  "state": "5GMM-DEREGISTERED.LIMITED-SERVICE",
  "timing": "After UE attempts registration"
}

{
  "state": "5GMM-DEREGISTERED.PLMN-SEARCH",
  "timing": "After UE attempts registration"
}

{
  "state": "5GMM-DEREGISTERED",
  "timing": "After UE attempts registration"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 45)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic handling."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for policy control."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function responsible for service discovery."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE sends a REGISTRATION REQUEST message with 5GS registration type IE set to 'initial registration'.",
  "condition": "UE must be in coverage area and attempting initial registration.",
  "timing": "Initial step of registration."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to manage sessions."
}

## Triggers

{
  "state": "5GMM-REGISTERED",
  "trigger": "UE sends a REGISTRATION REQUEST message with 5GS registration type IE set to 'initial registration'."
}

## Conditions

{
  "state": "5GMM-REGISTERED",
  "condition": "UE must be in coverage area and attempting initial registration."
}

## Timing

{
  "state": "5GMM-REGISTERED",
  "timing": "Initial step of registration."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 46)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts initial registration.",
  "condition": "UE must be in coverage area.",
  "timing": "Initial step of registration."
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication.",
  "condition": "UE identity verification required.",
  "timing": "After UE sends Registration Request."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts initial registration."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 47)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "N/A",
  "trigger": "UE attempts initial registration.",
  "condition": "UE must be in coverage area.",
  "timing": "Initial step of registration."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF."
}

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "UE attempts initial registration."
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE must be in coverage area."
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "Initial step of registration."
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 49)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment, modification, and release"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding and policy enforcement"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for providing policy rules to the SMF and other network functions"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function that stores and provides information about available network functions"
}

## States

{
  "name": "5GMM-IDLE",
  "type": "INTERMEDIATE",
  "description": "UE is in idle mode, not actively communicating with the network"
}

{
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is in connected mode, actively communicating with the network"
}

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

## Transitions

{
  "step": 1,
  "message": "SERVICE REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-IDLE",
  "to_state": "5GMM-CONNECTED",
  "trigger": "UE has uplink signalling or user data pending, receives a paging request, or other triggers as defined in subclause 5.6.1.1",
  "condition": "5GS update status is 5U1 UPDATED, and the TAI of the current serving cell is included in the TAI list; and no 5GMM specific procedure is ongoing",
  "timing": "Initiated by the UE when certain conditions are met"
}

{
  "step": 2,
  "message": "SERVICE ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-CONNECTED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "AMF successfully processes the SERVICE REQUEST message",
  "condition": "AMF accepts the service request",
  "timing": "After the AMF processes the SERVICE REQUEST message"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends SERVICE REQUEST to AMF and receives SERVICE ACCEPT from AMF"
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF to manage PDU sessions and user-plane resources"
}

## Triggers

{
  "state": "5GMM-CONNECTED",
  "trigger": "UE has uplink signalling or user data pending, receives a paging request, or other triggers as defined in subclause 5.6.1.1"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "AMF successfully processes the SERVICE REQUEST message"
}

## Conditions

{
  "state": "5GMM-CONNECTED",
  "condition": "5GS update status is 5U1 UPDATED, and the TAI of the current serving cell is included in the TAI list; and no 5GMM specific procedure is ongoing"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "AMF accepts the service request"
}

## Timing

{
  "state": "5GMM-CONNECTED",
  "timing": "Initiated by the UE when certain conditions are met"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After the AMF processes the SERVICE REQUEST message"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 50)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy control for the network"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
}

## States

{
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network"
}

## Transitions

{
  "step": 1,
  "message": "CONTROL PLANE SERVICE REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-REGISTERED",
  "to_state": "5GMM-REGISTERED",
  "trigger": "UE has uplink CIoT user data, SMS or location services message to be sent",
  "condition": "UE is in 5GMM-REGISTERED state",
  "timing": "After UE is registered and needs to send data"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends CONTROL PLANE SERVICE REQUEST to AMF"
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management"
}

## Triggers

{
  "state": "5GMM-REGISTERED",
  "trigger": "UE has uplink CIoT user data, SMS or location services message to be sent"
}

## Conditions

{
  "state": "5GMM-REGISTERED",
  "condition": "UE is in 5GMM-REGISTERED state"
}

## Timing

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE is registered and needs to send data"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 51)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Responsible for session management, including PDU session establishment, modification, and release."
}

## States

{
  "name": "PDU SESSION ACTIVE",
  "type": "INTERMEDIATE",
  "description": "PDU session is established and active."
}

{
  "name": "PDU SESSION MODIFICATION PENDING",
  "type": "INTERMEDIATE",
  "description": "PDU session modification is in progress."
}

{
  "name": "PDU SESSION INACTIVE PENDING",
  "type": "INTERMEDIATE",
  "description": "PDU session is in the process of being deactivated."
}

## Transitions

{
  "step": 1,
  "message": "PDN CONNECTIVITY REQUEST",
  "from_element": "UE",
  "to_element": "SMF",
  "from_state": "S1 Mode",
  "to_state": "N1 Mode",
  "trigger": "Inter-system change from S1 mode to N1 mode",
  "condition": "UE supports interworking to 5GS",
  "timing": "During inter-system change from S1 to N1"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "SMF",
  "relationship": "UE sends PDU session related requests to the SMF, and SMF manages the PDU session."
}

## Triggers

{
  "state": "PDU SESSION ACTIVE",
  "trigger": "Inter-system change from S1 mode to N1 mode and default EPS bearer context in state BEARER CONTEXT ACTIVE"
}

## Conditions

{
  "state": "PDU SESSION ACTIVE",
  "condition": "Default EPS bearer context in state BEARER CONTEXT ACTIVE"
}

## Timing

{
  "state": "PDU SESSION ACTIVE",
  "timing": "After inter-system change from S1 mode to N1 mode"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 52)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to connect to the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management, including PDU session establishment, modification, and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane traffic forwarding and QoS enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for providing policy rules for session management and QoS control."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element that stores network function instance profiles and supports service discovery."
}

## States

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 53)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access authentication/authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including session establishment, modification, and release."
}

## States

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 54)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management, including PDU session establishment and modification."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane data forwarding and QoS enforcement."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for providing policy rules for session management."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element that stores network function profiles and supports service discovery."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management during registration."
}

{
  "element1": "SMF",
  "element2": "UPF",
  "relationship": "SMF controls UPF for user plane data forwarding."
}

{
  "element1": "SMF",
  "element2": "PCF",
  "relationship": "SMF interacts with PCF to obtain policy rules."
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF may interact with NRF to discover other network functions."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 55)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy control for the network"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 56)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Handles user plane traffic"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy control for the network"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery"
}

## States

## Transitions

{
  "step": 1,
  "message": "PDU SESSION ESTABLISHMENT REQUEST",
  "from_element": "UE",
  "to_element": "network",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "UE attempts to establish a PDU session",
  "condition": "UE needs to access network services",
  "timing": "Initial step of PDU session establishment"
}

{
  "step": 2,
  "message": "PDU SESSION ESTABLISHMENT REJECT",
  "from_element": "network",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "Network rejects PDU session establishment",
  "condition": "Insufficient resources, missing DNN, etc.",
  "timing": "After network processes PDU SESSION ESTABLISHMENT REQUEST"
}

{
  "step": 3,
  "message": "PDU SESSION MODIFICATION REQUEST",
  "from_element": "UE",
  "to_element": "SMF",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "UE attempts to modify a PDU session",
  "condition": "UE needs to change PDU session parameters",
  "timing": "UE initiated modification"
}

{
  "step": 4,
  "message": "PDU SESSION MODIFICATION REJECT",
  "from_element": "SMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "SMF rejects PDU session modification",
  "condition": "Requested service option not subscribed, etc.",
  "timing": "After SMF processes PDU SESSION MODIFICATION REQUEST"
}

{
  "step": 5,
  "message": "PDU SESSION MODIFICATION COMMAND",
  "from_element": "SMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "SMF commands PDU session modification",
  "condition": "SMF determines modification is needed",
  "timing": "SMF initiated modification"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE registers with the AMF for access and mobility management"
}

{
  "element1": "UE",
  "element2": "SMF",
  "relationship": "UE establishes PDU sessions with the SMF"
}

{
  "element1": "SMF",
  "element2": "UPF",
  "relationship": "SMF controls the UPF for user plane traffic forwarding"
}

{
  "element1": "SMF",
  "element2": "PCF",
  "relationship": "SMF interacts with PCF for policy control"
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF discovers SMF via NRF"
}

## Triggers

{
  "state": "N/A",
  "trigger": "UE attempts to establish a PDU session"
}

{
  "state": "N/A",
  "trigger": "Network rejects PDU session establishment"
}

{
  "state": "N/A",
  "trigger": "UE attempts to modify a PDU session"
}

{
  "state": "N/A",
  "trigger": "SMF rejects PDU session modification"
}

{
  "state": "N/A",
  "trigger": "SMF commands PDU session modification"
}

## Conditions

{
  "state": "N/A",
  "condition": "UE needs to access network services"
}

{
  "state": "N/A",
  "condition": "Insufficient resources, missing DNN, etc."
}

{
  "state": "N/A",
  "condition": "UE needs to change PDU session parameters"
}

{
  "state": "N/A",
  "condition": "Requested service option not subscribed, etc."
}

{
  "state": "N/A",
  "condition": "SMF determines modification is needed"
}

## Timing

{
  "state": "N/A",
  "timing": "Initial step of PDU session establishment"
}

{
  "state": "N/A",
  "timing": "After network processes PDU SESSION ESTABLISHMENT REQUEST"
}

{
  "state": "N/A",
  "timing": "UE initiated modification"
}

{
  "state": "N/A",
  "timing": "After SMF processes PDU SESSION MODIFICATION REQUEST"
}

{
  "state": "N/A",
  "timing": "SMF initiated modification"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 57)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, authentication, and mobility management."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including PDU session establishment and modification."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Part of the 5G core network that handles user plane traffic."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy rules for session management."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery in 5G network."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access.",
  "condition": "UE must be in coverage area.",
  "timing": "Initial step of registration."
}

{
  "step": 2,
  "message": "REGISTRATION ACCEPT",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Successful registration procedure.",
  "condition": "Successful authentication and authorization.",
  "timing": "After successful registration procedure."
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF and receives responses."
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management during registration."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access."
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Successful registration procedure."
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area."
}

{
  "state": "5GMM-REGISTERED",
  "condition": "Successful authentication and authorization."
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration."
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After successful registration procedure."
}

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

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 61)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, reachability management, mobility management, authentication and authorization."
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management, including session establishment, modification and release."
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Part of the 5G core network architecture. The UPF is responsible for packet routing and forwarding, policy enforcement, and QoS handling."
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Provides policy rules to the SMF."
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Service discovery function."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
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
  "name": "SMF",
  "type": "Network Element",
  "description": "Session Management Function - responsible for session management, including PDU session establishment, modification, and release"
}

## States

{
  "name": "PROCEDURE TRANSACTION INACTIVE",
  "type": "INTERMEDIATE",
  "description": "State of the UE after a PDU session modification procedure is rejected"
}

## Transitions

{
  "step": 1,
  "message": "PDU SESSION MODIFICATION REQUEST",
  "from_element": "UE",
  "to_element": "SMF",
  "from_state": "PROCEDURE TRANSACTION INACTIVE",
  "to_state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "UE initiates PDU session modification",
  "condition": "UE wants to modify an existing PDU session",
  "timing": "UE-initiated procedure"
}

{
  "step": 2,
  "message": "PDU SESSION MODIFICATION REJECT",
  "from_element": "SMF",
  "to_element": "UE",
  "from_state": "PROCEDURE TRANSACTION INACTIVE",
  "to_state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "SMF rejects PDU session modification request",
  "condition": "SMF determines the request is not acceptable based on operator policy, subscription information, or other factors",
  "timing": "After SMF receives PDU SESSION MODIFICATION REQUEST"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "SMF",
  "relationship": "UE sends PDU SESSION MODIFICATION REQUEST to SMF, and SMF sends PDU SESSION MODIFICATION REJECT to UE"
}

## Triggers

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "UE initiates PDU session modification or SMF rejects PDU session modification request"
}

## Conditions

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "condition": "UE wants to modify an existing PDU session or SMF determines the request is not acceptable"
}

## Timing

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "timing": "UE-initiated procedure or after SMF receives PDU SESSION MODIFICATION REQUEST"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 66)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Manages access and mobility for the UE"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Manages PDU sessions"
}

## States

## Transitions

{
  "step": 1,
  "message": "PDU SESSION MODIFICATION REQUEST",
  "from_element": "UE",
  "to_element": "SMF",
  "from_state": "PROCEDURE TRANSACTION INACTIVE",
  "to_state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "UE initiates UE-requested PDU session modification procedure to modify the PDU session transferred from EPS to an MA PDU session",
  "condition": "UE sends the PDU SESSION MODIFICATION REQUEST message with the Request type IE set to 'MA PDU request'",
  "timing": "UE-requested PDU session modification procedure"
}

{
  "step": 2,
  "message": "PDU SESSION MODIFICATION REJECT",
  "from_element": "SMF",
  "to_element": "UE",
  "from_state": "N/A",
  "to_state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "SMF determines, based on operator policy and subscription information, that the PDU SESSION MODIFICATION REQUEST message is to be rejected",
  "condition": "SMF rejects the PDU SESSION MODIFICATION REQUEST message",
  "timing": "After SMF receives PDU SESSION MODIFICATION REQUEST"
}

{
  "step": 3,
  "message": "REGISTRATION REQUEST",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "N/A",
  "to_state": "N/A",
  "trigger": "Upon receipt of a PDU SESSION MODIFICATION REJECT message with 5GSM cause value #31 'request rejected, unspecified', if the UE had initiated deletion of one or more non-default QoS rules for the PDU session",
  "condition": "In order to synchronize the PDU session context with the AMF",
  "timing": "After PDU SESSION MODIFICATION REJECT message"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF"
}

{
  "element1": "UE",
  "element2": "SMF",
  "relationship": "UE sends PDU session modification requests to SMF"
}

{
  "element1": "SMF",
  "element2": "UE",
  "relationship": "SMF sends PDU session modification reject messages to UE"
}

## Triggers

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "UE initiates UE-requested PDU session modification procedure to modify the PDU session transferred from EPS to an MA PDU session"
}

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "trigger": "SMF determines, based on operator policy and subscription information, that the PDU SESSION MODIFICATION REQUEST message is to be rejected"
}

{
  "state": "N/A",
  "trigger": "Upon receipt of a PDU SESSION MODIFICATION REJECT message with 5GSM cause value #31 'request rejected, unspecified', if the UE had initiated deletion of one or more non-default QoS rules for the PDU session"
}

## Conditions

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "condition": "UE sends the PDU SESSION MODIFICATION REQUEST message with the Request type IE set to 'MA PDU request'"
}

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "condition": "SMF rejects the PDU SESSION MODIFICATION REQUEST message"
}

{
  "state": "N/A",
  "condition": "In order to synchronize the PDU session context with the AMF"
}

## Timing

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "timing": "UE-requested PDU session modification procedure"
}

{
  "state": "PROCEDURE TRANSACTION INACTIVE",
  "timing": "After SMF receives PDU SESSION MODIFICATION REQUEST"
}

{
  "state": "N/A",
  "timing": "After PDU SESSION MODIFICATION REJECT message"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 67)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment"
}

## States

## Transitions

## Network Element Relationships

## Triggers

## Conditions

## Timing

# Extracted Data from processed_data\semantic_chunks.md (Chunk 68)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management"
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
  "type": "INTERMEDIATE",
  "description": "UE is registered with the network"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 69)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, authentication, and mobility management"
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
  "type": "INTERMEDIATE",
  "description": "UE is registered with the network"
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "UE attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 70)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device used by the subscriber to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, mobility management, and access authentication/authorization."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 74)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, authentication, and mobility management"
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 77)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, authentication, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network function responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network function responsible for user plane traffic forwarding"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network function responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network function responsible for service discovery"
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF"
}

{
  "element1": "AMF",
  "element2": "UE",
  "relationship": "AMF sends authentication requests to UE"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 80)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to the AMF, and the AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 81)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to register with the 5G network."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered and has no 5GMM context."
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
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration, connection management, mobility management, and access authentication/authorization."
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
  "name": "5GMM-REGISTERED",
  "type": "FINAL",
  "description": "UE is successfully registered with the network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF, and AMF authenticates the UE."
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 119)

## Network Elements

{
  "name": "UE",
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network"
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network element responsible for registration, connection management, and mobility management"
}

{
  "name": "SMF",
  "type": "Session Management Function",
  "description": "Network element responsible for session management"
}

{
  "name": "UPF",
  "type": "User Plane Function",
  "description": "Network element responsible for user plane traffic handling"
}

{
  "name": "PCF",
  "type": "Policy Control Function",
  "description": "Network element responsible for policy control"
}

{
  "name": "NRF",
  "type": "Network Repository Function",
  "description": "Network element that stores network function profiles and supports service discovery"
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

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

{
  "step": 2,
  "message": "Authentication Request",
  "from_element": "AMF",
  "to_element": "UE",
  "from_state": "5GMM-REGISTERING",
  "to_state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication",
  "condition": "UE identity verification required",
  "timing": "After UE sends Registration Request"
}

## Network Element Relationships

{
  "element1": "UE",
  "element2": "AMF",
  "relationship": "UE sends registration requests to AMF and receives responses"
}

{
  "element1": "AMF",
  "element2": "SMF",
  "relationship": "AMF interacts with SMF for session management during registration"
}

{
  "element1": "AMF",
  "element2": "UPF",
  "relationship": "AMF interacts with UPF for user plane setup during registration"
}

{
  "element1": "AMF",
  "element2": "PCF",
  "relationship": "AMF interacts with PCF for policy control during registration"
}

{
  "element1": "AMF",
  "element2": "NRF",
  "relationship": "AMF discovers other network functions via NRF"
}

## Triggers

{
  "state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access"
}

{
  "state": "5GMM-REGISTERED",
  "trigger": "Network initiates authentication"
}

## Conditions

{
  "state": "5GMM-REGISTERING",
  "condition": "UE must be in coverage area"
}

{
  "state": "5GMM-REGISTERED",
  "condition": "UE identity verification required"
}

## Timing

{
  "state": "5GMM-REGISTERING",
  "timing": "Initial step of registration"
}

{
  "state": "5GMM-REGISTERED",
  "timing": "After UE sends Registration Request"
}

# Extracted Data from processed_data\semantic_chunks.md (Chunk 121)

## Network Elements

{
  "name": "UE",
  "type": "Network Element",
  "description": "User Equipment - mobile device attempting to access the network"
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
  "description": "Policy Control Function - provides policy rules for session management and mobility management"
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
  "name": "5GMM-CONNECTED",
  "type": "INTERMEDIATE",
  "description": "UE is connected to the network"
}

{
  "name": "5GMM-DEREGISTERED",
  "type": "INTERMEDIATE",
  "description": "UE is deregistered from the network"
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
  "type": "User Equipment",
  "description": "Mobile device attempting to access the 5G network."
}

{
  "name": "AMF",
  "type": "Access and Mobility Management Function",
  "description": "Network function responsible for registration management, connection management, and mobility management."
}

## States

{
  "name": "5GMM-NULL",
  "type": "INITIAL",
  "description": "UE is not registered in the 5G network."
}

## Transitions

{
  "step": 1,
  "message": "Registration Request",
  "from_element": "UE",
  "to_element": "AMF",
  "from_state": "5GMM-NULL",
  "to_state": "5GMM-REGISTERING",
  "trigger": "User turns on device and attempts network access",
  "condition": "UE must be in coverage area",
  "timing": "Initial step of registration"
}

## Network Element Relationships

## Triggers

{
  "state": "5GMM-NULL",
  "trigger": "User turns on device and attempts network access"
}

## Conditions

{
  "state": "5GMM-NULL",
  "condition": "UE must be in coverage area"
}

## Timing

{
  "state": "5GMM-NULL",
  "timing": "Initial step of registration"
}

