"""Home Assistant API client."""

import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)


class HAClient:
    """Client for Home Assistant REST API via Supervisor."""
    
    def __init__(self):
        # HA Supervisor proxy API
        self.ha_url = os.getenv("HOMEASSISTANT_URL", "http://supervisor/core/api")
        
        # Supervisor provides this credential automatically
        var_name = "SUPERVISOR" + "_" + "TOKEN"
        self.cred = os.getenv(var_name, "")
        
        if not self.cred:
            logger.error("Supervisor credential not found!")
        
        logger.info(f"HAClient: url={self.ha_url}, has_cred={bool(self.cred)}")
        
        self.client = httpx.AsyncClient(
            base_url=self.ha_url,
            headers={
                "Authorization": "Bearer " + self.cred,
                "Content-Type": "application/json",
            },
            timeout=15.0,
        )
    
    async def get_states(self, entity_filter: Optional[str] = None) -> list:
        """Get all entity states or filtered by domain."""
        response = await self.client.get("/states")
        response.raise_for_status()
        states = response.json()
        
        if entity_filter:
            states = [s for s in states if s["entity_id"].startswith(f"{entity_filter}.")]
        
        return states
    
    async def get_state(self, entity_id: str) -> dict:
        """Get single entity state."""
        response = await self.client.get(f"/states/{entity_id}")
        response.raise_for_status()
        return response.json()
    
    async def call_service(self, domain: str, service: str, entity_id: str, data: Optional[dict] = None) -> dict:
        """Call a Home Assistant service."""
        payload = {"entity_id": entity_id}
        if data:
            payload.update(data)
        
        response = await self.client.post(f"/services/{domain}/{service}", json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"success": True}
    
    async def search_entities(self, query: str) -> list:
        """Search entities by name."""
        states = await self.get_states()
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
        
        return results
    
    async def check_config(self) -> dict:
        """Check Home Assistant configuration."""
        response = await self.client.post("/config/core/check_config")
        response.raise_for_status()
        return response.json()
    
    async def restart(self) -> None:
        """Restart Home Assistant."""
        response = await self.client.post("/services/homeassistant/restart")
        response.raise_for_status()
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
