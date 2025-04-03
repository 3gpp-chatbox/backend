
flowchart TD
    start(("start")) --> 1["UE sends REGISTRATION REQUEST"]
    1 --> 2{{"UE starts timer T3510"}}
    2 --> 3{{"Initial registration request is accepted by the network?"}}
    3 -- Yes: AMF sends REGISTRATION ACCEPT --> 4["AMF sends REGISTRATION ACCEPT"]
    3 -- No: AMF sends REGISTRATION REJECT --> 13["AMF sends REGISTRATION REJECT"]
    4 --> 5{{"5G-GUTI or SOR transparent container IE included?"}}
    5 -- Yes: AMF starts timer T3550 --> 6{{"AMF starts timer T3550"}}
    5 -- No: UE resets counter --> 7["UE resets counter, enters 5GMM-REGISTERED"]
    6 --> 12["AMF stops timer T3550, enters 5GMM-REGISTERED"]
    7 --> 8{{"Network slicing indication IE present?"}}
    8 -- Yes: UE returns REGISTRATION COMPLETE --> 12
    8 -- No --> 9{{"CAG information list IE present and CAG supported?"}}
    9 --> 10{{"Operator-defined access category definitions IE present?"}}
    10 -- Yes: UE returns REGISTRATION COMPLETE --> 12
    10 -- No --> 11{{"UE radio capability ID IE present?"}}
    11 -- Yes: UE returns REGISTRATION COMPLETE --> 12
    11 -- No --> endNode(("end"))
    12 --> endNode
    13 --> endNode