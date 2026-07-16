from langchain_core.output_parsers import StrOutputParser

from backend.llm.llm_service import LLMService
from backend.llm.prompts import QUESTION_PROMPT
from backend.rag.retriever import RetrieverService


class qa_agent:

    def __init__(self, conversation_id: int):

        self.retriever = RetrieverService(
            conversation_id
        )

        self.llm = LLMService().get_llm()

        self.chain = (
            QUESTION_PROMPT
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str):

        docs = self.retriever.retrieve(
        query=question,
        k=1,
    )

        context = "\n\n".join(
    f"Chunk {i+1}:\n{doc.page_content}"
    for i, doc in enumerate(docs)
)
        print("=" * 80)
        print("Retrieved Docs:", len(docs))

        for i, doc in enumerate(docs):
            print(f"Doc {i+1} characters: {len(doc.page_content)}")

        print("Context characters:", len(context))
        print("=" * 80)

        answer = self.chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )
        

        return answer
    
