# Free AI Agent Model App

A powerful and flexible AI agent application that works with free AI models from various providers including Hugging Face, Ollama, and OpenAI-compatible APIs.

## Features

- 🤖 **Multiple Model Support**: Works with Hugging Face models, Ollama, and any OpenAI-compatible API
- 💬 **Conversation Memory**: Maintains context across multiple interactions
- 🛠️ **Tool System**: Extensible tool/function calling capability
- 🌐 **Multiple Interfaces**: CLI and Web UI (Flask-based)
- 🆓 **100% Free**: Uses only free AI models and APIs
- 📝 **Persistent Storage**: Save and load conversation histories

## Supported Model Providers

1. **Hugging Face** - Use free inference API or local models
2. **Ollama** - Run local open-source models (Llama 3, Mistral, etc.)
3. **OpenAI-compatible APIs** - Works with any compatible endpoint

## Installation

### Prerequisites

- Python 3.8+
- (Optional) Ollama installed for local models

### Setup

1. Clone this repository:
```bash
cd free-ai-model-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your API keys (if using cloud models)
```

## Usage

### CLI Interface

Run the interactive CLI:
```bash
python main.py
```

Or use it with specific models:
```bash
# Use Ollama with llama3
python main.py --provider ollama --model llama3

# Use Hugging Face
python main.py --provider huggingface --model mistralai/Mistral-7B-Instruct-v0.2
```

### Web Interface

Start the Flask web server:
```bash
python app.py
```

Then open your browser to `http://localhost:5000`

## Configuration

Edit [.env](.env) file:

```env
# Hugging Face (optional - for cloud API)
HUGGINGFACE_API_KEY=your_key_here

# Ollama settings (if running locally)
OLLAMA_BASE_URL=http://localhost:11434

# Custom OpenAI-compatible endpoint
OPENAI_API_BASE=https://your-endpoint.com/v1
OPENAI_API_KEY=your_key_here
```

## Project Structure

```
free-ai-model-project/
├── src/
│   ├── agent.py              # Core AI agent logic
│   ├── models/
│   │   ├── base.py          # Base model provider interface
│   │   ├── huggingface.py   # Hugging Face provider
│   │   ├── ollama.py        # Ollama provider
│   │   └── openai.py        # OpenAI-compatible provider
│   ├── tools/
│   │   ├── base.py          # Base tool interface
│   │   ├── calculator.py    # Example: calculator tool
│   │   ├── weather.py       # Example: weather tool
│   │   └── web_search.py    # Example: web search tool
│   └── utils/
│       ├── memory.py        # Conversation memory management
│       └── config.py        # Configuration utilities
├── main.py                   # CLI interface
├── app.py                    # Flask web interface
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment config
└── README.md                # This file
```

## Examples

### Basic Conversation

```python
from src.agent import Agent

# Create agent with Ollama
agent = Agent(provider="ollama", model="llama3")

# Chat
response = agent.chat("What is the capital of France?")
print(response)
```

### With Tools

```python
from src.agent import Agent
from src.tools.calculator import CalculatorTool

# Create agent with tools
agent = Agent(
    provider="ollama",
    model="llama3",
    tools=[CalculatorTool()]
)

# Agent can use tools
response = agent.chat("What is 45 * 67 + 123?")
print(response)
```

## Adding Custom Tools

Create a new tool by inheriting from `BaseTool`:

```python
from src.tools.base import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Description of what my tool does"
        )
    
    def execute(self, **kwargs):
        # Your tool logic here
        return {"result": "success"}
```

## Free Model Recommendations

### For Local Use (via Ollama)
- **llama3** - Best overall performance
- **mistral** - Fast and efficient
- **phi3** - Small but capable
- **codellama** - Best for code

### For Cloud Use (Hugging Face)
- **mistralai/Mistral-7B-Instruct-v0.2** - Great general model
- **meta-llama/Llama-2-7b-chat-hf** - Good conversations
- **bigcode/starcoder** - Code generation

## License

MIT License - Feel free to use for any purpose!

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.
