import subprocess
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MCP_RUN_COMMAND = ["uv", "run", "currency.py"]

def test_mcp_server():
    logger.info("Starting MCP server process...")
    process = subprocess.Popen(
        MCP_RUN_COMMAND,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Initialize
    logger.info("Sending initialize request...")
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    process.stdin.write(json.dumps(init) + "\n")
    process.stdin.flush()
    
    init_response = process.stdout.readline()
    logger.debug(f"Initialize response: {init_response.strip()}")
    
    # Send initialized notification
    logger.info("Sending initialized notification...")
    process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
    process.stdin.flush()
    
    # List tools
    logger.info("Requesting tools list...")
    list_tools = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    process.stdin.write(json.dumps(list_tools) + "\n")
    process.stdin.flush()
    
    response = json.loads(process.stdout.readline())
    logger.info("Available tools:")
    logger.info(json.dumps(response, indent=2))
    
    logger.info("Terminating MCP server process...")
    process.terminate()

if __name__ == "__main__":
    test_mcp_server()