"""Configuration loading."""

import os
import json
import yaml
from pathlib import Path


def load_config() -> dict:
    """Load configuration from Supervisor options or environment."""
    
    # Supervisor provides options in /data/options.yaml
    options_path = Path("/data/options.yaml")
    
    if options_path.exists():
        try:
            with open(options_path) as f:
                options = yaml.safe_load(f)
            
            # Validate required keys exist
            required_keys = ["xiaomi_api_key", "xiaomi_api_base", "xiaomi_model", "max_tokens", "temperature", "system_prompt"]
            missing_keys = [k for k in required_keys if k not in options]
            
            if missing_keys:
                print(f"WARNING: Missing config keys: {missing_keys}")
                
            return options
            
        except Exception as e:
            print(f"ERROR loading /data/options.yaml: {e}")
            raise
    else:
        # Fallback to environment variables (for development)
        print("WARNING: /data/options.yaml not found, using environment variables")
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
