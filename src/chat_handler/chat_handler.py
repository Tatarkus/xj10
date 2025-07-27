from typing import Any
import asyncio
from agent import xj10_agent


class ChatHandler:
    def __init__(self) -> None:
        """Initialize the chat handler."""
        pass

    def send_message_to_agent(self, message: str) -> str:
        """Send a message to the agent and get the response.

        Args:
            message: The user's message to send to the agent

        Returns:
            The agent's response as a string
        """
        try:
            response: Any = asyncio.run(
                xj10_agent.call_agent_and_print(message=message))
            return str(response)
        except Exception as e:
            return f"[Agent Error] {e}"

    def stop(self) -> None:
        """Stop the chat handler (no-op for synchronous implementation)."""
        pass
