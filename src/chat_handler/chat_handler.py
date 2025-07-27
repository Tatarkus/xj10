"""Chat handler - Interface between CLI and Agent."""

import asyncio
from agent.agent_factory import AgentFactory
from agent.message_handler import MessageHandler


class ChatHandler:
    """Handles chat communication with the agent."""

    def __init__(self) -> None:
        """Initialize the chat handler."""
        self.agent_factory = AgentFactory()
        self.message_handler = MessageHandler(self.agent_factory)
        self._running = False

    async def send_message_async(self, message: str) -> str:
        """Send a message to the agent asynchronously.

        Args:
            message: The user's message to send to the agent

        Returns:
            The agent's response as a string
        """
        try:
            response = await self.message_handler.send_message(
                message,
                verbose=False  # CLI will handle its own formatting
            )
            return str(response)
        except Exception as e:
            return f"[Agent Error] {e}"

    def send_message_to_agent(self, message: str) -> str:
        """Send a message to the agent and get the response (synchronous wrapper).

        Args:
            message: The user's message to send to the agent

        Returns:
            The agent's response as a string
        """
        try:
            response = asyncio.run(self.send_message_async(message))
            return response
        except Exception as e:
            return f"[Agent Error] {e}"

    def start(self) -> None:
        """Start the chat handler."""
        self._running = True

    def stop(self) -> None:
        """Stop the chat handler."""
        self._running = False

    @property
    def is_running(self) -> bool:
        """Check if the chat handler is running."""
        return self._running

    @property
    def agent_name(self) -> str:
        """Get the agent's name."""
        return self.agent_factory.agent.name
