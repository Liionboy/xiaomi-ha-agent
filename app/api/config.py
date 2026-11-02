"""Configuration API endpoints."""

import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class ConfigUpdate(BaseModel):
    """Configuration update request."""
    key: str
    value: str


@router.get("/")
async def get_config():
    """Get current configuration."""
    from main import app

    config = app.state.config.copy()

    # Mask sensitive values
    if config.get("xiaomi_api_key"):
        config["xiaomi_api_key"] = "***masked***"

    return config


@router.post("/update")
async def update_config(update: ConfigUpdate):
    """Update configuration."""
    # TODO: Implement config persistence
    return {"success": True, "message": f"Updated {update.key}"}


@router.post("/reload")
async def reload_config():
    """Reload configuration."""
    from main import app

    app.state.config = app.state.config.__class__.load_config()
    return {"success": True, "message": "Configuration reloaded"}
