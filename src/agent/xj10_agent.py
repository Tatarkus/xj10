import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from pydantic import BaseModel, Field
from google.genai import types
import asyncio

import json
import requests


AGENT_MODEL = "ollama/gemma3"


class MessageInput(BaseModel):
    message: str = Field(description="An user sent this message")


def get_weather(city: str) -> dict[str, str]:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict[str, str]: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict[str, str]:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict[str, str]: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="XJ10",
    model=LiteLlm(
        model=("ollama_chat/gamma3:latest"),
    ),
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)

session_service = InMemorySessionService()

# Create a runner for EACH agent
root_runner = Runner(
    agent=root_agent,
    app_name="XJ10",
    session_service=session_service
)

session_service.create_session(
    app_name="XJ10", user_id="Roboto", session_id="roboto_session")


print("Agent initialized")
print("Agent name:", root_agent.name)


async def call_agent_and_print(message: str) -> str:
    """Sends a query to the specified agent/runner and prints results."""

    # Ensure session exists before using it
    try:
        current_session = await session_service.get_session(app_name="XJ10", user_id="Roboto", session_id="roboto_session")
        if current_session is None:
            raise Exception("Session not found")
    except Exception:
        # Session doesn't exist, create it
        await session_service.create_session(app_name="XJ10", user_id="Roboto", session_id="roboto_session")

    query_json = json.dumps({"message": message})

    print(f"\n>>> Calling Agent: '{root_agent.name}' | Query: {query_json}")

    user_content = types.Content(
        role='user', parts=[types.Part(text=query_json)])

    final_response_content = "No final response received."
    async for event in root_runner.run_async(user_id="Roboto", session_id="roboto_session", new_message=user_content):
        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text
            print(
                f"<<< Agent '{root_agent.name}' Response: {final_response_content}")

    current_session = await session_service.get_session(app_name="XJ10",
                                                        user_id="Roboto",
                                                        session_id="roboto_session")

    if current_session and hasattr(current_session, 'state') and root_agent.output_key:
        stored_output = current_session.state.get(root_agent.output_key)

        # Pretty print if the stored output looks like JSON (likely from output_schema)
        print(f"--- Session State ['{root_agent.output_key}']: ", end="")

        try:
            # Attempt to parse and pretty print if it's JSON
            if stored_output:
                parsed_output = json.loads(stored_output)
                print(json.dumps(parsed_output, indent=2))
        except (json.JSONDecodeError, TypeError):
            # Otherwise, print as string
            print(stored_output)
        print("-" * 30)

    return final_response_content or "No response received"
