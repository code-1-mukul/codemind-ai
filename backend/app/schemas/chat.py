from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: MessageRole = Field(..., description="Role of the sender")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    repository_name:str
    question: str = Field(..., description="User's current question")
    session_id: Optional[str] = Field(
        default=None,
        description="Conversation session ID. Leave empty to start a new conversation."
    )


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Assistant's response")
    session_id: str = Field(..., description="Conversation session ID")
    sources: Optional[List[str]] = Field(
        default=None,
        description="Relevant source files used to answer the question"
    )