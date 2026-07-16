from langchain_core.output_parsers import PydanticOutputParser

from backend.llm.llm_service import LLMService
from backend.llm.output_models import ConversationSummary
from backend.llm.prompts import SUMMARY_PROMPT


class ConversationChain:

    def __init__(self):

        self.parser = PydanticOutputParser(
            pydantic_object=ConversationSummary
        )

        self.llm = LLMService().get_llm()

        self.chain = (
            SUMMARY_PROMPT
            | self.llm
            | self.parser
        )

    def invoke(self, conversation: str):

        return self.chain.invoke(
            {
                "conversation": conversation,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )