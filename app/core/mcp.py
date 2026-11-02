"""MCP Tool Registry."""

from typing import Any, Callable, Optional
from pydantic import BaseModel


class ToolParameter(BaseModel):
    """Tool parameter schema."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


class MCPTool:
    """MCP Tool definition."""

    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable,
        parameters: list[ToolParameter],
    ):
        self.name = name
        self.description = description
        self.handler = handler
        self.parameters = parameters

    def to_schema(self) -> dict:
        """Convert to OpenAI tool schema."""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }


class MCPToolRegistry:
    """Registry for MCP tools."""

    def __init__(self):
        self.tools: dict[str, MCPTool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: list[ToolParameter],
    ) -> Callable:
        """Decorator to register a tool."""
        def decorator(func: Callable) -> Callable:
            tool = MCPTool(name, description, func, parameters)
            self.tools[name] = tool
            return func
        return decorator

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get tool by name."""
        return self.tools.get(name)

    def get_schemas(self) -> list[dict]:
        """Get all tool schemas for OpenAI API."""
        return [tool.to_schema() for tool in self.tools.values()]

    async def execute(self, name: str, arguments: dict) -> Any:
        """Execute a tool."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")

        return await tool.handler(**arguments)
