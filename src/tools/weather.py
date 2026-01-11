"""
Weather tool for getting weather information.
"""
from typing import Dict, Any
from .base import BaseTool


class WeatherTool(BaseTool):
    """Tool for getting weather information (mock implementation)."""
    
    def __init__(self):
        super().__init__(
            name="weather",
            description="Gets current weather information for a location."
        )
    
    def execute(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location.
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with weather information
        """
        # This is a mock implementation
        # In a real app, you'd call a weather API like OpenWeatherMap (free tier available)
        
        mock_weather = {
            "new york": {"temp": 72, "condition": "Sunny", "humidity": 45},
            "london": {"temp": 62, "condition": "Cloudy", "humidity": 70},
            "tokyo": {"temp": 78, "condition": "Clear", "humidity": 55},
            "paris": {"temp": 68, "condition": "Partly Cloudy", "humidity": 60},
            "sydney": {"temp": 75, "condition": "Sunny", "humidity": 50},
        }
        
        location_lower = location.lower()
        if location_lower in mock_weather:
            weather = mock_weather[location_lower]
            return {
                "success": True,
                "location": location,
                "temperature": weather["temp"],
                "condition": weather["condition"],
                "humidity": weather["humidity"],
                "note": "This is mock data. Integrate a real weather API for production use."
            }
        else:
            return {
                "success": False,
                "error": f"Weather data not available for {location}",
                "note": "This is a mock implementation. Use a real weather API like OpenWeatherMap."
            }
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or location to get weather for"
                }
            },
            "required": ["location"]
        }
