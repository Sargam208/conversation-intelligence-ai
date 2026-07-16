from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from backend.vectordb.faiss_service import FAISSService
from backend.database.db_manager import DatabaseManager


class RetrieverService:
    """
    Handles semantic retrieval from a conversation's FAISS index.
    """

    def __init__(self, conversation_id: int):

        self.faiss = FAISSService()
        self.faiss.load(conversation_id)
        self.db = DatabaseManager()
        self.conversation_id = conversation_id

    def get_retriever(
        self,
        k: int = 8,
    ) -> VectorStoreRetriever:

        return self.faiss.as_retriever(k)

    def retrieve(
    self,
    query: str,
    k: int = 4,
) -> list[Document]:

        semantic_docs = self.faiss.similarity_search(
        query=query,
        k=k,
    )

        keyword_messages = self.keyword_search(
        query=query,
        limit=3,
    )

        keyword_docs = []

        for message in keyword_messages:

            keyword_docs.append(
            Document(
                page_content=(
                    f"{message.sender}: "
                    f"{message.message}"
                ),
                metadata={
                    "source": "keyword",
                    "timestamp": str(
                        message.timestamp
                    ),
                },
            )
        )

        unique = {}

        for doc in semantic_docs + keyword_docs:

            unique[doc.page_content] = doc

        return list(unique.values())
    def keyword_search(
    self,
    query: str,
    limit: int = 5,
):
        

        stop_words = {
        "who", "what", "where", "when",
        "why", "how", "is", "are",
        "was", "were", "the", "a",
        "an", "did", "do", "does",
        "whose", "which", "tell",
        "me", "about", "on", "in",
        "of", "to", "for"
    }

        keywords = [
        word.lower()
        for word in query.split()
        if word.lower() not in stop_words
    ]

        return self.db.search_messages_by_keyword(
        conversation_id=self.conversation_id,
        keywords=keywords,
        limit=limit,
    )