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

