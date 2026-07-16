from abc import ABC, abstractmethod
from typing import List

from backend.database.models import Message


class BaseParser(ABC):
    """
    Base class for all conversation parsers.
    """

    @abstractmethod
    def parse(self, file_path: str) -> List[Message]:
        """
        Parse a conversation file and return a list of Message objects.
        """
        pass