"""Message handler for agent communication."""

import json
from typing import Optional
from pydantic import BaseModel, Field
from google.genai import types

from .config import APP_NAME, DEFAULT_USER_ID, DEFAULT_SESSION_ID
from .agent_factory import AgentFactory


class MessageInput(BaseModel):
    """Input model for messages."""
    message: str = Field(description="A user sent this message")


class MessageHandler:
    """Handles message processing with the agent."""

    def __init__(self, agent_factory: Optional[AgentFactory] = None):
        """Initialize the message handler.

        Args:
            agent_factory: Optional factory instance. If None, creates a new one.
        """
        self.agent_factory = agent_factory or AgentFactory()
        self.runner = self.agent_factory.runner
        self.session_service = self.agent_factory.session_service
        self.agent = self.agent_factory.agent

    async def ensure_session_exists(
        self,
        user_id: str = DEFAULT_USER_ID,
        session_id: str = DEFAULT_SESSION_ID
    ) -> None:
        """Ensure a session exists for the user."""
        try:
            current_session = await self.session_service.get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )
            if current_session is None:
                raise Exception("Session not found")
        except Exception:
            # Session doesn't exist, create it
            await self.session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )

    async def send_message(
        self,
        message: str,
        user_id: str = DEFAULT_USER_ID,
        session_id: str = DEFAULT_SESSION_ID,
        verbose: bool = True,
    ) -> str:
        """Send a message to the agent and return the response.

        Args:
            message: The message to send
            user_id: User identifier
            session_id: Session identifier  
            verbose: Whether to print debug information

        Returns:
            The agent's response
        """
        await self.ensure_session_exists(user_id, session_id)

        query_json = json.dumps({"message": message})

        if verbose:
            print(
                f"\n>>> Calling Agent: '{self.agent.name}' | Query: {query_json}")

        user_content = types.Content(
            role='user',
            parts=[types.Part(text=query_json)]
        )

        final_response_content = "No final response received."

        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_content = event.content.parts[0].text
                if verbose:
                    print(
                        f"<<< Agent '{self.agent.name}' Response: {final_response_content}")

        # Handle session state if needed
        if verbose:
            await self._print_session_state(user_id, session_id)

        return final_response_content or "No response received"

    async def _print_session_state(
        self,
        user_id: str,
        session_id: str
    ) -> None:
        """Print session state for debugging."""
        current_session = await self.session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

        if current_session and hasattr(current_session, 'state') and self.agent.output_key:
            stored_output = current_session.state.get(self.agent.output_key)
            print(f"--- Session State ['{self.agent.output_key}']: ", end="")

            try:
                if stored_output:
                    parsed_output = json.loads(stored_output)
                    print(json.dumps(parsed_output, indent=2))
            except (json.JSONDecodeError, TypeError):
                print(stored_output)
            print("-" * 30)
