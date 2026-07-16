from langchain_core.output_parsers import PydanticOutputParser

from backend.database.models import Message
from backend.llm.llm_service import LLMService
from backend.llm.output_models import ConversationSummary
from backend.llm.prompts import SUMMARY_PROMPT


class ChunkAnalysisAgent:
    """
    Analyzes a single conversation chunk and returns
    a structured ConversationSummary.
    """

    def __init__(self):

        self.llm = LLMService().get_llm()

        self.parser = PydanticOutputParser(
            pydantic_object=ConversationSummary
        )

        self.chain = (
            SUMMARY_PROMPT
            | self.llm
            | self.parser
        )

    def analyze(
        self,
        messages: list[Message],
    ) -> ConversationSummary:

        conversation = "\n".join(
            f"{msg.sender}: {msg.message}"
            for msg in messages
        )

        return self.chain.invoke(
            {
                "conversation": conversation,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )