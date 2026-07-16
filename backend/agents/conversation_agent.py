from typing import List

from backend.database.models import Message
from backend.embeddings.embedding_service import EmbeddingService
from backend.agents.chunk_analysis_agent import ChunkAnalysisAgent
from backend.agents.summary_merger import SummaryMerger
from backend.llm.output_models import ConversationSummary


class ConversationAgent:
    """
    Generates AI insights using chunk-wise analysis.
    """

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.chunk_agent = ChunkAnalysisAgent()

        self.summary_merger = SummaryMerger()

    def analyze(
        self,
        messages: List[Message],
    ) -> ConversationSummary:

        chunks = self.embedding_service.create_chunks(
            messages
        )

        summaries = []

        for chunk in chunks:

            summary = self.chunk_agent.analyze(
                chunk.messages
            )

            summaries.append(summary)

            
        print(f"Total messages: {len(messages)}")
        print(f"Total chunks: {len(chunks)}")

        print(f"Merging {len(summaries)} chunk summaries...")

        final_summary = self.summary_merger.merge(
    summaries
)

        return final_summary
        