"""
Web search tool for searching the internet.
"""
from typing import Dict, Any
from .base import BaseTool


class WebSearchTool(BaseTool):
    """Tool for web search (mock implementation)."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Searches the web for information on a given query."
        )
    
    def execute(self, query: str, num_results: int = 3) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        # This is a mock implementation
        # For real implementation, you could use:
        # - DuckDuckGo API (free, no API key needed)
        # - SerpApi (has free tier)
        # - Google Custom Search API (limited free tier)
        
        return {
            "success": True,
            "query": query,
            "num_results": num_results,
            "results": [
                {
                    "title": f"Result 1 for '{query}'",
                    "url": "https://example.com/result1",
                    "snippet": "This is a mock search result. Integrate a real search API for production use."
                },
                {
                    "title": f"Result 2 for '{query}'",
                    "url": "https://example.com/result2",
                    "snippet": "Another mock result demonstrating the tool interface."
                }
            ],
            "note": "This is mock data. Integrate a real search API like DuckDuckGo or SerpApi for production use."
        }
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of search results to return (default: 3)"
                }
            },
            "required": ["query"]
        }
