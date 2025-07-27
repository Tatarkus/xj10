"""Agent factory for creating and configuring the XJ10 agent."""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService

from .config import (
    AGENT_MODEL,
    OLLAMA_API_BASE,
    AGENT_NAME,
    AGENT_DESCRIPTION,
    AGENT_INSTRUCTION,
    APP_NAME,
)


class AgentFactory:
    """Factory class for creating and managing the XJ10 agent."""

    def __init__(self):
        self.session_service = InMemorySessionService()
        self._agent = None
        self._runner = None

    def create_agent(self) -> Agent:
        """Create and configure the XJ10 agent."""
        if self._agent is None:
            self._agent = Agent(
                name=AGENT_NAME,
                model=LiteLlm(
                    model=AGENT_MODEL,
                    api_base=OLLAMA_API_BASE,
                ),
                description=AGENT_DESCRIPTION,
                instruction=AGENT_INSTRUCTION,
                tools=[],
            )
        return self._agent

    def create_runner(self) -> Runner:
        """Create a runner for the agent."""
        if self._runner is None:
            agent = self.create_agent()
            self._runner = Runner(
                agent=agent,
                app_name=APP_NAME,
                session_service=self.session_service,
            )
        return self._runner

    @property
    def agent(self) -> Agent:
        """Get the agent instance."""
        return self.create_agent()

    @property
    def runner(self) -> Runner:
        """Get the runner instance."""
        return self.create_runner()
