import sqlite3


def create_tables(connection: sqlite3.Connection) -> None:
    """
    Create all required database tables.
    """

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        file_hash TEXT UNIQUE NOT NULL,
        uploaded_at TIMESTAMP NOT NULL,
        total_messages INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_insights (
    conversation_id INTEGER PRIMARY KEY,

    executive_summary TEXT,

    key_discussion_points TEXT,

    important_decisions TEXT,

    action_items TEXT,

    deadlines TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
    REFERENCES conversations(id)
)
""")

    connection.commit()