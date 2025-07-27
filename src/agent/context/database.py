import sqlite3
from typing import List, Dict
from datetime import datetime


class ConversationDB:
    """SQLite database handler for conversation context and memory."""

    def __init__(self, db_path: str = "conversation.db") -> None:
        """Initialize the database connection."""
        self.db_path = db_path
        self.init_database()

    def init_database(self) -> None:
        """Initialize the database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)

            conn.commit()

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)",
                (timestamp, role, content)
            )
            conn.commit()

    def get_recent_messages(self, limit: int = 20) -> List[Dict[str, str]]:
        """Get recent conversation messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content FROM conversations 
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))

            messages = []
            for row in reversed(cursor.fetchall()):
                messages.append({"role": row[0], "content": row[1]})

            return messages

    def build_context_prompt(self, current_message: str) -> str:
        """Build a context-aware prompt with conversation history."""
        context_parts: List[str] = []

        # Add recent conversation history
        recent_messages = self.get_recent_messages(20)
        if recent_messages:
            context_parts.append("Previous conversation history:")
            for msg in recent_messages:
                role = "User" if msg['role'] == "user" else "Assistant"
                context_parts.append(f"{role}: {msg['content']}")

        # Add instruction for the LLM to maintain context naturally
        context_parts.append(
            "\nPlease respond to the current message while being aware of the conversation history above. "
            "Naturally remember and reference relevant information from our previous exchanges when appropriate."
        )

        # Add current message
        context_parts.append(f"\nCurrent message: {current_message}")

        return "\n".join(context_parts)
