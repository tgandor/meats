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

from diskindex.database import DatabaseConfig


def get_config_path() -> pathlib.Path:
    """Get the configuration file path."""
    return pathlib.Path.home() / ".config" / "diskindex" / "config.json"


def get_default_db_path() -> pathlib.Path:
    """Get the default SQLite database path."""
    return pathlib.Path.home() / ".local" / "share" / "diskindex" / "diskindex.db"


DEFAULT_CONFIG_PATH = get_config_path()


def load_config(config_path: Optional[pathlib.Path] = None) -> DatabaseConfig:
    """Load database configuration from file and environment."""
    config_path = config_path or DEFAULT_CONFIG_PATH

    # Default configuration
    backend = "sqlite"
    database = str(
        pathlib.Path.home() / ".local" / "share" / "diskindex" / "diskindex.db"
    )
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None

    # Load from config file if exists
    if config_path.exists():
        with config_path.open() as f:
            file_config = json.load(f)
            backend = file_config.get("backend", backend)
            database = file_config.get("database", database)
            host = file_config.get("host", host)
            port = file_config.get("port", port)
            user = file_config.get("user", user)
            password = file_config.get("password", password)

    # Override with environment variables
    if os.environ.get("DISKINDEX_BACKEND"):
        backend = os.environ["DISKINDEX_BACKEND"]
    if os.environ.get("DISKINDEX_DATABASE"):
        database = os.environ["DISKINDEX_DATABASE"]
    if os.environ.get("DISKINDEX_HOST"):
        host = os.environ["DISKINDEX_HOST"]
    if os.environ.get("DISKINDEX_PORT"):
        port = int(os.environ["DISKINDEX_PORT"])
    if os.environ.get("DISKINDEX_USER"):
        user = os.environ["DISKINDEX_USER"]
    if os.environ.get("DISKINDEX_PASSWORD"):
        password = os.environ["DISKINDEX_PASSWORD"]

    return DatabaseConfig(
        backend=backend,
        database=database,
        host=host,
        port=port,
        user=user,
        password=password,
    )


def save_config(
    config: DatabaseConfig, config_path: Optional[pathlib.Path] = None
) -> None:
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

    with config_path.open("w") as f:
        json.dump(config_data, f, indent=2)


def ensure_data_directory(config: DatabaseConfig) -> None:
    """Ensure data directory exists for SQLite database."""
    if config.backend == "sqlite":
        db_path = pathlib.Path(config.database).expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
