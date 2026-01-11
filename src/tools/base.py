"""
Base tool interface for AI agent.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """Abstract base class for agent tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Dictionary with execution results
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the tool's schema for the AI model.
        
        Returns:
            Dictionary describing the tool and its parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_parameters()
        }
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Define the parameters this tool accepts.
        Should be overridden by subclasses.
        """
        return {}
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
