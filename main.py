#!/usr/bin/env python3
"""
CLI interface for the AI Agent application.
"""
import argparse
import sys
import os
from datetime import datetime

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better terminal output: pip install rich")

from src.agent import Agent
from src.tools import CalculatorTool, WeatherTool, WebSearchTool


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Free AI Agent - Chat with free AI models"
    )
    parser.add_argument(
        '--provider',
        type=str,
        default='ollama',
        choices=['ollama', 'huggingface', 'openai'],
        help='Model provider (default: ollama)'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Model name (default: llama3 for ollama)'
    )
    parser.add_argument(
        '--no-tools',
        action='store_true',
        help='Disable tools'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key for cloud providers'
    )
    parser.add_argument(
        '--load',
        type=str,
        help='Load conversation from file'
    )
    
    args = parser.parse_args()
    
    # Initialize console
    if RICH_AVAILABLE:
        console = Console()
    else:
        console = None
    
    # Determine model name
    model_name = args.model
    if not model_name:
        if args.provider == 'ollama':
            model_name = 'llama3'
        elif args.provider == 'huggingface':
            model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
        else:
            model_name = 'gpt-3.5-turbo'
    
    # Initialize tools
    tools = None if args.no_tools else [
        CalculatorTool(),
        WeatherTool(),
        WebSearchTool()
    ]
    
    # Print welcome message
    print_header(console, args.provider, model_name, tools)
    
    # Create agent
    try:
        kwargs = {}
        if args.api_key:
            kwargs['api_key'] = args.api_key
        
        agent = Agent(
            provider=args.provider,
            model=model_name,
            tools=tools,
            **kwargs
        )
        
        # Check if provider is available
        if not agent.provider.is_available():
            print(f"\n⚠️  Warning: {args.provider} provider may not be properly configured.")
            if args.provider == 'ollama':
                print("   Make sure Ollama is installed and running: https://ollama.ai")
                print(f"   Try: ollama pull {model_name}")
            elif args.provider == 'huggingface':
                print("   Make sure you have a valid Hugging Face API key.")
            print()
        
        # Load conversation if specified
        if args.load:
            agent.load_conversation(args.load)
            print(f"✓ Loaded conversation from {args.load}\n")
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        sys.exit(1)
    
    # Start chat loop
    print("Type your message and press Enter. Commands:")
    print("  /clear  - Clear conversation history")
    print("  /save   - Save conversation")
    print("  /info   - Show agent info")
    print("  /exit   - Exit the application")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                if user_input == '/exit':
                    print("Goodbye! 👋")
                    break
                elif user_input == '/clear':
                    agent.clear_history()
                    print("✓ Conversation history cleared.\n")
                    continue
                elif user_input.startswith('/save'):
                    filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    os.makedirs('conversations', exist_ok=True)
                    filepath = os.path.join('conversations', filename)
                    agent.save_conversation(filepath)
                    print(f"✓ Conversation saved to {filepath}\n")
                    continue
                elif user_input == '/info':
                    info = agent.get_info()
                    print("\n📊 Agent Information:")
                    print(f"   Provider: {info['provider']}")
                    print(f"   Model: {info['model']}")
                    print(f"   Tools: {', '.join(info['tools']) if info['tools'] else 'None'}")
                    print(f"   Messages: {info['conversation_length']}\n")
                    continue
                else:
                    print(f"Unknown command: {user_input}\n")
                    continue
            
            # Get response from agent
            print("Assistant: ", end='', flush=True)
            response = agent.chat(user_input)
            
            if console and RICH_AVAILABLE:
                console.print(Markdown(response))
            else:
                print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def print_header(console, provider: str, model: str, tools):
    """Print application header."""
    header = f"""
╔══════════════════════════════════════════════════════════════╗
║           🤖 Free AI Agent Model App                         ║
║                                                              ║
║  Provider: {provider:<15}  Model: {model:<25}  ║
║  Tools: {len(tools) if tools else 0} enabled                                           ║
╚══════════════════════════════════════════════════════════════╝
"""
    if console and RICH_AVAILABLE:
        console.print(header, style="bold blue")
    else:
        print(header)


if __name__ == "__main__":
    main()
