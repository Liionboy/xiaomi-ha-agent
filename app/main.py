"""Xiaomi Home Assistant Agent — Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import load_config
from core.mcp import MCPToolRegistry
from core.xiaomi_client import XiaomiClient
from api.chat import router as chat_router
from api.tools import router as tools_router
from api.config import router as config_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown."""
    logger.info("Starting Xiaomi Home Assistant Agent...")

    # Load configuration
    app.state.config = load_config()

    # Initialize MCP tool registry
    app.state.mcp = MCPToolRegistry()

    # Initialize Xiaomi client
    app.state.xiaomi = XiaomiClient(
        api_key=***"xiaomi_api_key"],
        api_base=app.state.config["xiaomi_api_base"],
        model=app.state.config["xiaomi_model"],
    )

    # Load tools
    from core.tools import register_all_tools
    register_all_tools(app.state.mcp)

    logger.info(f"Loaded {len(app.state.mcp.tools)} MCP tools")

    yield

    logger.info("Shutting down Xiaomi Home Assistant Agent...")


app = FastAPI(
    title="Xiaomi Home Assistant Agent",
    description="AI-powered configuration assistant",
    version="0.1.0",
    lifespan=lifespan,
)

# Mount static files (Web UI)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Include routers
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(tools_router, prefix="/api/tools", tags=["tools"])
app.include_router(config_router, prefix="/api/config", tags=["config"])


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "xiaomi-ha-agent"}


@app.get("/")
async def root():
    """Serve Web UI."""
    from fastapi.responses import FileResponse
    return FileResponse(Path(__file__).parent / "static" / "index.html")
