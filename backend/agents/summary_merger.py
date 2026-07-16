from langchain_core.output_parsers import PydanticOutputParser

from backend.llm.llm_service import LLMService
from backend.llm.output_models import ConversationSummary
from backend.llm.prompts import MERGE_SUMMARY_PROMPT


class SummaryMerger:

    def __init__(self):

        self.llm = LLMService().get_llm()

        self.parser = PydanticOutputParser(
            pydantic_object=ConversationSummary
        )

        self.chain = (
            MERGE_SUMMARY_PROMPT
            | self.llm
            | self.parser
        )

    def merge(
        self,
        summaries: list[ConversationSummary],
    ) -> ConversationSummary:

        merged_input = "\n\n".join(
            f"Chunk {i+1}:\n{summary.model_dump_json(indent=2)}"
            for i, summary in enumerate(summaries)
        )

        return self.chain.invoke(
            {
                "summaries": merged_input,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )