# diskindex

Scan and index files from many disks for easy searching, duplicate detection, and file organization.

## Features

- **Multi-backend database**: PostgreSQL (primary) or SQLite (fallback)
- **Eager MD5 hashing**: Compute checksums during scan for duplicate detection
- **Directory hierarchy**: Track full directory structure with parent relationships
- **Volume detection**: Identify disk volumes, labels, and partition info (Windows & Linux)
- **Configurable ignore patterns**: Skip development artifacts with exception support (.cache/torch/ kept, rest ignored)
- **Progress tracking**: tqdm progress bars with file rate and ETA
- **Batch commits**: Efficient database inserts (1000 files per commit)
- **Incremental rescans**: Mark deleted files, identify new files (coming soon)
- **Duplicate management**: Multi-stage grouping and redundancy control (coming soon)
- **Web GUI**: Flask-based interface for exploration (coming soon)
- **Lightweight scanner**: Python 2.7 compatible for old systems (coming soon)

## Installation

### Using uv (recommended)

```bash
cd diskindex

# Create virtual environment
uv venv

# Install in editable mode
uv pip install -e .

# Or install with all features
uv pip install -e ".[all]"
```

### Using pipx (for CLI tool)

```bash
# Install as isolated CLI tool
pipx install /path/to/diskindex

# Or with extras
pipx install "/path/to/diskindex[postgresql]"
```

### Using uv tool (for CLI tool)

```bash
# Install as CLI tool with uv
uv tool install .

# Or from directory
uv tool install /path/to/diskindex

# With extras
uv tool install ".[postgresql]"
```

### Traditional pip

```bash
cd diskindex
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Optional dependencies

- `postgresql` - PostgreSQL database support
- `web` - Flask web GUI (coming soon)
- `lite` - Python 2.7 scanner support (coming soon)
- `all` - All optional dependencies

## Quick Start

Initialize the database:
```bash
# Using uv run (no activation needed)
uv run diskindex init --save-config

# Or if installed with pipx/uv tool
diskindex init --save-config

# Or in activated venv
diskindex init --save-config
```

Scan a directory:
```bash
uv run diskindex scan /path/to/directory --notes "My first scan"
# Or: diskindex scan /path/to/directory --notes "My first scan"
```

List all scans:
```bash
uv run diskindex list-scans
# Or: diskindex list-scans
```

## Usage

### Using uv run (recommended - no venv activation needed)

```bash
# Initialize
uv run diskindex init --save-config

# Scan with all options shown
uv run diskindex scan /media/backup --notes "Backup drive scan"
uv run diskindex scan /large/archive --no-hash
uv run diskindex scan /path --batch-size 5000

# List scans
uv run diskindex list-scans
```

### Using installed command (pipx/uv tool/activated venv)

```bash
# Initialize Database
diskindex init --save-config

# PostgreSQL
diskindex init --backend postgresql --database mydb --host localhost --user myuser --save-config

# Scan Directories
diskindex scan /media/backup --notes "Backup drive scan"
diskindex scan /large/archive --no-hash
diskindex scan /path --batch-size 5000

# List Scans
diskindex list-scans
```

## Configuration

Configuration is loaded from (in order):
1. `~/.config/diskindex/config.json`
2. Environment variables (`DISKINDEX_BACKEND`, `DISKINDEX_DATABASE`, etc.)
3. Command-line arguments

Database location (SQLite): `~/.local/share/diskindex/diskindex.db`

## Ignore Patterns

Default patterns (22 total, 3 exceptions):

**Ignored:**
- `.git/`, `.hg/`, `.svn/` (VCS metadata)
- `.venv/`, `venv/`, `env/` (Python virtual environments)
- `node_modules/` (Node.js dependencies)
- `__pycache__/`, `*.pyc`, `*.pyo` (Python cache)
- `build/`, `dist/` (build artifacts)
- `.idea/`, `.vscode/` (IDE settings)
- `.cache/`, `tmp/`, `temp/` (caches and temporary files)

**Exceptions (kept):**
- `.cache/torch/` (PyTorch models)
- `.cache/huggingface/` (HuggingFace models)
- `.cache/whisper/` (Whisper models)

## Database Schema

**scans**: Scan sessions with date, path, duration, notes
**volumes**: Disk volume metadata (label, filesystem, mount point, size)
**directories**: Directory hierarchy with parent_id relationships
**files**: File metadata (name, size, mtime, md5_hash, deleted_at)
**ignore_patterns**: Configurable patterns with exception support
**schema_version**: Schema version tracking for migrations

## Development Status

### Phase 1 (Current)

- [x] Database schema with PostgreSQL/SQLite support
- [x] Configuration management
- [x] Full-featured scanner with MD5 hashing
- [x] Directory hierarchy tracking
- [x] Volume detection (Windows/Linux)
- [x] Ignore pattern system with exceptions
- [x] Progress tracking with tqdm
- [x] Basic CLI (init, scan, list-scans)
- [ ] Incremental rescan support
- [ ] Duplicate detection module
- [ ] Search and query functions
- [ ] JSON export/import
- [ ] Lightweight scanner (Python 2.7)
- [ ] Web GUI (Flask)

### Phase 2 (Planned)

- Image similarity detection (perceptual hashing, SSIM)
- Media metadata (audio/video durations)
- Advanced duplicate management
- Redundancy level configuration
- Pattern-based file organization

## Architecture

```
diskindex/
├── pyproject.toml       # Project configuration
├── README.md
├── .gitignore
└── src/
    └── diskindex/
        ├── __init__.py      # Package initialization
        ├── main.py          # CLI entry point with argparse subcommands
        ├── config.py        # Configuration loading (file, env, CLI)
        ├── database.py      # Schema, connection management, migrations
        ├── models.py        # Data classes (Scan, Volume, Directory, File)
        ├── scanner.py       # File walker with MD5, progress, batch commits
        ├── duplicates.py    # Multi-stage grouping (coming soon)
        ├── queries.py       # Search functions (coming soon)
        └── web/             # Flask GUI (coming soon)
```

## Development

### uv Best Practices

This project follows uv conventions:

- **`.python-version`** is committed - specifies Python 3.12
- **`uv.lock`** is committed - ensures reproducible installations
- Use `uv sync` to install exact locked versions
- Use `uv lock --upgrade` to update dependencies

### Common Development Commands

```bash
# Install in development mode with all extras
uv sync --all-extras

# Run without installing
uv run diskindex scan /path/to/scan

# Run tests (when added)
uv run pytest

# Update dependencies
uv lock --upgrade

# Install as global tool (for testing)
uv tool install --editable .

# Uninstall global tool
uv tool uninstall diskindex
```

## License

MIT
