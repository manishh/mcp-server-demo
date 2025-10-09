import os
from typing import Any
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging


# Read API key from environment
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("currency")

# Constants
CURRENCY_API_BASE = "https://api.getgeoapi.com"
API_KEY = os.getenv("CURRENCY_API_KEY")
logging.info(f"Got the API key? {API_KEY is not None and API_KEY != ''}")  # for debugging

async def _send_api_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Currency API with proper error handling."""   

    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            logging.exception(ex)
            return None
        
def _format_conversion(rates: dict, to_currency: str) -> str:
    """Format currency conversion into a readable string."""
    return f"""
Converted Amount: {rates.get('rate_for_amount', 'Unknown')}
Latest {rates.get('currency_name', to_currency)} Rate: {rates.get('rate', 'Unknown')}    
"""



##############################################################################
#
# Different MCP tools here
#
##############################################################################





if __name__ == "__main__":
    # Initialize and run the server
    logging.info("Running MCP Currency Server...")
    mcp.run(transport='stdio')
