from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


# Define Pydantic models for structured response
class Metadata(BaseModel):
    """Metadata for tracking document sources and references in 3GPP specifications.

    Contains information about the source document, section references, and relevant
    specification details where the information was extracted from.
    """

    document_id: str
    section_reference: str | None = None  # e.g., "5.2.2.3.1"
    other_references: list[str] = Field(default_factory=list)
    # specification_version: str | None = None  # e.g., "Rel-16"


class NodeProperties(BaseModel):
    """Properties specific to nodes in the property graph."""

    messageType: str | None = None
    state: str | None = None
    eventType: str | None = None
    description: str | None = None


class Node(BaseModel):
    """Represents a node in the property graph with associated 3GPP specification metadata."""

    id: str
    type: Literal["State", "Event"]  # 'state' or 'event'
    entity: str  # 'UE', 'AMF', 'SMF', etc.
    properties: NodeProperties = Field(default_factory=NodeProperties)
    metadata: Metadata = Field(default_factory=Metadata)


class EdgeProperties(BaseModel):
    """Properties specific to edges in the property graph."""

    messageType: str | None = None
    parameters: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    sourceState: str | None = None
    targetState: str | None = None
    description: str | None = None


class Edge(BaseModel):
    """Represents an edge in the property graph."""

    id: str
    from_: str = Field(..., alias="from")
    to: str
    type: str
    properties: EdgeProperties = Field(default_factory=EdgeProperties)
    model_config = ConfigDict(populate_by_name=True)


class FlowPropertyGraph(BaseModel):
    """Represents the complete flow property graph."""

    procedureName: str
    nodes: list[Node]
    edges: list[Edge]
