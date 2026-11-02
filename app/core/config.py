"""Configuration loading."""

import os
import json
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config() -> dict:
    """Load configuration from Supervisor options or environment."""
    
    # Supervisor provides options in multiple possible locations
    possible_paths = [
        Path("/data/options.json"),
        Path("/data/options.yaml"),
        Path("/app/options.yaml"),
        Path("/config/options.yaml"),
    ]
    
    options_path = None
    for path in possible_paths:
        if path.exists():
            options_path = path
            logger.info(f"Found options file at: {path}")
            break
    
    if options_path:
        try:
            with open(options_path) as f:
                if options_path.suffix == '.json':
                    options = json.load(f)
                else:
                    options = yaml.safe_load(f)
            
            # Validate required keys exist
            required_keys = ["xiaomi_api_key", "xiaomi_api_base", "xiaomi_model", "max_tokens", "temperature", "system_prompt"]
            missing_keys = [k for k in required_keys if k not in options]
            
            if missing_keys:
                logger.warning(f"Missing config keys: {missing_keys}")
            
            # Debug: log what was actually loaded
            logger.info(f"Loaded config from {options_path}")
            logger.info(f"Loaded config keys: {list(options.keys())}")
            logger.info(f"xiaomi_api_base: {options.get('xiaomi_api_base', 'NOT SET')}")
            logger.info(f"xiaomi_api_key present: {'xiaomi_api_key' in options and bool(options['xiaomi_api_key'])}")
            
            return options
            
        except Exception as e:
            logger.error(f"ERROR loading {options_path}: {e}")
            raise
            
    else:
        # Fallback to environment variables (Supervisor may pass these directly)
        logger.warning("Options file not found, checking environment variables")
        
        # Log all environment variables for debugging
        # Never log the environment: it contains administrator credentials.
        
        # Check various possible env var names
        api_key = os.getenv("XIAOMI_API_KEY") or os.getenv("xiaomi_api_key", "")
        api_base = os.getenv("XIAOMI_API_BASE") or os.getenv("xiaomi_api_base", "https://api.xiaomi.com/v1")
        model = os.getenv("XIAOMI_MODEL") or os.getenv("xiaomi_model", "mimo-v2.6-pro")
        
        options = {
            "xiaomi_api_key": api_key,
            "xiaomi_api_base": api_base,
            "xiaomi_model": model,
            "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "system_prompt": os.getenv(
                "SYSTEM_PROMPT",
                "You are a helpful Home Assistant configuration assistant powered by Xiaomi MiMo.",
            ),
        }
        
        logger.info(f"Loaded from environment: {list(options.keys())}")
        logger.info(f"xiaomi_api_base from env: {api_base}")
        logger.info(f"xiaomi_api_key present: {bool(api_key)}")
        return options
