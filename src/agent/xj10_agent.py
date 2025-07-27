"""XJ10 Agent - Clean modular implementation using separate modules."""

from .agent_factory import AgentFactory
from .message_handler import MessageHandler


# Initialize the agent components
agent_factory = AgentFactory()
message_handler = MessageHandler(agent_factory)

# Expose the main interface
agent = agent_factory.agent
runner = agent_factory.runner

async def call_agent_and_print(message: str) -> str:
    """Sends a query to the agent and prints results.

    Args:
        message: The message to send to the agent

    Returns:
        The agent's response
    """
    return await message_handler.send_message(message)


# Convenience function for non-async usage
def send_message_sync(message: str) -> str:
    """Synchronous wrapper for sending messages."""
    import asyncio
    return asyncio.run(call_agent_and_print(message))
