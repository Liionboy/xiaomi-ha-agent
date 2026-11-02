"""Chat API endpoints."""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message."""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat completion request."""
    messages: list[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    use_tools: bool = True


class ToolCall(BaseModel):
    """Tool call."""
    id: str
    name: str
    arguments: dict


class ChatResponse(BaseModel):
    """Chat response."""
    message: ChatMessage
    tool_calls: Optional[list[ToolCall]] = None
    usage: Optional[dict] = None


@router.post("/completion", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Send chat completion request to Xiaomi API."""
    from main import app

    config = app.state.config
    xiaomi = app.state.xiaomi
    mcp = app.state.mcp
    
    logger.info(f"Chat completion request received with {len(request.messages)} messages")
    logger.info(f"Config keys: {list(config.keys())}")
    logger.info(f"Xiaomi client initialized: {xiaomi is not None}")
    
    try:
        # Convert messages to dict format
        messages = [msg.model_dump(exclude_none=True) for msg in request.messages]

        # Add system prompt if not present
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {
                "role": "system",
                "content": config["system_prompt"],
            })

        # Get tool schemas if requested
        tools = mcp.get_schemas() if request.use_tools else None

        # Call Xiaomi API
        logger.info(f"Calling Xiaomi API with model: {xiaomi.model}, base: {xiaomi.api_base}")
        logger.info(f"Using {len(tools) if tools else 0} tools, {len(messages)} messages")
        
        response = await xiaomi.chat_completion(
            messages=messages,
            tools=tools,
            temperature=request.temperature or config["temperature"],
            max_tokens=request.max_tokens or config["max_tokens"],
        )
        
        logger.info(f"Xiaomi API response received: {type(response)}")

        # Parse response
        choice = response["choices"][0]
        message = choice["message"]

        # Extract tool calls
        tool_calls = None
        if message.get("tool_calls"):
            tool_calls = [
                ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    arguments=tc["function"]["arguments"],
                )
                for tc in message["tool_calls"]
            ]

        return ChatResponse(
            message=ChatMessage(
                role=message["role"],
                content=message.get("content", ""),
            ),
            tool_calls=tool_calls,
            usage=response.get("usage"),
        )

    except Exception as e:
        logger.error(f"Chat completion error: {type(e).__name__}: {e}", exc_info=True)
        
        # Check for specific error types
        error_msg = str(e)
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            error_msg = "Xiaomi API key is invalid or missing. Please check your configuration."
        elif "404" in error_msg or "not found" in error_msg.lower():
            error_msg = f"Model '{xiaomi.model}' not found. Please check your model configuration."
        elif "timeout" in error_msg.lower():
            error_msg = "Xiaomi API request timed out. Please try again."
        elif "connection" in error_msg.lower():
            error_msg = "Cannot connect to Xiaomi API. Please check your internet connection and API URL."
        
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/execute-tool")
async def execute_tool(tool_name: str, arguments: dict):
    """Execute an MCP tool."""
    from main import app

    mcp = app.state.mcp

    try:
        result = await mcp.execute(tool_name, arguments)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
