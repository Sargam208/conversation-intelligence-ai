import re
from datetime import datetime
from typing import List

from backend.database.models import Message
from backend.parser.base_parser import BaseParser


class WhatsAppParser(BaseParser):
    """
    Parses exported WhatsApp chat (.txt) into structured Message objects.
    """

    # Supports formats like:
    # 03/07/24, 10:15 AM - Rahul: Hello
    # 03/07/2024, 10:15 pm - Rahul: Hello
    MESSAGE_PATTERN = re.compile(
        r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s"
        r"(\d{1,2}:\d{2}\s?[APap][Mm])\s-\s"
        r"([^:]+):\s(.*)$"
    )

    SYSTEM_MESSAGE_PATTERN = re.compile(
        r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s"
        r"(\d{1,2}:\d{2}\s?[APap][Mm])\s-\s(.*)$"
    )

    def parse(self, file_path: str) -> List[Message]:

        messages: List[Message] = []

        current_sender = None
        current_time = None
        current_message = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:

                line = line.rstrip()

                match = self.MESSAGE_PATTERN.match(line)

                if match:

                    if current_sender:
                        messages.append(
                            Message(
                                sender=current_sender,
                                message="\n".join(current_message).strip(),
                                timestamp=current_time,
                            )
                        )

                    date_str, time_str, sender, message = match.groups()

                    timestamp = self._parse_datetime(date_str, time_str)

                    current_sender = sender.strip()
                    current_time = timestamp
                    current_message = [message]

                    continue

                system_match = self.SYSTEM_MESSAGE_PATTERN.match(line)

                if system_match:
                    continue

                if current_sender:
                    current_message.append(line)

        if current_sender:
            messages.append(
                Message(
                    sender=current_sender,
                    message="\n".join(current_message).strip(),
                    timestamp=current_time,
                )
            )

        return messages

    @staticmethod
    def _parse_datetime(date_str: str, time_str: str) -> datetime:

        formats = [
            "%d/%m/%y %I:%M %p",
            "%d/%m/%Y %I:%M %p",
            "%m/%d/%y %I:%M %p",
            "%m/%d/%Y %I:%M %p",
        ]

        datetime_str = f"{date_str} {time_str.upper()}"

        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unsupported date format: {datetime_str}")