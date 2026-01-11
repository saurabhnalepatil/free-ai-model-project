"""
Memory management for conversation history.
"""
from typing import List, Dict, Optional
import json
import os
from datetime import datetime


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []
        self.metadata: Dict = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.metadata["updated_at"] = datetime.now().isoformat()
        
        # Trim history if needed
        if len(self.messages) > self.max_history * 2:  # *2 for user+assistant pairs
            self.messages = self.messages[-self.max_history * 2:]
    
    def get_messages(self, include_system: bool = True) -> List[Dict[str, str]]:
        """Get all messages in the conversation."""
        if include_system:
            return self.messages
        return [msg for msg in self.messages if msg["role"] != "system"]
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get messages formatted for model context."""
        return [{"role": msg["role"], "content": msg["content"]} 
                for msg in self.messages]
    
    def clear(self):
        """Clear conversation history."""
        self.messages = []
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def save(self, filepath: str):
        """Save conversation to a JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            "metadata": self.metadata,
            "messages": self.messages
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """Load conversation from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.metadata = data.get("metadata", {})
        self.messages = data.get("messages", [])
    
    def __len__(self):
        return len(self.messages)
    
    def __repr__(self):
        return f"ConversationMemory(messages={len(self.messages)}, max={self.max_history})"
