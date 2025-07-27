from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Import the chat handler as the interface to the agent
from chat_handler.chat_handler import ChatHandler


class XJ10CLI:
    """A simple terminal-based chat application."""

    def __init__(self) -> None:
        """Initialize the app."""
        self.console = Console()
        # Initialize the chat handler as the interface to the agent
        self.chat_handler = ChatHandler()
        self.chat_handler.start()

    def print_welcome(self) -> None:
        """Print welcome message."""
        agent_name = self.chat_handler.agent_name
        welcome_text = Text(f"🤖 {agent_name} Terminal Chat", style="bold blue")
        self.console.print(Panel(welcome_text, title="Welcome"))

        self.console.print(
            "Type your messages and press Enter. Type 'quit' or 'exit' to stop.")
        self.console.print(
            "Commands: 'history' - show recent conversation\n")

    def print_message(self, message: str, sender: str = "You") -> None:
        """Print a formatted message."""
        if sender == "You":
            user_text = Text(f"You: {message}", style="green")
            self.console.print(user_text)
        elif sender == "AI":
            # Format AI responses as markdown for better readability
            self.console.print(Text("AI:", style="blue bold"), end=" ")
            if message.strip():
                try:
                    # Try to render as markdown
                    markdown = Markdown(message)
                    self.console.print(markdown)
                except Exception:
                    # Fallback to plain text
                    self.console.print(Text(message, style="blue"))
            else:
                self.console.print(Text("(no response)", style="dim"))
        else:
            # System messages
            system_text = Text(f"[{sender}] {message}", style="yellow")
            self.console.print(system_text)

        self.console.print()  # Add a blank line

    def run(self) -> None:
        """Run the chat application."""
        self.print_welcome()

        try:
            while True:
                # Get user input
                user_input = Prompt.ask(
                    "[green]You[/green]", console=self.console)

                if user_input.lower() in ['quit', 'exit', 'q']:
                    self.console.print(Text("Goodbye! 👋", style="bold yellow"))
                    break

                if not user_input.strip():
                    continue

                # Handle special commands
                if user_input.lower() == 'history':
                    self.print_message(
                        "History feature not yet implemented", "System")
                    continue

                # Send message to agent
                try:
                    # self.print_message(user_input, "You")
                    response = self.chat_handler.send_message_to_agent(
                        user_input)
                    self.print_message(response, "AI")
                except Exception as e:
                    self.print_message(f"Error: {str(e)}", "System")

        except KeyboardInterrupt:
            self.console.print(Text("\nGoodbye! 👋", style="bold yellow"))
            self.chat_handler.stop()
        except EOFError:
            self.console.print(Text("\nGoodbye! 👋", style="bold yellow"))
            self.chat_handler.stop()
