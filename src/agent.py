"""
Main AI Agent class.
"""
from typing import List, Dict, Optional, Any
from .models import BaseModelProvider, OllamaProvider, HuggingFaceProvider, OpenAIProvider
from .utils.memory import ConversationMemory
from .utils.config import Config
from .tools.base import BaseTool
import re
import json


class Agent:
    """Main AI Agent with conversation management and tool support."""
    
    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3",
        tools: Optional[List[BaseTool]] = None,
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the AI Agent.
        
        Args:
            provider: Model provider ('ollama', 'huggingface', 'openai')
            model: Model name
            tools: List of tools the agent can use
            system_prompt: Custom system prompt
            **kwargs: Additional provider-specific arguments
        """
        self.provider_name = provider
        self.model_name = model
        self.tools = tools or []
        self.memory = ConversationMemory(max_history=Config.MAX_HISTORY_LENGTH)
        
        # Initialize model provider
        self.provider = self._create_provider(provider, model, **kwargs)
        
        # Set system prompt
        default_prompt = "You are a helpful AI assistant."
        if tools:
            tool_descriptions = "\n".join([
                f"- {tool.name}: {tool.description}" 
                for tool in tools
            ])
            default_prompt += f"\n\nYou have access to the following tools:\n{tool_descriptions}"
            default_prompt += "\n\nWhen you need to use a tool, respond with: TOOL_CALL: {tool_name}({parameters})"
        
        self.system_prompt = system_prompt or default_prompt
        self.memory.add_message("system", self.system_prompt)
    
    def _create_provider(self, provider: str, model: str, **kwargs) -> BaseModelProvider:
        """Create the appropriate model provider."""
        if provider == "ollama":
            base_url = kwargs.get('base_url', Config.OLLAMA_BASE_URL)
            return OllamaProvider(model, base_url=base_url)
        elif provider == "huggingface":
            api_key = kwargs.get('api_key', Config.HUGGINGFACE_API_KEY)
            return HuggingFaceProvider(model, api_key=api_key)
        elif provider == "openai":
            api_key = kwargs.get('api_key', Config.OPENAI_API_KEY)
            base_url = kwargs.get('base_url', Config.OPENAI_API_BASE)
            return OpenAIProvider(model, api_key=api_key, base_url=base_url)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def chat(self, message: str, stream: bool = False, **kwargs) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: User message
            stream: Whether to stream the response
            **kwargs: Additional generation parameters
            
        Returns:
            Agent's response
        """
        # Add user message to memory
        self.memory.add_message("user", message)
        
        # Get response from model
        messages = self.memory.get_context()
        
        if stream:
            return self._stream_response(messages, **kwargs)
        else:
            response = self.provider.generate(messages, **kwargs)
            
            # Check for tool calls
            if self.tools and "TOOL_CALL:" in response:
                response = self._handle_tool_call(response)
            
            # Add assistant response to memory
            self.memory.add_message("assistant", response)
            return response
    
    def _stream_response(self, messages: List[Dict[str, str]], **kwargs):
        """Stream the response (generator)."""
        full_response = ""
        for chunk in self.provider.stream_generate(messages, **kwargs):
            full_response += chunk
            yield chunk
        
        # Check for tool calls after streaming completes
        if self.tools and "TOOL_CALL:" in full_response:
            tool_result = self._handle_tool_call(full_response)
            yield "\n\n" + tool_result
            self.memory.add_message("assistant", full_response + "\n\n" + tool_result)
        else:
            self.memory.add_message("assistant", full_response)
    
    def _handle_tool_call(self, response: str) -> str:
        """Parse and execute tool calls from the response."""
        # Extract tool calls using regex
        pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        matches = re.findall(pattern, response)
        
        if not matches:
            return response
        
        results = []
        for tool_name, params_str in matches:
            # Find the tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if not tool:
                results.append(f"Error: Tool '{tool_name}' not found")
                continue
            
            # Parse parameters
            try:
                # Try to parse as JSON-like parameters
                params_str = params_str.strip()
                if params_str:
                    # Simple parsing for key=value pairs
                    params = {}
                    for param in params_str.split(','):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            key = key.strip().strip('"\'')
                            value = value.strip().strip('"\'')
                            params[key] = value
                else:
                    params = {}
                
                # Execute tool
                result = tool.execute(**params)
                results.append(f"Tool {tool_name} result: {json.dumps(result, indent=2)}")
            except Exception as e:
                results.append(f"Error executing {tool_name}: {str(e)}")
        
        # Return original response plus tool results
        return response + "\n\n" + "\n".join(results)
    
    def clear_history(self):
        """Clear conversation history."""
        self.memory.clear()
        self.memory.add_message("system", self.system_prompt)
    
    def save_conversation(self, filepath: str):
        """Save conversation to file."""
        self.memory.save(filepath)
    
    def load_conversation(self, filepath: str):
        """Load conversation from file."""
        self.memory.load(filepath)
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the agent."""
        return {
            "provider": self.provider_name,
            "model": self.model_name,
            "tools": [tool.name for tool in self.tools],
            "conversation_length": len(self.memory),
            "provider_info": self.provider.get_info()
        }
    
    def __repr__(self):
        return f"Agent(provider={self.provider_name}, model={self.model_name}, tools={len(self.tools)})"
