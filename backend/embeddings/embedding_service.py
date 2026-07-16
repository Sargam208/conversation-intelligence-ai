from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from backend.database.models import Message
from backend.models.conversation_chunk import ConversationChunk
from langchain_text_splitters import RecursiveCharacterTextSplitter


class EmbeddingService:
    """
    Creates semantic conversation chunks.
    """

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def get_embedding_model(self):

        return self.embedding_model

    def create_chunks(
        self,
        messages: List[Message],
    ) -> List[ConversationChunk]:

        chunks = []

        chunk_size = 8
        overlap = 2

        chunk_id = 0

        step = chunk_size - overlap

        for start in range(
            0,
            len(messages),
            step,
        ):

            chunk_messages = messages[
                start:start + chunk_size
            ]

            if not chunk_messages:
                continue

            text = "\n".join(
                f"[{msg.timestamp}] {msg.sender}: {msg.message}"
                for msg in chunk_messages
            )

            participants = sorted(
                {
                    msg.sender
                    for msg in chunk_messages
                }
            )

            document = Document(
                page_content=text,
                metadata={
                    "chunk_id": chunk_id,
                    "participants": participants,
                    "message_count": len(
                        chunk_messages
                    ),
                    "start_time":
                    chunk_messages[
                        0
                    ].timestamp.isoformat(),
                    "end_time":
                    chunk_messages[
                        -1
                    ].timestamp.isoformat(),
                },
            )

            chunks.append(

                ConversationChunk(

                    chunk_id=chunk_id,

                    messages=chunk_messages,

                    document=document,

                    participants=participants,

                    start_time=
                    chunk_messages[
                        0
                    ].timestamp,

                    end_time=
                    chunk_messages[
                        -1
                    ].timestamp,
                )

            )

            chunk_id += 1

        return chunks