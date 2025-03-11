from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class NetworkElement(BaseModel):
    name: str
    type: str = Field(default="Network Element")
    description: str

class State(BaseModel):
    name: str
    description: str
    network_element: str

class RegistrationStep(BaseModel):
    sequence_number: int
    source: str
    target: str
    message: str
    description: str
    source_state: Optional[str] = None
    target_state: Optional[str] = None
    trigger: Optional[Union[str, List[str]]] = None
    conditions: Optional[List[str]] = []
    timing: Optional[str] = None

class Metadata(BaseModel):
    procedure_type: str = Field(default="Initial Registration")
    spec_reference: str
    protocol: str = Field(default="5G NAS")

class RegistrationAnalysis(BaseModel):
    metadata: Metadata
    network_elements: List[NetworkElement]
    states: List[State]
    procedure_steps: List[RegistrationStep]

class ProcedureStep(BaseModel):
    sequence_number: int
    source: str
    target: str
    message: str
    description: str
    source_state: Optional[str] = None
    target_state: Optional[str] = None
    trigger: Optional[Union[str, List[str]]] = None
    conditions: Optional[List[str]] = []
    timing: Optional[str] = None

class Procedure(BaseModel):
    name: str
    description: str

class RegistrationData(BaseModel):
    procedure: Procedure
    network_elements: List[NetworkElement]
    procedure_flow: List[ProcedureStep]

# Periodic Registration specific models
class PeriodicRegistrationStep(ProcedureStep):
    message_type: Optional[str] = None
    parameters: Optional[List[str]] = []
    outcome: Optional[str] = None

class PeriodicRegistrationMetadata(BaseModel):
    procedureName: str = Field(default="Periodic Registration Update")
    specReference: str = Field(default="3GPP TS 24.501")
    protocol: str = Field(default="5G NAS")
    timer: Optional[str] = None
    parameters: Optional[Dict[str, str]] = Field(default_factory=dict)

class Node(BaseModel):
    id: str
    label: str
    source: str
    target: str
    messageType: Optional[str] = None
    type: Optional[str] = None

class Edge(BaseModel):
    from_: str = Field(alias="from")
    to: str
    label: str
    condition: Optional[str] = None

class PeriodicRegistrationData(BaseModel):
    procedure: str = Field(default="Periodic Registration")
    trigger: str
    description: str = Field(default="Periodic Registration Update procedure")
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    metadata: PeriodicRegistrationMetadata
    network_elements: List[NetworkElement]
    procedure_flow: List[PeriodicRegistrationStep] 