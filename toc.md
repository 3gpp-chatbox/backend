4 general 51
4.1 overview 51
4.2 coordination between the protocols for 5GS mobility management and 5GS session management 51
4.2A controlling of UE access technology utilization by 5GS 52
4.3 UE domain selection 52
4.3.1 UE's usage setting 52
4.3.2 domain selection for UE originating sessions / calls 53
4.3.3 change of UE's usage setting 54
4.3.4 change or determination of IMS voice availability 55
4.4 NAS security 56
4.4.1 general 56
4.4.2 handling of 5G NAS security contexts 56
4.4.2.1 general 56
4.4.2.1.1 establishment of 5G NAS security context 56
4.4.2.1.2 UE leaving state 5GMM-DEREGISTERED 59
4.4.2.1.3 UE entering state 5GMM-DEREGISTERED 59
4.4.2.2 establishment of a mapped 5G NAS security context during inter-system change from S1 mode to N1 mode in 5GMM-CONNECTED mode 59
4.4.2.3 establishment of a 5G NAS security context during N1 mode to N1 mode handover 60
4.4.2.4 establishment of an EPS security context during inter-system change from N1 mode to S1 mode in 5GMM-CONNECTED mode 61
4.4.2.5 establishment of secure exchange of NAS messages 62
4.4.2.6 change of security keys 64
4.4.3 handling of NAS COUNT and NAS sequence number 64
4.4.3.1 general 64
4.4.3.2 replay protection 65
4.4.3.3 integrity protection and verification 65
4.4.3.4 ciphering and deciphering 66
4.4.3.5 NAS COUNT wrap around 66
4.4.4 integrity protection of NAS signalling messages 67
4.4.4.1 general 67
4.4.4.2 integrity checking of NAS signalling messages in the UE 67
4.4.4.3 integrity checking of NAS signalling messages in the AMF 68
4.4.5 ciphering of NAS signalling messages 70
4.4.6 protection of initial NAS signalling messages 70
4.4.7 protection of NAS IEs 72
4.5 unified access control 73
4.5.1 general 73
4.5.2 determination of the access identities and access category associated with a request for access for UEs not operating in SNPN access operation mode over 3GPP access 75
4.5.2A determination of the access identities and access category associated with a request for access for UEs operating in SNPN access operation mode over 3GPP access 81
4.5.3 Operator-defined access categories 87
4.5.4 access control and checking 89
4.5.4.1 access control and checking in 5GMM-IDLE mode and in 5GMM-IDLE mode with suspend indication 89
4.5.4.2 access control and checking in 5GMM-CONNECTED mode and in 5GMM-CONNECTED mode with RRC inactive indication 91
4.5.5 exception handling and avoiding double barring 93
4.5.6 mapping between access categories/access identities and RRC establishment cause 98
4.6 network slicing 99
4.6.1 general 99
4.6.2 mobility management aspects 102
4.6.2.1 general 102
4.6.2.2 NSSAI storage 103
4.6.2.3 provision of NSSAI to lower layers in 5GMM-IDLE mode 111
4.6.2.4 network slice-specific authentication and authorization 112
4.6.2.5 mobility management based network slice admission control 114
4.6.2.6 provision of NSAG information to lower layers 115
4.6.2.7 mobility management based network slice replacement 116
4.6.2.8 mobility management for optimised handling of temporarily available network slices 118
4.6.2.9 mobility management based network slice usage control 119
4.6.2.10 mobility management aspects of handling network slices with NS-AoS not matching deployed tracking areas 120
4.6.2.11 mobility management for partial network slice 121
4.6.3 session management aspects 122
4.6.3.0 general 122
4.6.3.1 session management based network slice admission control 122
4.6.3.2 support of network slice admission control and interworking with EPC 123
4.6.3.3 session management based network slice data rate limitation control 123
4.6.3.4 session management based network slice replacement 123
4.6.3.5 session management for optimized handling of temporarily available network slices 124
4.6.3.6 session management for partial network slice 125
4.6.3.7 session management aspect of handling network slices with NS-AoS not matching deployed tracking areas 126
4.7 NAS over non-3GPP access 126
4.7.1 general 126
4.7.2 5GS mobility management aspects 127
4.7.2.1 general 127
4.7.2.2 establishment cause for non-3GPP access 128
4.7.3 5GS session management aspects 129
4.7.4 limited service state over non-3GPP access 129
4.7.5 NAS signalling using trusted WLAN access network 130
4.8 interworking with E-UTRAN connected to EPC 130
4.8.1 general 130
4.8.2 Single-registration mode 131
4.8.2.1 general 131
4.8.2.2 Single-registration mode with N26 interface 131
4.8.2.3 Single-registration mode without N26 interface 131
4.8.2.3.1 interworking between NG-RAN and E-UTRAN 131
4.8.2.3.2 interworking between TNGF or N3IWF connected to 5GCN and E-UTRAN 133
4.8.3 Dual-registration mode 134
4.8.4 core network selection for UEs not using CIoT 5GS optimizations 135
4.8.4A core network selection and redirection for UEs using CIoT optimizations 135
4.8.4A.1 core network selection 135
4.8.4A.2 redirection of the UE by the core network 136
4.9 disabling and re-enabling of UE's N1 mode capability 136
4.9.1 general 136
4.9.2 disabling and re-enabling of UE's N1 mode capability for 3GPP access 136
4.9.3 disabling and re-enabling of UE's N1 mode capability for non-3GPP access 140
4.9.4 disabling and re-enabling of UE's satellite NG-RAN capability 141
4.10 interworking with ePDG connected to EPC 141
4.11 UE configuration parameter updates 141
4.12 access traffic steering switching and splitting (ATSSS) 142
4.13 support of NAS signalling using wireline access network 142
4.14 Non-public network (NPN) 144
4.14.1 general 144
4.14.2 Stand-alone non-public network (SNPN) 144
4.14.3 public network integrated non-public network (PNI-NPN) 146
4.15 time synchronization and time sensitive communication 148
4.15.1 general 148
4.15.2 void 148
4.15.2.1 void 148
4.15.2.2 void 148
4.15.2.3 void 148
4.15.3 time synchronization 148
4.15.4 user plane node management 148
4.16 UE radio capability signalling optimisation 149
4.17 5GS mobility management in NB-N1 mode 150
4.18 5GS session management in NB-N1 mode 150
4.19 5GS mobility management in WB-N1 mode for IoT 150
4.20 5GS session management in WB-N1 mode for IoT 151
4.21 authentication and key management for applications (AKMA) 151
4.22 uncrewed aerial vehicle identification authentication and authorization 152
4.22.1 general 152
4.22.2 authentication and authorization of UAV 152
4.22.3 authorization of C2 communication 153
4.22.4 void 154
4.22.5 support of no-transmit zone 154
4.23 NAS over Non-Terrestrial network 154
4.23.1 general 154
4.23.2 list of "PLMNs not allowed to operate at the present UE location" 154
4.23.3 5GS mobility management via a satellite NG-RAN cell 155
4.23.4 5GS session management via a satellite NG-RAN cell 156
4.23.5 handling multiple tracking area codes from the lower layers 156
4.24 minimization of service interruption 157
4.25 support of MUSIM features 158
4.26 support for personal IoT network service 159
4.27 mobile base station relay support 160
4.28 NAS-specific aspects of mobile gNB with wireless access backhauling (MWAB) 160
4.28.1 general 160
4.28.2 authorization of MWAB-UE 160
4.28.3 control of UE access via MWAB 161
4.29 support of indirect network sharing 161
5 elementary procedures for 5GS mobility management 161
5.1 overview 161
5.1.1 general 161
5.1.2 types of 5GMM procedures 162
5.1.3 5GMM sublayer states 163
5.1.3.1 general 163
5.1.3.2 5GMM sublayer states 163
5.1.3.2.1 5GMM sublayer states in the UE 163
5.1.3.2.1.1 general 163
5.1.3.2.1.2 main states 164
5.1.3.2.1.2.1 5GMM-NULL 164
5.1.3.2.1.2.2 5GMM-DEREGISTERED 164
5.1.3.2.1.2.3 5GMM-REGISTERED-INITIATED 164
5.1.3.2.1.2.4 5GMM-REGISTERED 164
5.1.3.2.1.2.5 5GMM-DEREGISTERED-INITIATED 164
5.1.3.2.1.2.6 5GMM-SERVICE-REQUEST-INITIATED 164
5.1.3.2.1.3 substates of state 5GMM-DEREGISTERED 165
5.1.3.2.1.3.1 general 165
5.1.3.2.1.3.2 5GMM-DEREGISTERED.NORMAL-SERVICE 165
5.1.3.2.1.3.3 5GMM-DEREGISTERED.LIMITED-SERVICE 165
5.1.3.2.1.3.4 5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION 165
5.1.3.2.1.3.5 5GMM-DEREGISTERED.PLMN-SEARCH 165
5.1.3.2.1.3.6 5GMM-DEREGISTERED.NO-SUPI 165
5.1.3.2.1.3.7 5GMM-DEREGISTERED.NO-CELL-AVAILABLE 165
5.1.3.2.1.3.8 5GMM-DEREGISTERED.eCALL-INACTIVE 166
5.1.3.2.1.3.9 5GMM-DEREGISTERED.INITIAL-REGISTRATION-NEEDED 166
5.1.3.2.1.4 substates of state 5GMM-REGISTERED 166
5.1.3.2.1.4.1 general 166
5.1.3.2.1.4.2 5GMM-REGISTERED.NORMAL-SERVICE 166
5.1.3.2.1.4.3 5GMM-REGISTERED.NON-ALLOWED-SERVICE 166
5.1.3.2.1.4.4 5GMM-REGISTERED.ATTEMPTING-REGISTRATION-UPDATE 166
5.1.3.2.1.4.5 5GMM-REGISTERED.LIMITED-SERVICE 167
5.1.3.2.1.4.6 5GMM-REGISTERED.PLMN-SEARCH 167
5.1.3.2.1.4.7 5GMM-REGISTERED.NO-CELL-AVAILABLE 167
5.1.3.2.1.4.8 5GMM-REGISTERED.UPDATE-NEEDED 167
5.1.3.2.2 5GS update status in the UE 168
5.1.3.2.3 5GMM sublayer states in the network side 168
5.1.3.2.3.1 general 168
5.1.3.2.3.2 5GMM-DEREGISTERED 169
5.1.3.2.3.3 5GMM-COMMON-PROCEDURE-INITIATED 169
5.1.3.2.3.4 5GMM-REGISTERED 169
5.1.3.2.3.5 5GMM-DEREGISTERED-INITIATED 169
5.1.4 coordination between 5GMM and EMM 169
5.1.4.1 general 169
5.1.4.2 coordination between 5GMM for 3GPP access and EMM with N26 interface 170
5.1.4.3 coordination between 5GMM for 3GPP access and EMM without N26 interface 170
5.1.5 coordination between 5GMM and GMM 171
5.2 behaviour of the UE in state 5GMM-DEREGISTERED and state 5GMM-REGISTERED 171
5.2.1 general 171
5.2.2 UE behaviour in state 5GMM-DEREGISTERED 171
5.2.2.1 general 171
5.2.2.2 primary substate selection 171
5.2.2.2.1 selection of the substate after power on 171
5.2.2.3 detailed description of UE behaviour in state 5GMM-DEREGISTERED 172
5.2.2.3.1 NORMAL-SERVICE 172
5.2.2.3.2 LIMITED-SERVICE 172
5.2.2.3.3 ATTEMPTING-REGISTRATION 172
5.2.2.3.4 PLMN-SEARCH 174
5.2.2.3.5 NO-SUPI 174
5.2.2.3.6 NO-CELL-AVAILABLE 174
5.2.2.3.7 eCALL-INACTIVE 174
5.2.2.3.8 INITIAL-REGISTRATION-NEEDED 175
5.2.2.4 substate when back to state 5GMM-DEREGISTERED from another 5GMM state 175
5.2.3 UE behaviour in state 5GMM-REGISTERED 175
5.2.3.1 general 175
5.2.3.2 detailed description of UE behaviour in state 5GMM-REGISTERED 175
5.2.3.2.1 NORMAL-SERVICE 175
5.2.3.2.2 NON-ALLOWED-SERVICE 176
5.2.3.2.3 ATTEMPTING-REGISTRATION-UPDATE 176
5.2.3.2.4 LIMITED-SERVICE 178
5.2.3.2.5 PLMN-SEARCH 178
5.2.3.2.6 NO-CELL-AVAILABLE 178
5.2.3.2.7 UPDATE-NEEDED 178
5.3 general on elementary 5GMM procedures 179
5.3.1 5GMM modes and N1 NAS signalling connection 179
5.3.1.1 establishment of the N1 NAS signalling connection 179
5.3.1.2 Re-establishment of the N1 NAS signalling connection 180
5.3.1.3 release of the N1 NAS signalling connection 182
5.3.1.4 5GMM-CONNECTED mode with RRC inactive indication 186
5.3.1.5 suspend and resume of the N1 NAS signalling connection 190
5.3.2 permanent identifiers 191
5.3.3 temporary identities 194
5.3.4 registration areas 195
5.3.5 service area restrictions 196
5.3.5.1 general 196
5.3.5.2 3GPP access service area restrictions 196
5.3.5.3 wireline access service area restrictions 201
5.3.6 mobile initiated connection only mode 202
5.3.7 handling of the periodic registration update timer and mobile reachable timer 204
5.3.8 handling of timer T3502 206
5.3.9 handling of NAS level mobility management congestion control 206
5.3.10 handling of DNN based congestion control 208
5.3.11 handling of S-NSSAI based congestion control 208
5.3.12 handling of local emergency numbers 208
5.3.12A handling of local emergency numbers received via 3GPP access and non-3GPP access 209
5.3.12A.1 general 209
5.3.12A.2 receiving a REGISTRATION ACCEPT message via non-3GPP access 210
5.3.13 lists of 5GS forbidden tracking areas 210
5.3.13A forbidden PLMN lists 212
5.3.14 list of equivalent PLMNs 212
5.3.14A list of equivalent SNPNs 212
5.3.15 transmission failure abnormal case in the UE 213
5.3.16 extended DRX cycle for UEs in 5GMM-IDLE and 5GMM-CONNECTED mode with RRC inactive indication 213
5.3.17 service gap control 214
5.3.18 restriction on use of enhanced coverage 216
5.3.19 handling of congestion control for transport of user data via the control plane 217
5.3.19A specific requirements for UE configured to use timer T3245 217
5.3.19A.1 UE not operating in SNPN access operation mode 217
5.3.19A.2 UE operating in SNPN access operation mode 218
5.3.20 specific requirements for UE when receiving non-integrity protected reject messages 219
5.3.20.1 general 219
5.3.20.2 requirements for UE in a PLMN 219
5.3.20.3 requirements for UE in an SNPN 224
5.3.21 CIoT 5GS optimizations 228
5.3.22 interaction between MICO mode with active time and extended idle mode DRX cycle 230
5.3.23 forbidden wireline access area 231
5.3.24 WUS assistance 231
5.3.25 paging early indication with paging subgrouping assistance 232
5.3.26 support for unavailability period 233
5.4 5GMM common procedures 235
5.4.1 primary authentication and key agreement procedure 235
5.4.1.1 general 235
5.4.1.2 EAP based primary authentication and key agreement procedure 235
5.4.1.2.1 general 235
5.4.1.2.2 EAP-AKA' related procedures 238
5.4.1.2.3 EAP-TLS related procedures 245
5.4.1.2.3A procedures related to EAP methods other than EAP-AKA' and EAP-TLS 249
5.4.1.2.3B procedures related to EAP methods used for primary authentication of an N5GC device 253
5.4.1.2.3C procedures related to EAP methods used for primary authentication of an AUN3 device 255
5.4.1.2.4 EAP message reliable transport procedure 256
5.4.1.2.4.3 EAP message reliable transport procedure accepted by the UE 257
5.4.1.2.4.4 abnormal cases on the network side 257
5.4.1.2.4.5 abnormal cases in the UE 257
5.4.1.2.5 EAP result message transport procedure 259
5.4.1.3 5G AKA based primary authentication and key agreement procedure 261
5.4.1.3.1 general 261
5.4.1.3.2 authentication initiation by the network 261
5.4.1.3.3 authentication response by the UE 262
5.4.1.3.4 authentication completion by the network 263
5.4.1.3.5 authentication not accepted by the network 263
5.4.1.3.6 authentication not accepted by the UE 266
5.4.1.3.7 abnormal cases 266
5.4.2 security mode control procedure 271
5.4.2.1 general 271
5.4.2.2 NAS security mode control initiation by the network 271
5.4.2.3 NAS security mode command accepted by the UE 275
5.4.2.4 NAS security mode control completion by the network 277
5.4.2.5 NAS security mode command not accepted by the UE 278
5.4.2.6 abnormal cases in the UE 278
5.4.2.7 abnormal cases on the network side 279
5.4.3 identification procedure 279
5.4.3.1 general 279
5.4.3.2 identification initiation by the network 280
5.4.3.3 identification response by the UE 280
5.4.3.4 identification completion by the network 280
5.4.3.5 abnormal cases in the UE 280
5.4.3.6 abnormal cases on the network side 280
5.4.4 generic UE configuration update procedure 281
5.4.4.1 general 281
5.4.4.2 generic UE configuration update procedure initiated by the network 285
5.4.4.3 generic UE configuration update accepted by the UE 292
5.4.4.4 generic UE configuration update completion by the network 300
5.4.4.5 abnormal cases in the UE 301
5.4.4.6 abnormal cases on the network side 302
5.4.5 NAS transport procedure(s) 304
5.4.5.1 general 304
5.4.5.2 UE-initiated NAS transport procedure 304
5.4.5.2.1 general 304
5.4.5.2.2 UE-initiated NAS transport procedure initiation 305
5.4.5.2.3 UE-initiated NAS transport of messages accepted by the network 308
5.4.5.2.4 UE-initiated NAS transport of messages not accepted by the network 313
5.4.5.2.5 abnormal cases on the network side 316
5.4.5.2.6 abnormal cases in the UE 321
5.4.5.3 Network-initiated NAS transport procedure 323
5.4.5.3.1 general 323
5.4.5.3.2 Network-initiated NAS transport procedure initiation 324
5.4.5.3.3 Network-initiated NAS transport of messages accepted by the UE 329
5.4.6 5GMM status procedure 335
5.4.6.1 general 335
5.4.6.2 5GMM status received in the UE 335
5.4.6.3 5GMM status received in the network 335
5.4.7 network slice-specific authentication and authorization procedure 336
5.4.7.1 general 336
5.4.7.2 network slice-specific EAP message reliable transport procedure 337
5.4.7.2.1 network slice-specific EAP message reliable transport procedure initiation 337
5.4.7.2.2 network slice-specific EAP message reliable transport procedure accepted by the UE 338
5.4.7.2.3 abnormal cases on the network side 338
5.4.7.2.4 abnormal cases in the UE 339
5.4.7.3 network slice-specific EAP result message transport procedure 340
5.4.7.3.1 network slice-specific EAP result message transport procedure initiation 340
5.5 5GMM specific procedures 341
5.5.1 registration procedure 341
5.5.1.1 general 341
5.5.1.2 registration procedure for initial registration 342
5.5.1.2.1 general 342
5.5.1.2.2 initial registration initiation 342
5.5.1.2.3 5GMM common procedure initiation 353
5.5.1.2.4 initial registration accepted by the network 353
5.5.1.2.5 initial registration not accepted by the network 381
5.5.1.2.6 initial registration for emergency services not accepted by the network 398
5.5.1.2.6A initial registration for initiating an emergency PDU session not accepted by the network 399
5.5.1.2.7 abnormal cases in the UE 400
5.5.1.2.8 abnormal cases on the network side 403
5.5.1.3 registration procedure for mobility and periodic registration update 405
5.5.1.3.1 general 405
5.5.1.3.2 mobility and periodic registration update initiation 405
5.5.1.3.3 5GMM common procedure initiation 422
5.5.1.3.4 mobility and periodic registration update accepted by the network 423
5.5.1.3.5 mobility and periodic registration update not accepted by the network 459
5.5.1.3.6 mobility and periodic registration update for initiating an emergency PDU session not accepted by the network 478
5.5.1.3.6A mobility and periodic registration update for an emergency services fallback not accepted by the network 478
5.5.1.3.7 abnormal cases in the UE 479
5.5.1.3.8 abnormal cases on the network side 483
5.5.2 De-registration procedure 486
5.5.2.1 general 486
5.5.2.2 UE-initiated de-registration procedure 488
5.5.2.2.1 UE-initiated de-registration procedure initiation 488
5.5.2.2.2 UE-initiated de-registration procedure completion 490
5.5.2.2.3 UE-initiated de-registration procedure completion for 5GS services over 3GPP access 490
5.5.2.2.4 UE-initiated de-registration procedure completion for 5GS services over non-3GPP access 491
5.5.2.2.5 UE-initiated de-registration procedure completion for 5GS services over both 3GPP access and non-3GPP access 491
5.5.2.2.6 abnormal cases in the UE 491
5.5.2.2.7 abnormal cases in the network side 493
5.5.2.3 Network-initiated de-registration procedure 494
5.5.2.3.1 Network-initiated de-registration procedure initiation 494
5.5.2.3.2 Network-initiated de-registration procedure completion by the UE 496
5.5.2.3.3 Network-initiated de-registration procedure completion by the network 509
5.5.2.3.4 abnormal cases in the UE 510
5.5.2.3.5 abnormal cases in the network side 510
5.5.3 ecall inactivity procedure 511
5.5.4 authentication and key agreement procedure for 5G ProSe UE-to-network relay and 5G ProSe UE-to-UE relay 512
5.5.4.1 general 512
5.5.4.2 ProSe relay transaction identity (PRTI) 513
5.5.4.3 UE-initiated authentication and key agreement procedure initiation 514
5.5.4.4 UE-initiated authentication and key agreement procedure accepted by the network 514
5.5.4.5 UE-initiated authentication and key agreement procedure not accepted by the network 515
5.5.4.6 abnormal cases in the UE 515
5.5.4.7 abnormal cases on the network side 516
5.6 5GMM connection management procedures 516
5.6.1 service request procedure 516
5.6.1.1 general 516
5.6.1.2 service request procedure initiation 521
5.6.1.2.1 UE is not using 5GS services with control plane CIoT 5GS optimization 521
5.6.1.2.2 UE is using 5GS services with control plane CIoT 5GS optimization 524
5.6.1.3 common procedure initiation 527
5.6.1.4 service request procedure accepted by the network 527
5.6.1.4.1 UE is not using 5GS services with control plane CIoT 5GS optimization 527
5.6.1.4.2 UE is using 5GS services with control plane CIoT 5GS optimization 531
5.6.1.5 service request procedure not accepted by the network 536
5.6.1.6 service request procedure for initiating an emergency PDU session not accepted by the network 549
5.6.1.6A service request procedure for an emergency services fallback not accepted by the network 550
5.6.1.7 abnormal cases in the UE 550
5.6.1.8 abnormal cases on the network side 555
5.6.2 paging procedure 556
5.6.2.1 general 556
5.6.2.2 paging for 5GS services 557
5.6.2.2.1 general 557
5.6.2.2.2 abnormal cases on the network side 559
5.6.2.2.3 abnormal cases in the UE 559
5.6.3 notification procedure 560
5.6.3.1 general 560
5.6.3.2 notification procedure initiation 560
5.6.3.3 notification procedure completion 563
5.6.3.4 abnormal cases on the network side 564
5.6.3.5 abnormal cases on the UE side 564
6 elementary procedures for 5GS session management 564
6.1 overview 564
6.1.1 general 564
6.1.2 types of 5GSM procedures 565
6.1.3 5GSM sublayer states 566
6.1.3.1 general 566
6.1.3.2 5GSM sublayer states in the UE 566
6.1.3.2.1 overview 566
6.1.3.2.2 PDU SESSION INACTIVE 566
6.1.3.2.3 PDU SESSION ACTIVE PENDING 566
6.1.3.2.4 PDU SESSION ACTIVE 566
6.1.3.2.5 PDU SESSION INACTIVE PENDING 567
6.1.3.2.6 PDU SESSION MODIFICATION PENDING 567
6.1.3.2.7 PROCEDURE TRANSACTION INACTIVE 567
6.1.3.2.8 PROCEDURE TRANSACTION PENDING 567
6.1.3.3 5GSM sublayer states in the network side 567
6.1.3.3.1 overview 567
6.1.3.3.2 PDU SESSION INACTIVE 568
6.1.3.3.3 PDU SESSION ACTIVE 568
6.1.3.3.4 PDU SESSION INACTIVE PENDING 568
6.1.3.3.5 PDU SESSION MODIFICATION PENDING 568
6.1.3.3.6 PROCEDURE TRANSACTION INACTIVE 568
6.1.3.3.7 PROCEDURE TRANSACTION PENDING 568
6.1.4 coordination between 5GSM and ESM 569
6.1.4.1 coordination between 5GSM and ESM with N26 interface 569
6.1.4.2 coordination between 5GSM and ESM without N26 interface 583
6.1.4A coordination between 5GSM and SM 585
6.1.5 coordination for interworking with ePDG connected to EPC 585
6.2 general on elementary 5GSM procedures 586
6.2.1 principles of PTI handling for 5GSM procedures 586
6.2.2 PDU session types 588
6.2.3 PDU session management 588
6.2.4 IP address allocation 589
6.2.4.1 general 589
6.2.4.2 IP address allocation via NAS signalling 589
6.2.4.2a IPv6 prefix delegation via DHCPv6 590
6.2.4.3 additional RG related requirements for IP address allocation 590
6.2.4.4 additional requirements of the UE acting as 5G ProSe layer-3 UE-to-network relay UE for IP address allocation 591
6.2.5 quality of service 591
6.2.5.1 general 591
6.2.5.1.1 QoS rules 591
6.2.5.1.1.1 general 591
6.2.5.1.1.2 signalled QoS rules 591
6.2.5.1.1.3 derived QoS rules 593
6.2.5.1.1.4 QoS flow descriptions 593
6.2.5.1.2 Session-AMBR 594
6.2.5.1.2A void 594
6.2.5.1.3 UL user data packet matching 594
6.2.5.1.4 reflective QoS 595
6.2.5.1.4.1 general 595
6.2.5.1.4.2 derivation of packet filter for UL direction from DL user data packet 595
6.2.5.1.4.3 creating a derived QoS rule by reflective QoS in the UE 597
6.2.5.1.4.4 updating a derived QoS rule by reflective QoS in the UE 597
6.2.5.1.4.5 deleting a derived QoS rule in the UE 598
6.2.5.1.4.6 ignoring RQI in the UE 598
6.2.5.2 QoS in MA PDU session 598
6.2.6 local area data network (LADN) 598
6.2.7 handling of DNN based congestion control 600
6.2.8 handling of S-NSSAI based congestion control 601
6.2.9 interaction with upper layers 605
6.2.9.1 general 605
6.2.9.2 URSP 605
6.2.9.3 ProSeP 606
6.2.10 handling of 3GPP PS data off 606
6.2.11 Multi-homed IPv6 PDU session 607
6.2.12 handling of network rejection not due to congestion control 608
6.2.13 handling of small data rate control 610
6.2.14 handling of serving PLMN rate control 611
6.2.15 handling of reliable data service 611
6.2.16 handling of header compression for control plane CIoT optimizations 611
6.2.17 handling of edge computing enhancements 612
6.2.18 support of redundant PDU sessions 613
6.2.19 handling of maximum group data rate limitation control 613
6.2.20 support of UL PDU set handling 613
6.3 Network-requested 5GSM procedures 613
6.3.1 PDU session authentication and authorization procedure 613
6.3.1.1 general 613
6.3.1.2 PDU EAP message reliable transport procedure 615
6.3.1.2.1 PDU EAP message reliable transport procedure initiation 615
6.3.1.2.2 PDU EAP message reliable transport procedure accepted by the UE 617
6.3.1.2.3 abnormal cases on the network side 617
6.3.1.2.4 abnormal cases in the UE 618
6.3.1.3 PDU EAP result message transport procedure 618
6.3.1.3.1 PDU EAP result message transport procedure initiation 618
6.3.1.3.2 abnormal cases in the UE 618
6.3.1A Service-level authentication and authorization procedure 619
6.3.1A.1 general 619
6.3.1A.2 Service-level authentication and authorization procedure initiation 620
6.3.1A.3 Service-level authentication and authorization procedure accepted by the UE 622
6.3.1A.4 abnormal cases on the network side 622
6.3.1A.5 abnormal cases in the UE 622
6.3.2 Network-requested PDU session modification procedure 623
6.3.2.1 general 623
6.3.2.2 Network-requested PDU session modification procedure initiation 623
6.3.2.3 Network-requested PDU session modification procedure accepted by the UE 629
6.3.2.4 Network-requested PDU session modification procedure not accepted by the UE 639
6.3.2.5 abnormal cases on the network side 644
6.3.2.6 abnormal cases in the UE 646
6.3.3 Network-requested PDU session release procedure 646
6.3.3.1 general 646
6.3.3.2 Network-requested PDU session release procedure initiation 646
6.3.3.3 Network-requested PDU session release procedure accepted by the UE 649
6.3.3.4 N1 SM delivery skipped 666
6.3.3.5 abnormal cases on the network side 666
6.3.3.6 abnormal cases in the UE 666
6.4 UE-requested 5GSM procedures 667
6.4.1 UE-requested PDU session establishment procedure 667
6.4.1.1 general 667
6.4.1.2 UE-requested PDU session establishment procedure initiation 668
6.4.1.3 UE-requested PDU session establishment procedure accepted by the network 681
6.4.1.4 UE-requested PDU session establishment procedure not accepted by the network 696
6.4.1.4.1 general 696
6.4.1.4.2 handling of network rejection due to congestion control 700
6.4.1.4.3 handling of network rejection not due to congestion control 712
6.4.1.5 handling the maximum number of established PDU sessions 723
6.4.1.5A handling the maximum number of allowed active user-plane resources for PDU sessions of UEs in NB-N1 mode 724
6.4.1.6 abnormal cases in the UE 724
6.4.1.7 abnormal cases on the network side 727
6.4.2 UE-requested PDU session modification procedure 727
6.4.2.1 general 727
6.4.2.2 UE-requested PDU session modification procedure initiation 729
6.4.2.3 UE-requested PDU session modification procedure accepted by the network 736
6.4.2.4 UE-requested PDU session modification procedure not accepted by the network 736
6.4.2.4.1 general 736
6.4.2.4.2 handling of network rejection due to congestion control 737
6.4.2.4.3 handling of network rejection not due to congestion control 749
6.4.2.5 abnormal cases in the UE 754
6.4.2.6 abnormal cases on the network side 755
6.4.3 UE-requested PDU session release procedure 756
6.4.3.1 general 756
6.4.3.2 UE-requested PDU session release procedure initiation 757
6.4.3.3 UE-requested PDU session release procedure accepted by the network 758
6.4.3.4 UE-requested PDU session release procedure not accepted by the network 758
6.4.3.5 abnormal cases in the UE 758
6.4.3.6 abnormal cases on the network side 759
6.5 5GSM status procedure 760
6.5.1 general 760
6.5.2 5GSM status received in the UE 760
6.5.3 5GSM status received in the SMF 760
6.6 miscellaneous procedures 761
6.6.1 exchange of extended protocol configuration options 761
6.6.2 remote UE report procedure 761
6.6.2.1 general 761
6.6.2.2 remote UE report procedure initiation 761
6.6.2.3 remote UE report procedure accepted by the network 762
6.6.2.4 abnormal cases in the UE 762
6.6.2.5 abnormal cases on the network side 763
7 handling of unknown unforeseen and erroneous protocol data 763
7.1 general 763
7.2 message too short or too long 764
7.2.1 message too short 764
7.2.2 message too long 764
7.3 unknown or unforeseen procedure transaction identity or PDU session identity 764
7.3.1 procedure transaction identity 764
7.3.2 PDU session identity 765
7.4 unknown or unforeseen message type 766
7.5 Non-semantical mandatory information element errors 766
7.5.1 common procedures 766
7.5.2 5GS mobility management 767
7.5.3 5GS session management 767
7.6 unknown and unforeseen IEs in the non-imperative message part 767
7.6.1 IEIs unknown in the message 767
7.6.2 out of sequence IEs 767
7.6.3 repeated IEs 767
7.6.4 unknown and unforeseen IEs in a type 6 IE container information element 768
7.6.4.1 IEIs unknown in the type 6 IE container information element 768
7.6.4.2 out of sequence IEs 768
7.6.4.3 repeated IEs 768
7.7 Non-imperative message part errors 768
7.7.1 syntactically incorrect optional IEs 768
7.7.2 conditional IE errors 768
7.7.3 errors in a type 6 IE container information element 769
7.7.3.1 syntactically incorrect optional IEs 769
7.7.3.2 conditional IE errors 769
7.8 messages with semantically incorrect contents 769
8 message functional definitions and contents 770
8.1 overview 770
8.2 5GS mobility management messages 771
8.2.1 authentication request 771
8.2.1.1 message definition 771
8.2.1.2 authentication parameter RAND 771
8.2.1.3 authentication parameter AUTN 771
8.2.1.4 void 771
8.2.1.5 EAP message 771
8.2.2 authentication response 772
8.2.2.1 message definition 772
8.2.2.2 authentication response parameter 772
8.2.2.3 EAP message 772
8.2.3 authentication result 772
8.2.3.1 message definition 772
8.2.3.2 ABBA 773
8.2.3.3 AUN3 device security key 773
8.2.4 authentication failure 773
8.2.4.1 message definition 773
8.2.4.2 authentication failure parameter 774
8.2.5 authentication reject 774
8.2.5.1 message definition 774
8.2.5.2 EAP message 774
8.2.6 registration request 774
8.2.6.1 message definition 774
8.2.6.2 Non-current native NAS key set identifier 778
8.2.6.3 5GMM capability 778
8.2.6.4 UE security capability 778
8.2.6.5 requested NSSAI 778
8.2.6.6 last visited registered TAI 778
8.2.6.7 S1 UE network capability 778
8.2.6.8 uplink data status 779
8.2.6.9 PDU session status 779
8.2.6.10 MICO indication 779
8.2.6.11 UE status 779
8.2.6.12 additional GUTI 779
8.2.6.13 allowed PDU session status 779
8.2.6.14 UE's usage setting 779
8.2.6.15 requested DRX parameters 779
8.2.6.16 EPS NAS message container 779
8.2.6.17 LADN indication 780
8.2.6.17A payload container type 780
8.2.6.18 payload container 780
8.2.6.19 network slicing indication 780
8.2.6.20 5GS update type 780
8.2.6.21 NAS message container 780
8.2.6.22 requested extended DRX parameters 780
8.2.6.23 EPS bearer context status 781
8.2.6.24 T3324 value 781
8.2.6.25 mobile station classmark 2 781
8.2.6.26 supported codecs 781
8.2.6.27 UE radio capability ID 781
8.2.6.28 requested mapped NSSAI 781
8.2.6.29 additional information requested 781
8.2.6.30 requested WUS assistance information 781
8.2.6.31 void 781
8.2.6.32 N5GC indication 781
8.2.6.33 requested NB-N1 mode DRX parameters 781
8.2.6.34 UE request type 781
8.2.6.35 paging restriction 782
8.2.6.35 Service-level-AA container 782
8.2.6.36 NID 782
8.2.6.37 UE determined PLMN with disaster condition 782
8.2.6.38 requested PEIPS assistance information 782
8.2.6.39 requested T3512 value 782
8.2.6.40 unavailability information 782
8.2.6.41 Non-3GPP path switching information 782
8.2.6.42 AUN3 indication 782
8.2.7 registration accept 782
8.2.7.1 message definition 782
8.2.7.2 5G-GUTI 786
8.2.7.3 equivalent PLMNs 786
8.2.7.4 TAI list 786
8.2.7.5 allowed NSSAI 786
8.2.7.6 rejected NSSAI 786
8.2.7.7 configured NSSAI 786
8.2.7.8 5GS network feature support 786
8.2.7.9 PDU session status 787
8.2.7.10 PDU session reactivation result 787
8.2.7.11 PDU session reactivation result error cause 787
8.2.7.12 LADN information 787
8.2.7.13 MICO indication 787
8.2.7.14 network slicing indication 787
8.2.7.15 service area list 787
8.2.7.16 T3512 value 787
8.2.7.17 Non-3GPP de-registration timer value 787
8.2.7.18 T3502 value 787
8.2.7.19 emergency number list 788
8.2.7.20 extended emergency number list 788
8.2.7.21 SOR transparent container 788
8.2.7.22 EAP message 788
8.2.7.23 NSSAI inclusion mode 788
8.2.7.24 Operator-defined access category definitions 788
8.2.7.25 negotiated DRX parameters 788
8.2.7.26 Non-3GPP NW policies 788
8.2.7.27 negotiated extended DRX parameters 788
8.2.7.28 T3447 value 788
8.2.7.29 T3448 value 789
8.2.7.30 T3324 value 789
8.2.7.31 EPS bearer context status 789
8.2.7.32 UE radio capability ID 789
8.2.7.33 UE radio capability ID deletion indication 789
8.2.7.34 pending NSSAI 789
8.2.7.35 ciphering key data 789
8.2.7.36 CAG information list 789
8.2.7.37 truncated 5G-S-TMSI configuration 789
8.2.7.38 negotiated NB-N1 mode DRX parameters 790
8.2.7.39 negotiated WUS assistance information 790
8.2.7.40 extended rejected NSSAI 790
8.2.7.41 Service-level-AA container 790
8.2.7.42 negotiated PEIPS assistance information 790
8.2.7.43 5GS additional request result 790
8.2.7.44 NSSRG information 790
8.2.7.45 disaster roaming wait range 790
8.2.7.46 disaster return wait range 790
8.2.7.47 list of PLMNs to be used in disaster condition 791
8.2.7.48 forbidden TAI(s) for the list of "5GS forbidden tracking areas for roaming" 791
8.2.7.49 forbidden TAI(s) for the list of "5GS forbidden tracking areas for regional provision of service" 791
8.2.7.50 extended CAG information list 791
8.2.7.51 NSAG information 791
8.2.7.52 equivalent SNPNs 791
8.2.7.53 NID 791
8.2.7.54 registration accept type 6 IE container 791
8.2.7.54.1 general 791
8.2.7.54.2 extended LADN information 792
8.2.7.54.3 S-NSSAI location validity information 792
8.2.7.54.4 void 792
8.2.7.54.5 partially allowed NSSAI 792
8.2.7.54.6 partially rejected NSSAI 792
8.2.7.55 RAN timing synchronization 792
8.2.7.56 alternative NSSAI 792
8.2.7.57 maximum time offset 792
8.2.7.58 S-NSSAI time validity information 792
8.2.7.59 unavailability configuration 792
8.2.7.60 feature authorization indication 793
8.2.7.61 On-demand NSSAI 793
8.2.7.62 RAT utilization control 793
8.2.8 registration complete 793
8.2.8.1 message definition 793
8.2.8.2 SOR transparent container 793
8.2.9 registration reject 793
8.2.9.1 message definition 793
8.2.9.2 T3346 value 794
8.2.9.3 T3502 value 794
8.2.9.4 EAP message 794
8.2.9.5 rejected NSSAI 795
8.2.9.6 CAG information list 795
8.2.9.7 extended rejected NSSAI 795
8.2.9.8 disaster return wait range 795
8.2.9.9 extended CAG information list 795
8.2.9.10 lower bound timer value 795
8.2.9.11 forbidden TAI(s) for the list of "5GS forbidden tracking areas for roaming" 795
8.2.9.12 forbidden TAI(s) for the list of "5GS forbidden tracking areas for regional provision of service" 795
8.2.9.13 N3IWF identifier 795
8.2.9.14 TNAN information 795
8.2.9.15 extended 5GMM cause 795
8.2.9.16 RAT utilization control 796
8.2.10 UL NAS transport 796
8.2.10.1 message definition 796
8.2.10.2 PDU session ID 796
8.2.10.3 old PDU session ID 797
8.2.10.4 request type 797
8.2.10.5 S-NSSAI 797
8.2.10.6 DNN 797
8.2.10.7 additional information 797
8.2.10.8 MA PDU session information 797
8.2.10.9 release assistance indication 797
8.2.10.10 Non-3GPP access path switching indication 797
8.2.10.11 alternative S-NSSAI 797
8.2.10.12 payload container information 797
8.2.11 DL NAS transport 798
8.2.11.1 message definition 798
8.2.11.2 PDU session ID 798
8.2.11.3 additional information 798
8.2.11.4 5GMM cause 798
8.2.11.5 Back-off timer value 798
8.2.11.6 lower bound timer value 799
8.2.12 De-registration request (UE originating de-registration) 799
8.2.12.1 message definition 799
8.2.12.2 unavailability information 799
8.2.12.3 NAS message container 799
8.2.13 De-registration accept (UE originating de-registration) 799
8.2.13.1 message definition 799
8.2.14 De-registration request (UE terminated de-registration) 800
8.2.14.1 message definition 800
8.2.14.2 5GMM cause 801
8.2.14.3 T3346 value 801
8.2.14.4 rejected NSSAI 801
8.2.14.5 CAG information list 801
8.2.14.6 extended rejected NSSAI 802
8.2.14.7 disaster return wait range 802
8.2.14.7A extended CAG information list 802
8.2.14.8 lower bound timer value 802
8.2.14.9 forbidden TAI(s) for the list of "5GS forbidden tracking areas for roaming" 802
8.2.14.10 forbidden TAI(s) for the list of "5GS forbidden tracking areas for regional provision of service" 802
8.2.14.11 RAT utilization control 802
8.2.15 De-registration accept (UE terminated de-registration) 802
8.2.15.1 message definition 802
8.2.16 service request 803
8.2.16.1 message definition 803
8.2.16.2 uplink data status 803
8.2.16.3 PDU session status 803
8.2.16.4 allowed PDU session status 803
8.2.16.5 NAS message container 804
8.2.16.6 UE request type 804
8.2.16.7 paging restriction 804
8.2.17 service accept 804
8.2.17.1 message definition 804
8.2.17.2 PDU session status 805
8.2.17.3 PDU session reactivation result 805
8.2.17.4 PDU session reactivation result error cause 805
8.2.17.5 EAP message 805
8.2.17.6 T3448 value 805
8.2.17.7 5GS additional request result 805
8.2.17.8 forbidden TAI(s) for the list of "5GS forbidden tracking areas for roaming" 805
8.2.17.9 forbidden TAI(s) for the list of "5GS forbidden tracking areas for regional provision of service" 805
8.2.18 service reject 805
8.2.18.1 message definition 805
8.2.18.2 PDU session status 806
8.2.18.3 T3346 value 806
8.2.18.4 EAP message 806
8.2.18.5 T3448 value 806
8.2.18.6 CAG information list 807
8.2.18.7 disaster return wait range 807
8.2.18.8 extended CAG information list 807
8.2.18.9 lower bound timer value 807
8.2.18.10 forbidden TAI(s) for the list of "5GS forbidden tracking areas for roaming" 807
8.2.18.11 forbidden TAI(s) for the list of "5GS forbidden tracking areas for regional provision of service" 807
8.2.19 configuration update command 807
8.2.19.1 message definition 807
8.2.19.2 configuration update indication 810
8.2.19.3 5G-GUTI 810
8.2.19.4 TAI list 810
8.2.19.5 allowed NSSAI 810
8.2.19.6 service area list 810
8.2.19.7 full name for network 811
8.2.19.8 short name for network 811
8.2.19.9 local time zone 811
8.2.19.10 universal time and local time zone 811
8.2.19.11 network daylight saving time 811
8.2.19.12 LADN information 811
8.2.19.13 MICO indication 811
8.2.19.14 network slicing indication 811
8.2.19.15 configured NSSAI 811
8.2.19.16 rejected NSSAI 811
8.2.19.17 Operator-defined access category definitions 811
8.2.19.18 SMS indication 811
8.2.19.19 T3447 value 811
8.2.19.20 CAG information list 812
8.2.19.21 UE radio capability ID 812
8.2.19.22 UE radio capability ID deletion indication 812
8.2.19.23 5GS registration result 812
8.2.19.24 truncated 5G-S-TMSI configuration 812
8.2.19.25 additional configuration indication 812
8.2.19.26 extended rejected NSSAI 812
8.2.19.27 Service-level-AA container 812
8.2.19.28 NSSRG information 812
8.2.19.29 disaster roaming wait range 812
8.2.19.30 disaster return wait range 812
8.2.19.31 list of PLMNs to be used in disaster condition 813
8.2.19.32 extended CAG information list 813
8.2.19.33 updated PEIPS assistance information 813
8.2.19.34 NSAG information 813
8.2.19.35 priority indicator 813
8.2.19.36 RAN timing synchronization 813
8.2.19.37 extended LADN information 813
8.2.19.38 alternative NSSAI 813
8.2.19.39 S-NSSAI location validity information 813
8.2.19.40 S-NSSAI time validity information 813
8.2.19.41 maximum time offset 813
8.2.19.42 partially allowed NSSAI 814
8.2.19.43 partially rejected NSSAI 814
8.2.19.44 feature authorization indication 814
8.2.19.45 On-demand NSSAI 814
8.2.19.46 RAT utilization control 814
8.2.20 configuration update complete 814
8.2.20.1 message definition 814
8.2.20.2 void 814
8.2.21 identity request 814
8.2.21.1 message definition 814
8.2.22 identity response 815
8.2.22.1 message definition 815
8.2.23 notification 815
8.2.23.1 message definition 815
8.2.24 notification response 816
8.2.24.1 message definition 816
8.2.24.2 PDU session status 816
8.2.25 security mode command 816
8.2.25.1 message definition 816
8.2.25.2 IMEISV request 817
8.2.25.3 void 817
8.2.25.4 selected EPS NAS security algorithms 817
8.2.25.5 additional 5G security information 817
8.2.25.6 EAP message 818
8.2.25.7 ABBA 818
8.2.25.8 replayed S1 UE security capabilities 818
8.2.25.9 AUN3 device security key 818
8.2.26 security mode complete 818
8.2.26.1 message definition 818
8.2.26.2 IMEISV 818
8.2.26.3 NAS message container 818
8.2.26.4 non-IMEISV PEI 819
8.2.27 security mode reject 819
8.6.27.1 message definition 819
8.2.28 security protected 5GS NAS message 819
8.2.28.1 message definition 819
8.2.29 5GMM status 820
8.2.29.1 message definition 820
8.2.30 control plane service request 820
8.2.30.1 message definition 820
8.2.30.2 CIoT small data container 821
8.2.30.3 payload container type 821
8.2.30.4 payload container 821
8.2.30.5 PDU session ID 821
8.2.30.6 PDU session status 822
8.2.30.7 release assistance indication 822
8.2.30.8 uplink data status 822
8.2.30.9 NAS message container 822
8.2.30.10 additional information 822
8.2.30.11 allowed PDU session status 822
8.2.30.12 UE request type 822
8.2.30.13 paging restriction 822
8.2.31 network slice-specific authentication command 822
8.2.31.1 message definition 822
8.2.32 network slice-specific authentication complete 823
8.2.32.1 message definition 823
8.2.33 network slice-specific authentication result 823
8.2.33.1 message definition 823
8.2.34 relay key request 824
8.2.34.1 message definition 824
8.2.35 relay key accept 824
8.2.35.1 message definition 824
8.2.35.2 EAP message 825
8.2.36 relay key reject 825
8.2.36.1 message definition 825
8.2.36.2 EAP message 825
8.2.37 relay authentication request 826
8.2.37.1 message definition 826
8.2.38 relay authentication response 826
8.2.38.1 message definition 826
8.3 5GS session management messages 827
8.3.1 PDU session establishment request 827
8.3.1.1 message definition 827
8.3.1.2 PDU session type 828
8.3.1.3 SSC mode 829
8.3.1.4 maximum number of supported packet filters 829
8.3.1.5 5GSM capability 829
8.3.1.6 void 829
8.3.1.7 Always-on PDU session requested 829
8.3.1.8 SM PDU DN request container 829
8.3.1.9 extended protocol configuration options 829
8.3.1.10 IP header compression configuration 829
8.3.1.11 DS-TT ethernet port MAC address 829
8.3.1.12 UE-DS-TT residence time 829
8.3.1.13 port management information container 830
8.3.1.14 ethernet header compression configuration 830
8.3.1.15 suggested interface identifier 830
8.3.1.16 Service-level-AA container 830
8.3.1.17 requested MBS container 830
8.3.1.18 PDU session pair ID 830
8.3.1.19 RSN 830
8.3.1.20 URSP rule enforcement reports 830
8.3.2 PDU session establishment accept 830
8.3.2.1 message definition 830
8.3.2.2 5GSM cause 832
8.3.2.3 PDU address 832
8.3.2.4 RQ timer value 832
8.3.2.5 S-NSSAI 832
8.3.2.6 Always-on PDU session indication 832
8.3.2.7 mapped EPS bearer contexts 832
8.3.2.8 EAP message 832
8.3.2.9 authorized QoS flow descriptions 832
8.3.2.10 extended protocol configuration options 832
8.3.2.11 DNN 832
8.3.2.12 5GSM network feature support 832
8.3.2.13 void 832
8.3.2.14 serving PLMN rate control 832
8.3.2.15 ATSSS container 833
8.3.2.16 control plane only indication 833
8.3.2.17 IP header compression configuration 833
8.3.2.18 ethernet header compression configuration 833
8.3.2.19 Service-level-AA container 833
8.3.2.20 received MBS container 833
8.3.2.21 N3QAI 833
8.3.2.22 protocol description 833
8.3.2.23 ECN marking for L4S indication 833
8.3.3 PDU session establishment reject 833
8.3.3.1 message definition 833
8.3.3.2 Back-off timer value 834
8.3.3.3 allowed SSC mode 834
8.3.3.4 EAP message 834
8.3.3.4A 5GSM congestion re-attempt indicator 834
8.3.3.5 extended protocol configuration options 835
8.3.3.6 Re-attempt indicator 835
8.3.3.7 Service-level-AA container 835
8.3.4 PDU session authentication command 835
8.3.4.1 message definition 835
8.3.4.2 extended protocol configuration options 835
8.3.4.3 void 836
8.3.5 PDU session authentication complete 836
8.3.5.1 message definition 836
8.3.5.2 extended protocol configuration options 836
8.3.5.3 void 836
8.3.6 PDU session authentication result 836
8.3.6.1 message definition 836
8.3.6.2 EAP message 837
8.3.6.3 extended protocol configuration options 837
8.3.7 PDU session modification request 837
8.3.7.1 message definition 837
8.3.7.2 5GSM capability 838
8.3.7.3 5GSM cause 839
8.3.7.4 maximum number of supported packet filters 839
8.3.7.5 Always-on PDU session requested 839
8.3.7.6 integrity protection maximum data rate 839
8.3.7.7 requested QoS rules 839
8.3.7.8 requested QoS flow descriptions 839
8.3.7.9 extended protocol configuration options 839
8.3.7.10 mapped EPS bearer contexts 839
8.3.7.11 port management information container 839
8.3.7.12 IP header compression configuration 839
8.3.7.13 ethernet header compression configuration 840
8.3.7.14 requested MBS container 840
8.3.7.15 Service-level-AA container 840
8.3.7.16 Non-3GPP delay budget 840
8.3.7.17 URSP rule enforcement reports 840
8.3.8 PDU session modification reject 840
8.3.8.1 message definition 840
8.3.8.2 Back-off timer value 841
8.3.8.2A 5GSM congestion re-attempt indicator 841
8.3.8.3 extended protocol configuration options 841
8.3.8.4 Re-attempt indicator 841
8.3.9 PDU session modification command 841
8.3.9.1 message definition 841
8.3.9.2 5GSM cause 842
8.3.9.3 Session-AMBR 843
8.3.9.4 RQ timer value 843
8.3.9.5 Always-on PDU session indication 843
8.3.9.6 authorized QoS rules 843
8.3.9.7 mapped EPS bearer contexts 843
8.3.9.8 authorized QoS flow descriptions 843
8.3.9.9 extended protocol configuration options 843
8.3.9.10 void 843
8.3.9.11 ATSSS container 843
8.3.9.12 IP header compression configuration 843
8.3.9.13 port management information container 843
8.3.9.14 serving PLMN rate control 843
8.3.9.15 ethernet header compression configuration 844
8.3.9.16 received MBS container 844
8.3.9.17 Service-level-AA container 844
8.3.9.18 alternative S-NSSAI 844
8.3.9.19 N3QAI 844
8.3.9.20 protocol description 844
8.3.9.21 ECN marking for L4S indication 844
8.3.10 PDU session modification complete 844
8.3.10.1 message definition 844
8.3.10.2 extended protocol configuration options 845
8.3.10.3 port management information container 845
8.3.11 PDU session modification command reject 845
8.3.11.1 message definition 845
8.3.11.2 extended protocol configuration options 846
8.3.12 PDU session release request 846
8.3.12.1 message definition 846
8.3.12.2 5GSM cause 846
8.3.12.3 extended protocol configuration options 846
8.3.13 PDU session release reject 846
8.3.13.1 message definition 846
8.3.13.2 extended protocol configuration options 847
8.3.14 PDU session release command 847
8.3.14.1 message definition 847
8.3.14.2 Back-off timer value 848
8.3.14.3 EAP message 848
8.3.14.4 extended protocol configuration options 848
8.3.14.5 5GSM congestion re-attempt indicator 848
8.3.14.6 access type 848
8.3.14.7 Service-level-AA container 848
8.3.14.8 alternative S-NSSAI 849
8.3.15 PDU session release complete 849
8.3.15.1 message definition 849
8.3.15.2 5GSM cause 849
8.3.15.3 extended protocol configuration options 849
8.3.16 5GSM status 849
8.3.16.1 message definition 849
8.3.17 Service-level authentication command 850
8.3.17.1 message definition 850
8.3.18 Service-level authentication complete 850
8.3.18.1 message definition 850
8.3.19 remote UE report 851
8.3.19.1 message definition 851
8.3.19.2 remote UE context connected 851
8.3.19.3 remote UE context disconnected 851
8.3.20 remote UE report response 852
8.3.20.1 message definition 852
8.3.20.2 void 852
8.3.20.3 void 852
8.3.20.4 void 852
9 general message format and information elements coding 852
9.1 overview 852
9.1.1 NAS message format 852
9.1.2 field format and mapping 853
9.2 extended protocol discriminator 854
9.3 security header type 854
9.4 PDU session identity 854
9.5 spare half octet 854
9.6 procedure transaction identity 854
9.7 message type 855
9.8 message authentication code 856
9.9 plain 5GS NAS message 856
9.10 sequence number 856
9.11 other information elements 857
9.11.1 general 857
9.11.2 common information elements 857
9.11.2.1 additional information 857
9.11.2.1A access type 858
9.11.2.1B DNN 858
9.11.2.2 EAP message 858
9.11.2.3 GPRS timer 859
9.11.2.4 GPRS timer 2 859
9.11.2.5 GPRS timer 3 859
9.11.2.6 intra N1 mode NAS transparent container 859
9.11.2.7 N1 mode to S1 mode NAS transparent container 860
9.11.2.8 S-NSSAI 860
9.11.2.9 S1 mode to N1 mode NAS transparent container 862
9.11.2.10 Service-level-AA container 863
9.11.2.11 Service-level device ID 866
9.11.2.12 Service-level-AA server address 866
9.11.2.13 Service-level-AA payload 867
9.11.2.14 Service-level-AA response 867
9.11.2.15 Service-level-AA payload type 868
9.11.2.16 void 869
9.11.2.17 Service-level-AA pending indication 869
9.11.2.18 Service-level-AA service status indication 869
9.11.2.19 time duration 869
9.11.2.20 unavailability information 869
9.11.2.21 unavailability configuration 870
9.11.3 5GS mobility management (5GMM) information elements 870
9.11.3.1 5GMM capability 870
9.11.3.2 5GMM cause 879
9.11.3.2A 5GS DRX parameters 883
9.11.3.3 5GS identity type 883
9.11.3.4 5GS mobile identity 884
9.11.3.5 5GS network feature support 890
9.11.3.6 5GS registration result 896
9.11.3.7 5GS registration type 897
9.11.3.8 5GS tracking area identity 898
9.11.3.9 5GS tracking area identity list 899
9.11.3.9A 5GS update type 904
9.11.3.10 ABBA 905
9.11.3.11 void 906
9.11.3.12 additional 5G security information 906
9.11.3.12A additional information requested 906
9.11.3.13 allowed PDU session status 907
9.11.3.14 authentication failure parameter 908
9.11.3.15 authentication parameter AUTN 908
9.11.3.16 authentication parameter RAND 908
9.11.3.17 authentication response parameter 908
9.11.3.18 configuration update indication 908
9.11.3.18A CAG information list 908
9.11.3.18B CIoT small data container 910
9.11.3.18C ciphering key data 914
9.11.3.18D control plane service type 923
9.11.3.19 daylight saving time 923
9.11.3.20 De-registration type 923
9.11.3.21 void 924
9.11.3.22 void 924
9.11.3.23 emergency number list 924
9.11.3.23A EPS bearer context status 924
9.11.3.24 EPS NAS message container 924
9.11.3.25 EPS NAS security algorithms 925
9.11.3.26 extended emergency number list 925
9.11.3.26A extended DRX parameters 925
9.11.3.27 void 925
9.11.3.28 IMEISV request 925
9.11.3.29 LADN indication 925
9.11.3.30 LADN information 926
9.11.3.31 MICO indication 927
9.11.3.31A MA PDU session information 928
9.11.3.31B mapped NSSAI 928
9.11.3.31C mobile station classmark 2 929
9.11.3.32 NAS key set identifier 930
9.11.3.33 NAS message container 930
9.11.3.34 NAS security algorithms 931
9.11.3.35 network name 931
9.11.3.36 network slicing indication 931
9.11.3.36A Non-3GPP NW provided policies 932
9.11.3.37 NSSAI 932
9.11.3.37A NSSAI inclusion mode 933
9.11.3.38 Operator-defined access category definitions 933
9.11.3.39 payload container 937
9.11.3.40 payload container type 944
9.11.3.41 PDU session identity 2 944
9.11.3.42 PDU session reactivation result 945
9.11.3.43 PDU session reactivation result error cause 945
9.11.3.44 PDU session status 946
9.11.3.45 PLMN list 946
9.11.3.46 rejected NSSAI 946
9.11.3.46A release assistance indication 948
9.11.3.47 request type 948
9.11.3.48 S1 UE network capability 949
9.11.3.48A S1 UE security capability 949
9.11.3.49 service area list 949
9.11.3.50 service type 954
9.11.3.50A SMS indication 954
9.11.3.51 SOR transparent container 955
9.11.3.51A supported codec list 973
9.11.3.52 time zone 973
9.11.3.53 time zone and time 973
9.11.3.53A UE parameters update transparent container 973
9.11.3.54 UE security capability 976
9.11.3.55 UE's usage setting 981
9.11.3.56 UE status 981
9.11.3.57 uplink data status 982
9.11.3.58 void 983
9.11.3.59 void 983
9.11.3.60 void 983
9.11.3.61 void 983
9.11.3.62 void 983
9.11.3.63 void 983
9.11.3.64 void 983
9.11.3.65 void 983
9.11.3.66 void 983
9.11.3.67 void 983
9.11.3.68 UE radio capability ID 983
9.11.3.69 UE radio capability ID deletion indication 983
9.11.3.70 truncated 5G-S-TMSI configuration 984
9.11.3.71 WUS assistance information 985
9.11.3.72 N5GC indication 985
9.11.3.73 NB-N1 mode DRX parameters 986
9.11.3.74 additional configuration indication 986
9.11.3.75 extended rejected NSSAI 987
9.11.3.76 UE request type 991
9.11.3.77 paging restriction 991
9.11.3.78 void 992
9.11.3.79 NID 992
9.11.3.80 PEIPS assistance information 992
9.11.3.81 5GS additional request result 994
9.11.3.82 NSSRG information 995
9.11.3.83 list of PLMNs to be used in disaster condition 996
9.11.3.84 registration wait range 997
9.11.3.85 PLMN identity 998
9.11.3.86 extended CAG information list 998
9.11.3.87 NSAG information 1003
9.11.3.88 ProSe relay transaction identity 1004
9.11.3.89 relay key request parameters 1005
9.11.3.90 relay key response parameters 1006
9.11.3.91 priority indicator 1007
9.11.3.92 SNPN list 1007
9.11.3.93 N3IWF identifier 1008
9.11.3.94 TNAN information 1009
9.11.3.95 RAN timing synchronization 1010
9.11.3.96 extended LADN information 1011
9.11.3.97 alternative NSSAI 1012
9.11.3.98 type 6 IE container 1013
9.11.3.99 Non-3GPP access path switching indication 1014
9.11.3.100 S-NSSAI location validity information 1015
9.11.3.101 S-NSSAI time validity information 1016
9.11.3.102 Non-3GPP path switching information 1018
9.11.3.103 partial NSSAI 1019
9.11.3.104 AUN3 indication 1020
9.11.3.106 payload container information 1021
9.11.3.107 AUN3 device security key 1021
9.11.3.108 On-demand NSSAI 1022
9.11.3.109 extended 5GMM cause 1023
9.11.3.110 RAT utilization control 1023
9.11.4 5GS session management (5GSM) information elements 1023
9.11.4.1 5GSM capability 1023
9.11.4.2 5GSM cause 1026
9.11.4.3 Always-on PDU session indication 1027
9.11.4.4 Always-on PDU session requested 1028
9.11.4.5 allowed SSC mode 1028
9.11.4.6 extended protocol configuration options 1029
9.11.4.7 integrity protection maximum data rate 1029
9.11.4.8 mapped EPS bearer contexts 1030
9.11.4.9 maximum number of supported packet filters 1034
9.11.4.10 PDU address 1034
9.11.4.11 PDU session type 1036
9.11.4.12 QoS flow descriptions 1036
9.11.4.13 QoS rules 1043
9.11.4.14 Session-AMBR 1051
9.11.4.15 SM PDU DN request container 1052
9.11.4.16 SSC mode 1053
9.11.4.17 Re-attempt indicator 1053
9.11.4.18 5GSM network feature support 1054
9.11.4.19 void 1055
9.11.4.20 serving PLMN rate control 1055
9.11.4.21 5GSM congestion re-attempt indicator 1055
9.11.4.22 ATSSS container 1055
9.11.4.23 control plane only indication 1056
9.11.4.24 IP header compression configuration 1056
9.11.4.25 DS-TT ethernet port MAC address 1060
9.11.4.26 UE-DS-TT residence time 1060
9.11.4.27 port management information container 1061
9.11.4.28 ethernet header compression configuration 1061
9.11.4.29 remote UE context list 1062
9.11.4.30 requested MBS container 1066
9.11.4.31 received MBS container 1068
9.11.4.32 PDU session pair ID 1075
9.11.4.33 RSN 1076
9.11.4.34 ECS address 1076
9.11.4.35 void 1082
9.11.4.36 N3QAI 1082
9.11.4.37 Non-3GPP delay budget 1086
9.11.4.38 URSP rule enforcement reports 1088
9.11.4.39 protocol description 1089
9.11.4.40 ECN marking for L4S indication 1093
9.12 3GPP specific coding information defined within present document 1093
9.12.1 serving network name (SNN) 1093
10 list of system parameters 1095
10.1 general 1095
10.2 timers of 5GS mobility management 1095
10.3 timers of 5GS session management 1106
10.4 void 1112