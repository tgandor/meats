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

```bash
cd diskindex
pip install -e .
```

For PostgreSQL support:
```bash
pip install -e ".[postgresql]"
```

For web GUI:
```bash
pip install -e ".[web]"
```

All features:
```bash
pip install -e ".[all]"
```

## Quick Start

Initialize the database:
```bash
python main.py init --save-config
```

Scan a directory:
```bash
python main.py scan /path/to/directory --notes "My first scan"
```

List all scans:
```bash
python main.py list-scans
```

## Usage

### Initialize Database

```bash
# SQLite (default)
python main.py init --save-config

# PostgreSQL
python main.py init --backend postgresql --database mydb --host localhost --user myuser --save-config
```

### Scan Directories

```bash
# Full scan with MD5 hashing
python main.py scan /media/backup --notes "Backup drive scan"

# Scan without hashing (faster)
python main.py scan /large/archive --no-hash

# Custom batch size
python main.py scan /path --batch-size 5000
```

### List Scans

```bash
python main.py list-scans
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
├── main.py          # CLI entry point with argparse subcommands
├── config.py        # Configuration loading (file, env, CLI)
├── database.py      # Schema, connection management, migrations
├── models.py        # Data classes (Scan, Volume, Directory, File)
├── scanner.py       # File walker with MD5, progress, batch commits
├── duplicates.py    # Multi-stage grouping (coming soon)
├── queries.py       # Search functions (coming soon)
└── web/             # Flask GUI (coming soon)
```

## License

MIT
