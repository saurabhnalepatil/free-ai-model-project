"""Main package initialization."""
from .agent import Agent
from .models import BaseModelProvider, OllamaProvider, HuggingFaceProvider, OpenAIProvider
from .tools import BaseTool, CalculatorTool, WeatherTool, WebSearchTool

__version__ = "1.0.0"
__all__ = [
    'Agent',
    'BaseModelProvider',
    'OllamaProvider',
    'HuggingFaceProvider',
    'OpenAIProvider',
    'BaseTool',
    'CalculatorTool',
    'WeatherTool',
    'WebSearchTool'
]
