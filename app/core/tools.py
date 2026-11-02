"""MCP Tools for Home Assistant."""

from typing import Any
from .mcp import MCPToolRegistry, ToolParameter
from .ha_client import HAClient


def register_all_tools(registry: MCPToolRegistry):
    """Register all MCP tools."""

    # Initialize HA client
    ha = HAClient()

    # ========================================
    # ENTITY TOOLS
    # ========================================

    @registry.register(
        name="ha_get_entity_state",
        description="Get the current state of a Home Assistant entity",
        parameters=[
            ToolParameter(name="entity_id", type="string", description="Entity ID (e.g., light.living_room)"),
        ],
    )
    async def get_entity_state(entity_id: str) -> dict:
        """Get entity state from Home Assistant."""
        try:
            state = await ha.get_state(entity_id)
            return {
                "entity_id": state["entity_id"],
                "state": state["state"],
                "attributes": state.get("attributes", {}),
                "last_changed": state.get("last_changed"),
            }
        except Exception as e:
            return {"error": f"Failed to get state for {entity_id}: {str(e)}"}

    @registry.register(
        name="ha_list_entities",
        description="List all Home Assistant entities, optionally filtered by domain",
        parameters=[
            ToolParameter(name="domain", type="string", description="Filter by domain (e.g., light, sensor)", required=False),
        ],
    )
    async def list_entities(domain: str = None) -> list[dict]:
        """List all entities."""
        try:
            states = await ha.get_states(domain)
            return [
                {
                    "entity_id": s["entity_id"],
                    "state": s["state"],
                    "friendly_name": s.get("attributes", {}).get("friendly_name", s["entity_id"]),
                }
                for s in states
            ]
        except Exception as e:
            return [{"error": f"Failed to list entities: {str(e)}"}]

    @registry.register(
        name="ha_call_service",
        description="Call a Home Assistant service to control devices (turn_on, turn_off, etc.)",
        parameters=[
            ToolParameter(name="domain", type="string", description="Service domain (e.g., light, switch)"),
            ToolParameter(name="service", type="string", description="Service name (e.g., turn_on, turn_off)"),
            ToolParameter(name="entity_id", type="string", description="Entity ID to control"),
            ToolParameter(name="data", type="object", description="Additional service data (optional)", required=False),
        ],
    )
    async def call_service(domain: str, service: str, entity_id: str, data: dict = None) -> dict:
        """Call Home Assistant service."""
        try:
            result = await ha.call_service(domain, service, entity_id, data)
            return {
                "success": True,
                "service": f"{domain}.{service}",
                "entity_id": entity_id,
                "result": result,
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to call {domain}.{service}: {str(e)}"}

    # ========================================
    # CONFIGURATION TOOLS
    # ========================================

    @registry.register(
        name="ha_check_config",
        description="Validate Home Assistant configuration for errors",
        parameters=[],
    )
    async def check_config() -> dict:
        """Check HA configuration."""
        try:
            result = await ha.check_config()
            return {
                "valid": result.get("result", "") == "valid",
                "errors": result.get("errors", ""),
                "warnings": result.get("warnings", ""),
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @registry.register(
        name="ha_restart",
        description="Restart Home Assistant",
        parameters=[],
    )
    async def restart_homeassistant() -> dict:
        """Restart Home Assistant."""
        try:
            await ha.restart()
            return {"success": True, "message": "Home Assistant is restarting..."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========================================
    # AUTOMATION & HISTORY
    # ========================================

    @registry.register(
        name="ha_get_automations",
        description="List all automations",
        parameters=[],
    )
    async def get_automations() -> list[dict]:
        """Get all automations."""
        try:
            states = await ha.get_states("automation")
            return [
                {
                    "entity_id": s["entity_id"],
                    "state": s["state"],
                    "friendly_name": s.get("attributes", {}).get("friendly_name", ""),
                }
                for s in states
            ]
        except Exception as e:
            return [{"error": f"Failed to get automations: {str(e)}"}]

    @registry.register(
        name="ha_search_entities",
        description="Search for entities by name or partial name",
        parameters=[
            ToolParameter(name="query", type="string", description="Search query (e.g., 'Plafoniera', 'Birou', 'living')"),
        ],
    )
    async def search_entities(query: str) -> list[dict]:
        """Search entities by friendly name or entity_id."""
        try:
            states = await ha.get_states()
            query_lower = query.lower()
            
            results = []
            for s in states:
                friendly_name = s.get("attributes", {}).get("friendly_name", "").lower()
                entity_id = s["entity_id"].lower()
                
                if query_lower in friendly_name or query_lower in entity_id:
                    results.append({
                        "entity_id": s["entity_id"],
                        "state": s["state"],
                        "friendly_name": s.get("attributes", {}).get("friendly_name", s["entity_id"]),
                        "domain": s["entity_id"].split(".")[0],
                    })
            
            return results if results else [{"message": f"No entities found matching '{query}'"}]
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
