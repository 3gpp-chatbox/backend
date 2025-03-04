from pydantic import BaseModel, Field
from typing import List, Optional, Union

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