"""Database schema and connection management for diskindex.

Supports PostgreSQL (primary) and SQLite (fallback) backends.
Auto-initializes schema on first run and handles migrations.
"""

import sqlite3
from typing import Optional, Union
from datetime import datetime
import os


class DatabaseConfig:
    """Database connection configuration."""

    def __init__(
        self,
        backend: str = "sqlite",
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.backend = backend
        self.database = database or "diskindex.db"
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_connection(
        self,
    ) -> Union[sqlite3.Connection, "psycopg2.extensions.connection"]:
        """Get database connection based on backend type."""
        if self.backend == "sqlite":
            db_path = os.path.expanduser(self.database)
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
        elif self.backend == "postgresql":
            import psycopg2
            import psycopg2.extras

            conn = psycopg2.connect(
                database=self.database,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
            )
            return conn
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")


# Schema version for migrations
CURRENT_SCHEMA_VERSION = 1


SQLITE_SCHEMA = """
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL PRIMARY KEY,
    updated DATETIME NOT NULL
);

-- Scan sessions
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_date DATETIME NOT NULL,
    scan_path TEXT NOT NULL,
    duration_seconds REAL,
    notes TEXT
);

-- Volumes/partitions
CREATE TABLE IF NOT EXISTS volumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    label TEXT,
    filesystem_type TEXT,
    mount_point TEXT,
    device_path TEXT,
    total_size INTEGER,
    UNIQUE(scan_id, mount_point)
);

-- Directory hierarchy
CREATE TABLE IF NOT EXISTS directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES directories(id) ON DELETE CASCADE,
    path TEXT NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(scan_id, path)
);

-- Files
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    directory_id INTEGER NOT NULL REFERENCES directories(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    extension TEXT,
    size INTEGER NOT NULL,
    mtime DATETIME,
    md5_hash TEXT,
    deleted_at DATETIME
);

-- Ignore patterns
CREATE TABLE IF NOT EXISTS ignore_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL,
    is_exception BOOLEAN DEFAULT 0,
    applies_to TEXT DEFAULT 'all',
    notes TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_files_scan ON files(scan_id);
CREATE INDEX IF NOT EXISTS idx_files_directory ON files(directory_id);
CREATE INDEX IF NOT EXISTS idx_files_filename ON files(filename);
CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
CREATE INDEX IF NOT EXISTS idx_files_size ON files(size);
CREATE INDEX IF NOT EXISTS idx_files_hash ON files(md5_hash);
CREATE INDEX IF NOT EXISTS idx_files_deleted ON files(deleted_at);
CREATE INDEX IF NOT EXISTS idx_directories_scan ON directories(scan_id);
CREATE INDEX IF NOT EXISTS idx_directories_parent ON directories(parent_id);
CREATE INDEX IF NOT EXISTS idx_directories_path ON directories(path);
"""


POSTGRESQL_SCHEMA = """
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL PRIMARY KEY,
    updated TIMESTAMP NOT NULL
);

-- Scan sessions
CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    scan_date TIMESTAMP NOT NULL,
    scan_path TEXT NOT NULL,
    duration_seconds REAL,
    notes TEXT
);

-- Volumes/partitions
CREATE TABLE IF NOT EXISTS volumes (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    label TEXT,
    filesystem_type TEXT,
    mount_point TEXT,
    device_path TEXT,
    total_size BIGINT,
    UNIQUE(scan_id, mount_point)
);

-- Directory hierarchy
CREATE TABLE IF NOT EXISTS directories (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES directories(id) ON DELETE CASCADE,
    path TEXT NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(scan_id, path)
);

-- Files
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    directory_id INTEGER NOT NULL REFERENCES directories(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    extension TEXT,
    size BIGINT NOT NULL,
    mtime TIMESTAMP,
    md5_hash TEXT,
    deleted_at TIMESTAMP
);

-- Ignore patterns
CREATE TABLE IF NOT EXISTS ignore_patterns (
    id SERIAL PRIMARY KEY,
    pattern TEXT NOT NULL,
    is_exception BOOLEAN DEFAULT FALSE,
    applies_to TEXT DEFAULT 'all',
    notes TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_files_scan ON files(scan_id);
CREATE INDEX IF NOT EXISTS idx_files_directory ON files(directory_id);
CREATE INDEX IF NOT EXISTS idx_files_filename ON files(filename);
CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
CREATE INDEX IF NOT EXISTS idx_files_size ON files(size);
CREATE INDEX IF NOT EXISTS idx_files_hash ON files(md5_hash);
CREATE INDEX IF NOT EXISTS idx_files_deleted ON files(deleted_at);
CREATE INDEX IF NOT EXISTS idx_directories_scan ON directories(scan_id);
CREATE INDEX IF NOT EXISTS idx_directories_parent ON directories(parent_id);
CREATE INDEX IF NOT EXISTS idx_directories_path ON directories(path);
"""


def initialize_database(config: DatabaseConfig) -> None:
    """Initialize database schema if not exists."""
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        if config.backend == "sqlite":
            cursor.executescript(SQLITE_SCHEMA)
        else:  # postgresql
            # PostgreSQL doesn't support executescript, execute one by one
            for statement in POSTGRESQL_SCHEMA.split(";"):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

        # Insert initial schema version if not exists
        if config.backend == "sqlite":
            cursor.execute(
                "INSERT OR IGNORE INTO schema_version (version, updated) VALUES (?, ?)",
                (CURRENT_SCHEMA_VERSION, datetime.now()),
            )
        else:
            cursor.execute(
                "INSERT INTO schema_version (version, updated) VALUES (%s, %s) "
                "ON CONFLICT (version) DO NOTHING",
                (CURRENT_SCHEMA_VERSION, datetime.now()),
            )

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def run_migrations(config: DatabaseConfig) -> None:
    """Run database migrations if needed."""
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        # Get current schema version
        cursor.execute("SELECT MAX(version) FROM schema_version")
        result = cursor.fetchone()
        current_version = result[0] if result and result[0] else 0

        # Run migrations for each version
        if current_version < CURRENT_SCHEMA_VERSION:
            # Future migrations will go here
            # Example:
            # if current_version < 2:
            #     cursor.execute("ALTER TABLE files ADD COLUMN sha256_hash TEXT")
            #     cursor.execute(
            #         "INSERT INTO schema_version (version, updated) VALUES (?, ?)",
            #         (2, datetime.now())
            #     )
            pass

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_default_ignore_patterns() -> list[tuple[str, bool, str]]:
    """Get default ignore patterns (pattern, is_exception, notes)."""
    return [
        # Standard development artifacts
        (".git/", False, "Git repository metadata"),
        (".hg/", False, "Mercurial repository metadata"),
        (".svn/", False, "Subversion repository metadata"),
        (".venv/", False, "Python virtual environment"),
        ("venv/", False, "Python virtual environment"),
        ("env/", False, "Python virtual environment"),
        ("node_modules/", False, "Node.js dependencies"),
        ("__pycache__/", False, "Python bytecode cache"),
        ("*.pyc", False, "Python compiled files"),
        ("*.pyo", False, "Python optimized files"),
        (".tox/", False, "Python tox test environment"),
        # Build outputs
        ("build/", False, "Build artifacts"),
        ("dist/", False, "Distribution artifacts"),
        ("*.egg-info/", False, "Python package metadata"),
        # IDE and editor files
        (".idea/", False, "JetBrains IDE settings"),
        (".vscode/", False, "VS Code settings"),
        ("*.swp", False, "Vim swap files"),
        ("*.swo", False, "Vim swap files"),
        ("*~", False, "Backup files"),
        # Cache exceptions - valuable resources
        (".cache/torch/", True, "PyTorch models (valuable)"),
        (".cache/huggingface/", True, "HuggingFace models (valuable)"),
        (".cache/whisper/", True, "Whisper models (valuable)"),
        # General cache (after exceptions)
        (".cache/", False, "General cache directory"),
        ("tmp/", False, "Temporary files"),
        ("temp/", False, "Temporary files"),
    ]


def install_default_ignore_patterns(config: DatabaseConfig) -> None:
    """Install default ignore patterns into database."""
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        # Check if patterns already exist
        cursor.execute("SELECT COUNT(*) FROM ignore_patterns")
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert default patterns
            patterns = get_default_ignore_patterns()
            placeholder = "?" if config.backend == "sqlite" else "%s"

            for pattern, is_exception, notes in patterns:
                cursor.execute(
                    f"INSERT INTO ignore_patterns (pattern, is_exception, applies_to, notes) "
                    f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
                    (pattern, is_exception, "all", notes),
                )

            conn.commit()
    finally:
        cursor.close()
        conn.close()
