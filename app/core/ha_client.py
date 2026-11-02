"""Home Assistant API client."""

import os
import httpx
from typing import Optional


class HAClient:
    """Client for Home Assistant REST API."""
    
    def __init__(self):
        # HA Supervisor provides these environment variables
        self.ha_url = os.getenv("HOMEASSISTANT_URL", "http://supervisor/core/api")
        self.token = os.getenv("SUPERVISOR_TOKEN", "")
        
        if not self.token:
            # Fallback to config
            self.token = os.getenv("HOMEASSISTANT_TOKEN", "")
        
        self.client = httpx.AsyncClient(
            base_url=self.ha_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=10.0,
        )
    
    async def get_states(self, entity_filter: Optional[str] = None) -> list[dict]:
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
        payload = {
            "entity_id": entity_id,
        }
        if data:
            payload.update(data)
        
        response = await self.client.post(f"/services/{domain}/{service}", json=payload)
        response.raise_for_status()
        return response.json()
    
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
