from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class NetworkElement(BaseModel):
    name: str
    type: str
    description: str = Field(default="")

class State(BaseModel):
    name: str
    type: str = Field(description="INITIAL/INTERMEDIATE/FINAL")
    description: str = Field(default="")

class RegistrationStep(BaseModel):
    sequence_number: int
    step_name: str
    source_element: str
    destination_element: str
    message: str
    source_state: str
    destination_state: str
    description: str
    trigger: str
    conditions: List[str]
    timing: str

class Metadata(BaseModel):
    procedure_name: str
    total_steps: int
    source: str
    extraction_time: datetime = Field(default_factory=datetime.now)

class RegistrationAnalysis(BaseModel):
    network_elements: List[NetworkElement]
    states: List[State]
    registration_flow: List[RegistrationStep]
    metadata: Metadata 