from pydantic import BaseModel


class ArchitectureNode(BaseModel):
    id: str
    label: str
    type: str
    group: str | None = None

class ArchitectureEdge(BaseModel):
    source: str
    target: str
    relation: str


class ArchitectureGraph(BaseModel):
    nodes: list[ArchitectureNode]
    edges: list[ArchitectureEdge]

class FlowNode(BaseModel):
    id: str
    label: str
    type: str


class FlowEdge(BaseModel):
    source: str
    target: str
    relation: str


class DataFlowGraph(BaseModel):
    nodes: list[FlowNode]
    edges: list[FlowEdge]