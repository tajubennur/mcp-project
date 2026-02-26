"""
Minimal MCP Protocol Server
Implements tool discovery and execution via JSON-RPC
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="Real MCP Server")


# ---- Tool Definition ----
TOOLS = [
    {
        "name": "add",
        "description": "Add two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    }
]


@app.get("/.well-known/mcp.json")
def mcp_metadata():
    """
    MCP discovery endpoint.
    Foundry uses this to detect MCP compliance.
    """
    return {
        "protocol": "mcp",
        "version": "1.0",
        "tools": TOOLS
    }


@app.post("/mcp")
async def mcp_handler(request: Request):
    """
    JSON-RPC style MCP execution endpoint.
    """
    body = await request.json()

    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    if method == "tools.list":
        result = TOOLS

    elif method == "tools.call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "add":
            result = arguments["a"] + arguments["b"]
        else:
            result = {"error": "Unknown tool"}

    else:
        result = {"error": "Unknown method"}

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }