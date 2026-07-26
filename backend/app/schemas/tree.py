from pydantic import BaseModel, Field


class TreeNode(BaseModel):
    name: str
    path: str
    is_directory: bool
    children: list["TreeNode"] = Field(default_factory=list)


TreeNode.model_rebuild()