import json
import sqlite3
from pathlib import Path
from typing import List
from datetime import datetime, date

from backend.database.models import Conversation, Message, AIInsight
from backend.database.schema import create_tables
from backend.llm.output_models import (
    ConversationSummary,
    Decision,
    ActionItem,
)

class DatabaseManager:
    """
    Handles all SQLite database operations.
    """

    def __init__(self, db_path: str = "data/conversation.db") -> None:

        Path("data").mkdir(exist_ok=True)

        self.connection = sqlite3.connect(
            db_path,
            check_same_thread=False,
        )

        self.connection.row_factory = sqlite3.Row

        create_tables(self.connection)

    # ---------------------------------------------------------
    # Conversation
    # ---------------------------------------------------------

    def create_conversation(
        self,
        conversation: Conversation,
    ) -> int:

        cursor = self.connection.cursor()

        cursor.execute(
    """
    INSERT INTO conversations
    (
        file_name,
        file_hash,
        uploaded_at,
        total_messages
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        conversation.file_name,
        conversation.file_hash,
        conversation.uploaded_at.isoformat(),
        conversation.total_messages,
    ),
)

        self.connection.commit()

        return cursor.lastrowid
    
    def find_conversation_by_hash(
    self,
    file_hash: str,
):
        

        cursor = self.connection.cursor()

        cursor.execute(
        """
        SELECT id
        FROM conversations
        WHERE file_hash = ?
        """,
        (file_hash,),
    )

        row = cursor.fetchone()

        if row:

            return row["id"]

        return None

    # ---------------------------------------------------------
    # Messages
    # ---------------------------------------------------------
    def conversation_exists(
    self,
    file_hash: str,
) -> bool:

        return (
        self.find_conversation_by_hash(
            file_hash
        )
        is not None
    )
    
    def insert_messages(
        self,
        conversation_id: int,
        messages: List[Message],
    ) -> None:

        cursor = self.connection.cursor()

        cursor.executemany(
            """
            INSERT INTO messages
            (conversation_id, sender, message, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    conversation_id,
                    msg.sender,
                    msg.message,
                    msg.timestamp.isoformat(),
                )
                for msg in messages
            ],
        )

        self.connection.commit()

    def get_messages(
        self,
        conversation_id: int,
    ) -> List[Message]:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT sender, message, timestamp
            FROM messages
            WHERE conversation_id=?
            ORDER BY timestamp
            """,
            (conversation_id,),
        )

        rows = cursor.fetchall()

        messages = []

        for row in rows:

            messages.append(
                Message(
                    sender=row["sender"],
                    message=row["message"],
                    timestamp=datetime.fromisoformat(
                        row["timestamp"]
                    ),
                )
            )

        return messages

    def get_messages_by_date_range(
        self,
        conversation_id: int,
        start_date: date,
        end_date: date,
    ) -> List[Message]:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT sender, message, timestamp
            FROM messages
            WHERE conversation_id=?
            AND DATE(timestamp)
            BETWEEN DATE(?) AND DATE(?)
            ORDER BY timestamp
            """,
            (
                conversation_id,
                start_date.isoformat(),
                end_date.isoformat(),
            ),
        )

        rows = cursor.fetchall()

        messages = []

        for row in rows:

            messages.append(
                Message(
                    sender=row["sender"],
                    message=row["message"],
                    timestamp=datetime.fromisoformat(
                        row["timestamp"]
                    ),
                )
            )

        return messages
    
    def search_messages_by_keyword(
    self,
    conversation_id: int,
    keywords: List[str],
    limit: int = 10,
) -> List[Message]:

        if not keywords:
            return []

        cursor = self.connection.cursor()

        conditions = " OR ".join(
        [
            "LOWER(message) LIKE LOWER(?)"
            for _ in keywords
        ]
    )

        query = f"""
    SELECT sender, message, timestamp
    FROM messages
    WHERE conversation_id = ?
    AND ({conditions})
    ORDER BY timestamp
    LIMIT ?
    """

        params = (
        [conversation_id]
        + [f"%{word}%" for word in keywords]
        + [limit]
    )

        cursor.execute(query, params)

        rows = cursor.fetchall()

        messages = []

        for row in rows:

            messages.append(
            Message(
                sender=row["sender"],
                message=row["message"],
                timestamp=datetime.fromisoformat(
                    row["timestamp"]
                ),
            )
        )

        return messages
    


    def get_date_range(
        self,
        conversation_id: int,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                MIN(DATE(timestamp)) AS min_date,
                MAX(DATE(timestamp)) AS max_date
            FROM messages
            WHERE conversation_id=?
            """,
            (conversation_id,),
        )

        row = cursor.fetchone()

        min_date = datetime.strptime(
            row["min_date"],
            "%Y-%m-%d",
        ).date()

        max_date = datetime.strptime(
            row["max_date"],
            "%Y-%m-%d",
        ).date()

        return min_date, max_date

    # ---------------------------------------------------------
    # AI Insights
    # ---------------------------------------------------------

    def save_ai_insights(
    self,
    conversation_id: int,
    insights,
) -> None:

        cursor = self.connection.cursor()

        cursor.execute(
        """
        INSERT OR REPLACE INTO ai_insights
        (
            conversation_id,
            executive_summary,
            key_discussion_points,
            important_decisions,
            action_items,
            deadlines
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            conversation_id,
            insights.executive_summary,
            json.dumps(insights.key_discussion_points),
            json.dumps(
                [
                    d.model_dump()
                    for d in insights.important_decisions
                ]
            ),
            json.dumps(
                [
                    a.model_dump()
                    for a in insights.action_items
                ]
            ),
            json.dumps(insights.deadlines),
        ),
    )

        self.connection.commit()
    def get_ai_insights(
    self,
    conversation_id: int,
):
        

        cursor = self.connection.cursor()

        cursor.execute(
        """
        SELECT *
        FROM ai_insights
        WHERE conversation_id = ?
        """,
        (conversation_id,),
    )

        row = cursor.fetchone()

        if row is None:
            return None

        return ConversationSummary(

        executive_summary=row["executive_summary"],

        key_discussion_points=json.loads(
            row["key_discussion_points"]
        ),

        important_decisions=[
            Decision(**d)
            for d in json.loads(
                row["important_decisions"]
            )
        ],

        action_items=[
            ActionItem(**a)
            for a in json.loads(
                row["action_items"]
            )
        ],

        deadlines=json.loads(
            row["deadlines"]
        ),
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def get_connection(self):

        return self.connection

    def close(self):

        self.connection.close()