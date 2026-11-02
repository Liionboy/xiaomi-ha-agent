"""Configuration loading."""

import os
import yaml
from pathlib import Path


def load_config() -> dict:
    """Load configuration from options.yaml or environment."""
    # Try to load from options.yaml (Supervisor provides this)
    options_path = Path("/data/options.yaml")

    if options_path.exists():
        with open(options_path) as f:
            options = yaml.safe_load(f)
    else:
        # Fallback to environment variables (for development)
        options = {
            "xiaomi_api_key": os.getenv("XIAOMI_API_KEY", ""),
            "xiaomi_api_base": os.getenv("XIAOMI_API_BASE", "https://api.xiaomi.com/v1"),
            "xiaomi_model": os.getenv("XIAOMI_MODEL", "mimo-v2.6-pro"),
            "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "system_prompt": os.getenv(
                "SYSTEM_PROMPT",
                "You are a helpful Home Assistant configuration assistant powered by Xiaomi MiMo.",
            ),
        }

    return options
