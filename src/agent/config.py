"""Agent configuration settings."""

# Model configuration
AGENT_MODEL = "ollama/gemma3"
OLLAMA_API_BASE = "http://host.docker.internal:11434"

# Agent settings
AGENT_NAME = "XJ10"
AGENT_DESCRIPTION = "Agent to answer questions about Music and Music genres."
AGENT_INSTRUCTION = (
    "You are a helpful agent super knowledgable about Music and Music genres. " \
    " Use KAOMOJIS such as (｡♥‿♥｡), (≧◡≦), (✿◠‿◠), (｡♥‿♥｡), to show friendliness " \
)

# Session configuration
APP_NAME = "XJ10"
DEFAULT_USER_ID = "Roboto"
DEFAULT_SESSION_ID = "roboto_session"
