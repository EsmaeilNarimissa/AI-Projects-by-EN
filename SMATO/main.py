"""Main entry point for the agent system."""

import asyncio
import argparse
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt

from core.agent import Agent
from core.memory import MemoryConfig
from config.api_keys import validate_api_keys
from config import SYSTEM_MESSAGES

# Set up rich console
console = Console()

# Set up logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rich")

class CLIConfig(BaseModel):
    """Configuration for the CLI interface."""
    system_message: Optional[str] = Field(
        default=SYSTEM_MESSAGES["default"],
        description="System message to initialize the agent"
    )
    max_history: int = Field(
        default=100,
        description="Maximum number of messages to keep in history"
    )
    show_thinking: bool = Field(
        default=True,
        description="Show agent's thinking process"
    )

class AgentCLI:
    """Command-line interface for the agent system."""
    
    def __init__(self, config: Optional[CLIConfig] = None) -> None:
        """Initialize the CLI interface."""
        self.config = config or CLIConfig()
        self.console = Console()
        
        # Initialize agent with memory configuration
        memory_config = MemoryConfig(
            max_messages=self.config.max_history,
            system_message=self.config.system_message
        )
        
        self.agent = Agent(
            memory_config=memory_config,
            show_thinking=self.config.show_thinking
        )
        
        logger.info("Agent initialized successfully")
    
    def print_welcome(self) -> None:
        """Print welcome message and available commands."""
        self.console.print("\n[bold green]Welcome to the Agent System![/bold green]")
        self.console.print("\nAvailable commands:")
        self.console.print("  [blue]/exit[/blue] - End the session")
        self.console.print("  [blue]/clear[/blue] - Clear conversation history")
        self.console.print("  [blue]/history[/blue] - View conversation history")
        self.console.print("  [blue]/help[/blue] - Show this help message")
        self.console.print("  [blue]/debug[/blue] - Toggle debug mode")
        self.console.print("\nStart chatting or type /help for more information.\n")
    
    async def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if should continue session."""
        command = command.lower()
        
        if command == 'exit':
            self.console.print("[yellow]Goodbye![/yellow]")
            return False
            
        elif command == 'clear':
            self.agent.clear_history()
            self.console.print("[green]Conversation history cleared.[/green]")
            
        elif command == 'history':
            history = self.agent.get_conversation_history()
            if not history:
                self.console.print("[yellow]No conversation history.[/yellow]")
            else:
                self.console.print("\n[bold]Conversation History:[/bold]")
                for msg in history:
                    self.console.print(
                        f"[blue]{msg['role']}[/blue]: {msg['content']}"
                    )
            
        elif command == 'help':
            self.print_welcome()
            
        elif command == 'debug':
            self.config.show_thinking = not self.config.show_thinking
            status = "enabled" if self.config.show_thinking else "disabled"
            self.console.print(f"[green]Debug mode {status}.[/green]")
            
        else:
            self.console.print("[red]Unknown command. Type '/help' for available commands.[/red]")
        
        return True
    
    async def interactive_session(self) -> None:
        """Run an interactive session with the agent."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                # Check if it's a command
                if user_input.startswith('/'):
                    command = user_input[1:]
                    should_continue = await self.handle_command(command)
                    if not should_continue:
                        break
                    continue
                
                # Process message
                self.console.print("[dim]Thinking...[/dim]")
                response = await self.agent.process_message(user_input)
                
                # Display response
                self.console.print("\n[bold green]Assistant[/bold green]:", response)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session interrupted. Goodbye![/yellow]")
                break
                
            except Exception as e:
                logger.exception("Fatal error")
                self.console.print(f"\n[red]Fatal error: {str(e)}[/red]")
                break

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the agent system")
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )
    parser.add_argument(
        "--system-message",
        type=str,
        help="Custom system message for the agent"
    )
    return parser.parse_args()

async def main() -> None:
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create CLI config
        config = CLIConfig(
            show_thinking=not args.no_debug,
            system_message=args.system_message
        )
        
        # Validate API keys
        validate_api_keys()
        
        # Run CLI
        cli = AgentCLI(config)
        await cli.interactive_session()
        
    except Exception as e:
        logger.exception("Fatal error")
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program interrupted. Goodbye![/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unhandled error: {str(e)}[/red]")
        raise