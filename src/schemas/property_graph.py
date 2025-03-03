from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


# Define Pydantic models for structured response
class NodeProperties(BaseModel):
    messageType: str | None = None
    state: str | None = None
    eventType: str | None = None
    description: str | None = None


class Node(BaseModel):
    id: str
    type: Literal["State", "Event"]  # 'state' or 'event'
    entity: str  # 'UE', 'AMF', 'SMF', etc.
    properties: NodeProperties = Field(default_factory=NodeProperties)


class EdgeProperties(BaseModel):
    messageType: str | None = None
    parameters: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    sourceState: str | None = None
    targetState: str | None = None
    description: str | None = None


class Edge(BaseModel):
    id: str
    from_: str = Field(..., alias="from")
    to: str
    type: str
    properties: EdgeProperties = Field(default_factory=EdgeProperties)
    model_config = ConfigDict(populate_by_name=True)


class FlowPropertyGraph(BaseModel):
    procedureName: str
    nodes: list[Node]
    edges: list[Edge]
