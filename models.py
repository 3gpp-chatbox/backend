from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict

class NetworkElement(BaseModel):
    name: str
    type: str = Field(default="Network Element")
    description: str

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
    specReference: str
    protocol: str = Field(default="5G NAS")
    timer: Optional[str] = None

class PeriodicRegistrationData(BaseModel):
    trigger: str
    description: str
    nodes: List[Dict]
    edges: List[Dict]
    metadata: PeriodicRegistrationMetadata
    network_elements: List[NetworkElement]
    procedure_flow: List[PeriodicRegistrationStep] 