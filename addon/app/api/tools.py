"""Tools API endpoints."""

import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list")
async def list_tools():
    """List all available MCP tools."""
    from main import app

    mcp = app.state.mcp
    return {"tools": mcp.get_schemas()}


@router.get("/info/{tool_name}")
async def get_tool_info(tool_name: str):
    """Get detailed information about a tool."""
    from main import app

    mcp = app.state.mcp
    tool = mcp.get_tool(tool_name)

    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    return {
        "name": tool.name,
        "description": tool.description,
        "parameters": [p.model_dump() for p in tool.parameters],
    }
