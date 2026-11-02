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

        # Iterative tool-call loop
        all_tool_calls = []
        message = response["choices"][0]["message"]
        
        for iteration in range(8):  # max 8 tool-call rounds
            tool_calls_raw = message.get("tool_calls")
            if not tool_calls_raw:
                break  # AI done, no more tools to call
            
            # Parse + execute each tool call
            for tc in tool_calls_raw:
                arguments = tc["function"]["arguments"]
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                
                parsed_call = ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    arguments=arguments,
                )
                all_tool_calls.append(parsed_call)
                
                try:
                    logger.info(f"[iter {iteration}] Executing tool: {parsed_call.name} args={parsed_call.arguments}")
                    result = await mcp.execute(parsed_call.name, parsed_call.arguments)
                    logger.info(f"[iter {iteration}] Tool result: {str(result)[:200]}")
                except Exception as tool_err:
                    logger.error(f"[iter {iteration}] Tool error: {tool_err}")
                    result = {"error": str(tool_err)}
                
                # Add assistant tool_call message (required by API format)
                messages.append({
                    "role": "assistant",
                    "content": message.get("content") or "",
                    "tool_calls": [tc],
                })
                # Add tool result
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": str(result),
                })
            
            # Call API again with tool results
            response = await xiaomi.chat_completion(
                messages=messages,
                tools=tools,
                temperature=request.temperature or config["temperature"],
                max_tokens=request.max_tokens or config["max_tokens"],
            )
            message = response["choices"][0]["message"]
        
        final_content = message.get("content", "") or "(no response)"
        
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content=final_content,
            ),
            tool_calls=all_tool_calls if all_tool_calls else None,
            usage=response.get("usage"),
        )

    except Exception as e:
        error_str = str(e)
        logger.error(f"Chat completion error: {type(e).__name__}: {error_str}", exc_info=True)
        
        # Check for specific error types
        if "Name does not resolve" in error_str or "-2" in error_str:
            error_msg = "DNS resolution failed. Cannot resolve api.xiaomi.com. Check your internet connection and DNS settings."
        elif "401" in error_str or "unauthorized" in error_str.lower():
            error_msg = "Xiaomi API key is invalid or missing. Please check your configuration."
        elif "404" in error_str or "not found" in error_str.lower():
            error_msg = f"Model '{xiaomi.model}' not found. Please check your model configuration."
        elif "timeout" in error_str.lower():
            error_msg = "Xiaomi API request timed out. Please try again."
        elif "connection" in error_str.lower():
            error_msg = "Cannot connect to Xiaomi API. Please check your internet connection and API URL."
        else:
            error_msg = f"Error: {error_str}"
        
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
