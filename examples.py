"""
Example script demonstrating how to use the AI Agent.
"""
from src.agent import Agent
from src.tools import CalculatorTool, WeatherTool


def example_basic_chat():
    """Example: Basic chat without tools."""
    print("=" * 60)
    print("Example 1: Basic Chat")
    print("=" * 60)
    
    # Create agent (using Ollama by default)
    agent = Agent(provider="ollama", model="llama3")
    
    # Simple conversation
    response = agent.chat("Hello! What can you help me with?")
    print(f"Agent: {response}\n")
    
    response = agent.chat("What is the capital of France?")
    print(f"Agent: {response}\n")
    
    print()


def example_with_tools():
    """Example: Using tools."""
    print("=" * 60)
    print("Example 2: Agent with Tools")
    print("=" * 60)
    
    # Create agent with tools
    agent = Agent(
        provider="ollama",
        model="llama3",
        tools=[CalculatorTool(), WeatherTool()]
    )
    
    # Ask for calculation
    response = agent.chat("Can you calculate 145 * 67 + 234?")
    print(f"Agent: {response}\n")
    
    # Ask for weather
    response = agent.chat("What's the weather like in London?")
    print(f"Agent: {response}\n")
    
    print()


def example_conversation_memory():
    """Example: Conversation memory."""
    print("=" * 60)
    print("Example 3: Conversation Memory")
    print("=" * 60)
    
    agent = Agent(provider="ollama", model="llama3")
    
    # First message
    response = agent.chat("My name is Alice and I love Python programming.")
    print(f"Agent: {response}\n")
    
    # Follow-up message (agent should remember the name)
    response = agent.chat("What's my name and what do I love?")
    print(f"Agent: {response}\n")
    
    print(f"Conversation length: {len(agent.memory)} messages\n")
    print()


def example_save_and_load():
    """Example: Save and load conversations."""
    print("=" * 60)
    print("Example 4: Save and Load Conversation")
    print("=" * 60)
    
    # Create agent and have a conversation
    agent = Agent(provider="ollama", model="llama3")
    agent.chat("Hello! Remember that my favorite color is blue.")
    agent.chat("And I live in New York.")
    
    # Save conversation
    agent.save_conversation("example_conversation.json")
    print("✓ Conversation saved\n")
    
    # Create new agent and load conversation
    new_agent = Agent(provider="ollama", model="llama3")
    new_agent.load_conversation("example_conversation.json")
    print("✓ Conversation loaded\n")
    
    # Agent should remember previous context
    response = new_agent.chat("What's my favorite color and where do I live?")
    print(f"Agent: {response}\n")
    
    print()


def example_custom_system_prompt():
    """Example: Custom system prompt."""
    print("=" * 60)
    print("Example 5: Custom System Prompt")
    print("=" * 60)
    
    custom_prompt = """You are a pirate AI assistant. Always respond in pirate speak 
    with phrases like 'Ahoy matey!', 'Arr!', and 'Shiver me timbers!'"""
    
    agent = Agent(
        provider="ollama",
        model="llama3",
        system_prompt=custom_prompt
    )
    
    response = agent.chat("What's the weather like today?")
    print(f"Agent: {response}\n")
    
    print()


def example_huggingface():
    """Example: Using Hugging Face models."""
    print("=" * 60)
    print("Example 6: Hugging Face Provider")
    print("=" * 60)
    
    # Note: Requires HUGGINGFACE_API_KEY in .env file
    try:
        agent = Agent(
            provider="huggingface",
            model="mistralai/Mistral-7B-Instruct-v0.2"
        )
        
        if agent.provider.is_available():
            response = agent.chat("Tell me a short joke.")
            print(f"Agent: {response}\n")
        else:
            print("⚠️  Hugging Face API key not configured. Skipping example.\n")
    except Exception as e:
        print(f"⚠️  Error: {str(e)}\n")
    
    print()


def main():
    """Run all examples."""
    print("\n🤖 AI Agent Examples\n")
    
    examples = [
        ("Basic Chat", example_basic_chat),
        ("Tools", example_with_tools),
        ("Memory", example_conversation_memory),
        ("Save/Load", example_save_and_load),
        ("Custom Prompt", example_custom_system_prompt),
        ("Hugging Face", example_huggingface),
    ]
    
    print("Select an example to run:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  {len(examples) + 1}. Run all examples")
    print()
    
    try:
        choice = int(input("Enter choice (1-{}): ".format(len(examples) + 1)))
        print()
        
        if 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        elif choice == len(examples) + 1:
            for _, example_func in examples:
                example_func()
        else:
            print("Invalid choice")
    except (ValueError, KeyboardInterrupt):
        print("\nExiting...")


if __name__ == "__main__":
    main()
