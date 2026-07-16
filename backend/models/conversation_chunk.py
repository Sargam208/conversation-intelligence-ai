from dataclasses import dataclass
from datetime import datetime
from typing import List

from langchain_core.documents import Document

from backend.database.models import Message


@dataclass
class ConversationChunk:
    """
    Represents one semantic chunk of a conversation.
    """

    chunk_id: int

    messages: List[Message]

    document: Document

    participants: List[str]

    start_time: datetime

    end_time: datetime