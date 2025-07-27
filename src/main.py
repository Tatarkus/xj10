

from cli_app.cli_app import XJ10CLI
from chat_handler import ChatHandler


def main() -> None:
    """Main function to run the CLI application with agent process."""
    chat_handler = ChatHandler()
    cli = XJ10CLI()
    cli.console.print(
        "[dim]Agent process started. Type your message and press Enter.[/dim]")

    try:
        cli.print_welcome()
        while True:
            user_input = cli.console.input("[green]You[/green]: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                chat_handler.stop()
                cli.console.print("Goodbye! 👋", style="bold yellow")
                break
            if not user_input.strip():
                continue
            response = chat_handler.send_message_to_agent(user_input)
            cli.print_message(response, sender="AI")
    except (KeyboardInterrupt, EOFError):
        chat_handler.stop()
        cli.console.print("\nGoodbye! 👋", style="bold yellow")


if __name__ == "__main__":
    main()
