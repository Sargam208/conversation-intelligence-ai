from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a single chat message.
    """

    sender: str
    message: str
    timestamp: datetime


class Conversation(BaseModel):
    """
    Represents an uploaded conversation.
    """

    conversation_id: Optional[int] = None

    file_name: str

    file_hash: str

    participants: List[str] = Field(default_factory=list)

    total_messages: int = 0

    uploaded_at: datetime = Field(
        default_factory=datetime.now
    )

class Task(BaseModel):
    """
    Represents an extracted action item.
    """

    assignee: str
    task: str
    deadline: Optional[str] = None


class AIInsight(BaseModel):
    """
    Stores AI-generated insights.
    """

    summary: str
    topics: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)