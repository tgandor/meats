"""Configuration management for diskindex.

Loads configuration from:
1. Config file (~/.config/diskindex/config.json)
2. Environment variables
3. Command-line arguments (handled by main.py)
"""

import json
import os
import pathlib
from typing import Optional

from database import DatabaseConfig


DEFAULT_CONFIG_PATH = pathlib.Path.home() / ".config" / "diskindex" / "config.json"


def load_config(config_path: Optional[pathlib.Path] = None) -> DatabaseConfig:
    """Load database configuration from file and environment."""
    config_path = config_path or DEFAULT_CONFIG_PATH
    
    # Default configuration
    config_data = {
        "backend": "sqlite",
        "database": str(pathlib.Path.home() / ".local" / "share" / "diskindex" / "diskindex.db"),
    }
    
    # Load from config file if exists
    if config_path.exists():
        with config_path.open() as f:
            file_config = json.load(f)
            config_data.update(file_config)
    
    # Override with environment variables
    if os.environ.get("DISKINDEX_BACKEND"):
        config_data["backend"] = os.environ["DISKINDEX_BACKEND"]
    if os.environ.get("DISKINDEX_DATABASE"):
        config_data["database"] = os.environ["DISKINDEX_DATABASE"]
    if os.environ.get("DISKINDEX_HOST"):
        config_data["host"] = os.environ["DISKINDEX_HOST"]
    if os.environ.get("DISKINDEX_PORT"):
        config_data["port"] = int(os.environ["DISKINDEX_PORT"])
    if os.environ.get("DISKINDEX_USER"):
        config_data["user"] = os.environ["DISKINDEX_USER"]
    if os.environ.get("DISKINDEX_PASSWORD"):
        config_data["password"] = os.environ["DISKINDEX_PASSWORD"]
    
    return DatabaseConfig(**config_data)


def save_config(config: DatabaseConfig, config_path: Optional[pathlib.Path] = None) -> None:
    """Save database configuration to file."""
    config_path = config_path or DEFAULT_CONFIG_PATH
    
    # Ensure config directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare config data (exclude password for security)
    config_data = {
        "backend": config.backend,
        "database": config.database,
    }
    
    if config.host:
        config_data["host"] = config.host
    if config.port:
        config_data["port"] = config.port
    if config.user:
        config_data["user"] = config.user
    # Note: password not saved to file, use env var instead
    
    with config_path.open('w') as f:
        json.dump(config_data, f, indent=2)


def ensure_data_directory(config: DatabaseConfig) -> None:
    """Ensure data directory exists for SQLite database."""
    if config.backend == "sqlite":
        db_path = pathlib.Path(config.database).expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
