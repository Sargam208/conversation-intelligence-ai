from pathlib import Path

from backend.database.db_manager import DatabaseManager
from backend.database.models import Conversation
from backend.embeddings.embedding_service import EmbeddingService
from backend.parser.whatsapp_parser import WhatsAppParser
from backend.vectordb.faiss_service import FAISSService
import hashlib

class IngestionPipeline:

    def __init__(self):

        self.parser = WhatsAppParser()
        self.db = DatabaseManager()
        self.embedding_service = EmbeddingService()
        self.faiss = FAISSService()

    def _calculate_file_hash(
    self,
    file_path: str,
) -> str:

        hasher = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(8192):

                hasher.update(chunk)

        return hasher.hexdigest()
    

    def ingest(self, file_path: str):

        file_hash = self._calculate_file_hash(
    file_path
)

        existing_conversation = (
    self.db.find_conversation_by_hash(
        file_hash
    )
)

        if existing_conversation is not None:


            print(
        "Conversation already exists.")

            return existing_conversation

        messages = self.parser.parse(file_path)

        conversation = Conversation(
    file_name=Path(file_path).name,
    file_hash=file_hash,
    total_messages=len(messages),
)
        

        conversation_id = self.db.create_conversation(
            conversation
        )

        self.db.insert_messages(
            conversation_id,
            messages,
        )

        chunks = self.embedding_service.create_chunks(
    messages
)

        self.faiss.build_index(chunks)
        self.faiss.save(conversation_id)

        return conversation_id

    def get_messages(
        self,
        conversation_id: int,
        start_date=None,
        end_date=None,
    ):

        if start_date and end_date:
            return self.db.get_messages_by_date_range(
                conversation_id,
                start_date,
                end_date,
            )

        return self.db.get_messages(
            conversation_id
        )

    def get_date_range(
        self,
        conversation_id: int,
    ):
        return self.db.get_date_range(
            conversation_id
        )