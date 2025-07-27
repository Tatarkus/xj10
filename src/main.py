from cli_app.cli_app import XJ10CLI


def main() -> None:
    """Main function to run the CLI application."""
    cli = XJ10CLI()
    cli.run()

if __name__ == "__main__":
    main()