"""
Calculator tool for mathematical operations.
"""
from typing import Dict, Any
from .base import BaseTool


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs mathematical calculations. Supports basic arithmetic operations."
        )
    
    def execute(self, expression: str) -> Dict[str, Any]:
        """
        Execute a mathematical expression.
        
        Args:
            expression: Mathematical expression as a string (e.g., "2 + 2", "45 * 67")
            
        Returns:
            Dictionary with the calculation result
        """
        try:
            # Security: only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/().() ')
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "error": "Invalid characters in expression"
                }
            
            result = eval(expression)
            return {
                "success": True,
                "expression": expression,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '45 * 67 + 123')"
                }
            },
            "required": ["expression"]
        }
