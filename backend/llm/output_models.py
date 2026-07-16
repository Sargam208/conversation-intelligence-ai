
from typing import List, Optional

from pydantic import BaseModel


class Decision(BaseModel):
    title: str
    details: str
    confidence: Optional[str] = "High"


class ActionItem(BaseModel):
    assignee: Optional[str]
    task: str
    deadline: Optional[str]
    priority: Optional[str] = "Medium"


class ConversationSummary(BaseModel):
    executive_summary: str

    key_discussion_points: List[str]

    important_decisions: List[Decision]

    action_items: List[ActionItem]

    deadlines: List[str]