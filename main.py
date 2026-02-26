"""
Simple MCP Server
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My First MCP Server")


class AddInput(BaseModel):
    a: int
    b: int


@app.get("/")
def health():
    return {"status": "MCP server running"}


@app.post("/tools/add")
def add(data: AddInput):
    result = data.a + data.b
    return {
        "tool": "add",
        "input": data.model_dump(),
        "output": result
    }
