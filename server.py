from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

@mcp.tool()
def calculate(expression: str) -> str:
    """Perform basic arithmetic calculations. Supports +, -, *, /, ** (power), and parentheses."""
    try:
        # Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/().** ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Only numbers and basic operators (+, -, *, /, **, parentheses) are allowed."
        
        # Evaluate the expression safely
        result = eval(expression)
        return f"{expression} = {result}"
    
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except SyntaxError:
        return "Error: Invalid mathematical expression."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")