from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from backend.embeddings.embedding_service import EmbeddingService
from backend.models.conversation_chunk import ConversationChunk

class FAISSService:
    """
    Handles creation, persistence and retrieval
    of FAISS vector indexes.
    """

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.embedding_model = (
            self.embedding_service.get_embedding_model()
        )

        self.vector_store = None

    def build_index(
    self,
    chunks: List[ConversationChunk],
) -> None:

        documents = [
        chunk.document
        for chunk in chunks
    ]

        self.vector_store = FAISS.from_documents(
        documents,
        self.embedding_model,
    )

    def save(
        self,
        conversation_id: int,
    ) -> None:

        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")

        path = Path(
            f"data/vector_store/conversation_{conversation_id}"
        )

        path.mkdir(parents=True, exist_ok=True)

        self.vector_store.save_local(str(path))

    def load(
        self,
        conversation_id: int,
    ) -> None:

        path = Path(
            f"data/vector_store/conversation_{conversation_id}"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"No vector index found for conversation {conversation_id}"
            )

        self.vector_store = FAISS.load_local(
            str(path),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:

        if self.vector_store is None:
            raise ValueError(
                "Vector store not initialized."
            )

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def as_retriever(
        self,
        k: int = 5,
    ):

        if self.vector_store is None:
            raise ValueError(
                "Vector store not initialized."
            )

        return self.vector_store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )