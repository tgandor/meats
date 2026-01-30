"""Main CLI interface for diskindex."""

import argparse
import json
import sys

from diskindex.config import (
    load_config,
    ensure_data_directory,
    get_config_path,
    get_default_db_path,
)
from diskindex.database import (
    initialize_database,
    install_default_ignore_patterns,
    run_migrations,
)
from diskindex.scanner import Scanner


def normalize_backend(backend: str) -> str:
    """Normalize backend aliases to canonical names."""
    aliases = {
        "pg": "postgresql",
        "pgsql": "postgresql",
        "postgres": "postgresql",
        "sqlite3": "sqlite",
    }
    return aliases.get(backend.lower(), backend.lower())


def cmd_init(args):
    """Initialize database and configuration."""
    config_path = get_config_path()
    db_path = get_default_db_path()

    # Normalize backend aliases
    args.backend = normalize_backend(args.backend)

    # Validate SQLite-specific constraints
    if args.backend == "sqlite":
        # Check if PostgreSQL-specific options were explicitly provided
        # (only error if they differ from defaults or were explicitly set)
        has_pg_options = (
            (args.host and args.host != "localhost")
            or (args.port and args.port != 5432)
            or (args.user and args.user != "postgres")
            or args.password
        )
        if has_pg_options:
            print(
                "Error: SQLite backend does not accept --host, --port, --user, or --password",
                file=sys.stderr,
            )
            print(
                f"Use --database to specify SQLite file path (default: {db_path})",
                file=sys.stderr,
            )
            return 1

    # Validate PostgreSQL-specific constraints
    if args.backend == "postgresql":
        # Check if psycopg2 is available
        try:
            import psycopg2
        except ImportError:
            print("Error: PostgreSQL backend requires psycopg2-binary", file=sys.stderr)
            print(
                "Install with: uv pip install 'diskindex[postgresql]'", file=sys.stderr
            )
            print("         or: pip install 'diskindex[postgresql]'", file=sys.stderr)
            return 1

        if not args.database:
            print("Error: PostgreSQL backend requires --database (-d)", file=sys.stderr)
            return 1

        # Get password from environment if not provided
        password = args.password
        if not password:
            import os

            password = os.environ.get("PGPASSWORD")

        # Test PostgreSQL connection before saving config
        print(
            f"Testing PostgreSQL connection to {args.host}:{args.port}/{args.database}..."
        )
        try:
            conn_params = {
                "dbname": args.database,
                "host": args.host,
                "port": args.port,
                "user": args.user,
            }

            if password:
                conn_params["password"] = password

            # Test connection
            conn = psycopg2.connect(**conn_params)
            conn.close()
            print("✓ Connection successful")
        except Exception as e:
            print(f"Error: Failed to connect to PostgreSQL: {e}", file=sys.stderr)
            print("\nPlease verify:", file=sys.stderr)
            print(f"  - Database '{args.database}' exists", file=sys.stderr)
            print(f"  - Host '{args.host}' is reachable", file=sys.stderr)
            print(f"  - User '{args.user}' has access", file=sys.stderr)
            print(
                "  - Password is correct (use --password or PGPASSWORD env var)",
                file=sys.stderr,
            )
            return 1

    # Build config from args
    config = load_config()
    config.backend = args.backend
    config.database = args.database or str(db_path)

    if args.backend == "postgresql":
        config.host = args.host
        config.port = args.port
        config.user = args.user
        if args.password:
            config.password = args.password

    # Ensure data directory exists
    ensure_data_directory(config)

    # Initialize database
    print(f"\nInitializing {args.backend} database...")
    if args.backend == "sqlite":
        print(f"Database location: {config.database}")
    else:
        print(f"Database: {config.database} at {config.host}:{config.port}")

    initialize_database(config)
    print("✓ Database schema created")

    # Run migrations
    run_migrations(config)
    print("✓ Migrations applied")

    # Install default ignore patterns
    install_default_ignore_patterns(config)
    print("✓ Default ignore patterns installed")

    # Save configuration
    if args.save_config:
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare config data (exclude password for security)
        config_data = {
            "backend": config.backend,
            "database": config.database,
        }

        if config.backend == "postgresql":
            config_data.update(
                {
                    "host": config.host,
                    "port": config.port,
                    "user": config.user,
                }
            )
            if args.password:
                print("\nNote: Password not saved to config file for security.")
                print("Set PGPASSWORD environment variable or use ~/.pgpass file.")

        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        print(f"✓ Configuration saved to {config_path}")

    # Show summary
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("=" * 60)
    print(f"Backend:  {args.backend}")
    if args.backend == "sqlite":
        print(f"Database: {config.database}")
    else:
        print(f"Database: {config.database}")
        print(f"Host:     {config.host}:{config.port}")
        print(f"User:     {config.user}")

    if args.save_config:
        print(f"\nConfig:   {config_path}")
    else:
        print("\nConfig:   Not saved (use --save-config to persist)")

    print("\nNext steps:")
    print("  diskindex scan /path/to/directory")
    print("  diskindex list-scans")

    return 0


def cmd_scan(args):
    """Perform a full scan."""
    config = load_config()

    # Ensure database is initialized
    ensure_data_directory(config)
    initialize_database(config)
    run_migrations(config)

    # Create scanner
    scanner = Scanner(
        config,
        compute_hash=not args.no_hash,
        batch_size=args.batch_size,
        one_filesystem=args.one_filesystem,
    )

    # Perform scan
    scan_id = scanner.scan(args.path, notes=args.notes)
    print(f"\nScan #{scan_id} completed successfully!")


def cmd_list_scans(args):
    """List all scans."""
    config = load_config()
    run_migrations(config)
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, scan_date, scan_path, duration_seconds, notes "
            "FROM scans ORDER BY scan_date DESC"
        )

        print("\nScans:")
        print("-" * 80)

        for row in cursor.fetchall():
            if isinstance(row, tuple):
                scan_id, scan_date, scan_path, duration, notes = row
            else:
                scan_id = row["id"]
                scan_date = row["scan_date"]
                scan_path = row["scan_path"]
                duration = row["duration_seconds"]
                notes = row["notes"]

            duration_str = f"{duration:.1f}s" if duration else "N/A"
            notes_str = f" - {notes}" if notes else ""
            print(f"#{scan_id:3d} {scan_date} {scan_path}")
            print(f"      Duration: {duration_str}{notes_str}")

            # Get file count
            cursor.execute(
                f"SELECT COUNT(*), SUM(size) FROM files WHERE scan_id = {scan_id}"
            )
            count_row = cursor.fetchone()
            file_count = count_row[0] if isinstance(count_row, tuple) else count_row[0]
            total_size = count_row[1] if isinstance(count_row, tuple) else count_row[1]

            if file_count:
                size_gb = (total_size or 0) / (1024**3)
                print(f"      Files: {file_count:,} ({size_gb:.2f} GB)")

            print()

    finally:
        cursor.close()
        conn.close()


def cmd_delete_scan(args):
    """Delete a scan and all associated data."""
    config = load_config()
    run_migrations(config)
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        # Get scan info first
        cursor.execute(
            f"SELECT scan_date, scan_path, notes FROM scans WHERE id = {args.scan_id}"
        )
        row = cursor.fetchone()

        if not row:
            print(f"Error: Scan #{args.scan_id} not found", file=sys.stderr)
            return 1

        if isinstance(row, tuple):
            scan_date, scan_path, notes = row
        else:
            scan_date = row["scan_date"]
            scan_path = row["scan_path"]
            notes = row["notes"]

        # Get file count for confirmation
        cursor.execute(
            f"SELECT COUNT(*), SUM(size) FROM files WHERE scan_id = {args.scan_id}"
        )
        count_row = cursor.fetchone()
        file_count = count_row[0] if isinstance(count_row, tuple) else count_row[0]
        total_size = count_row[1] if isinstance(count_row, tuple) else count_row[1]

        # Show what will be deleted
        print(f"\nScan #{args.scan_id}:")
        print(f"  Date: {scan_date}")
        print(f"  Path: {scan_path}")
        if notes:
            print(f"  Notes: {notes}")
        if file_count:
            size_gb = (total_size or 0) / (1024**3)
            print(f"  Files: {file_count:,} ({size_gb:.2f} GB)")

        # Confirmation prompt (unless --yes flag)
        if not args.yes:
            response = input("\nDelete this scan? [y/N]: ")
            if response.lower() not in ("y", "yes"):
                print("Cancelled.")
                return 0

        # Delete the scan (CASCADE will delete all related records)
        cursor.execute(f"DELETE FROM scans WHERE id = {args.scan_id}")
        conn.commit()

        print(f"✓ Deleted scan #{args.scan_id}")
        return 0

    except Exception as e:
        conn.rollback()
        print(f"Error deleting scan: {e}", file=sys.stderr)
        return 1
    finally:
        cursor.close()
        conn.close()


def cmd_webui(args):
    """Start the web UI server."""
    try:
        from diskindex.web.app import run_server
    except ImportError:
        print("Error: Web UI requires Flask", file=sys.stderr)
        print("Install with: uv pip install 'diskindex[web]'", file=sys.stderr)
        print("         or: pip install 'diskindex[web]'", file=sys.stderr)
        return 1

    print("Starting web UI...")
    run_server(host=args.host, port=args.port, debug=args.debug)
    return 0


def cmd_patterns_list(args):
    """List all ignore patterns."""
    config = load_config()
    run_migrations(config)
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, pattern, is_exception, applies_to, notes "
            "FROM ignore_patterns ORDER BY is_exception DESC, pattern"
        )

        print("\nIgnore Patterns:")
        print("-" * 80)

        for row in cursor.fetchall():
            if isinstance(row, tuple):
                pattern_id, pattern, is_exception, applies_to, notes = row
            else:
                pattern_id = row["id"]
                pattern = row["pattern"]
                is_exception = row["is_exception"]
                applies_to = row["applies_to"]
                notes = row["notes"]

            exception_flag = " [EXCEPTION]" if is_exception else ""
            notes_str = f" - {notes}" if notes else ""
            print(f"#{pattern_id:3d} {pattern}{exception_flag}{notes_str}")

    finally:
        cursor.close()
        conn.close()


def cmd_patterns_add(args):
    """Add a new ignore pattern."""
    config = load_config()
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        placeholder = "?" if config.backend == "sqlite" else "%s"
        cursor.execute(
            f"INSERT INTO ignore_patterns (pattern, is_exception, applies_to, notes) "
            f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
            (args.pattern, args.exception, args.applies_to, args.notes),
        )
        conn.commit()
        pattern_id = (
            cursor.lastrowid if config.backend == "sqlite" else cursor.fetchone()[0]
        )

        exception_flag = " (exception)" if args.exception else ""
        print(f"✓ Added pattern #{pattern_id}: {args.pattern}{exception_flag}")

        if args.apply:
            print("\nRe-applying patterns to existing scans...")
            from diskindex.patterns import reapply_patterns

            reapply_patterns(config, verbose=True)

    finally:
        cursor.close()
        conn.close()


def cmd_patterns_remove(args):
    """Remove an ignore pattern."""
    config = load_config()
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        # Check if pattern exists
        placeholder = "?" if config.backend == "sqlite" else "%s"
        cursor.execute(
            f"SELECT pattern FROM ignore_patterns WHERE id = {placeholder}", (args.id,)
        )
        row = cursor.fetchone()

        if not row:
            print(f"Error: Pattern #{args.id} not found", file=sys.stderr)
            return 1

        pattern = row[0] if isinstance(row, tuple) else row["pattern"]

        # Delete pattern
        cursor.execute(
            f"DELETE FROM ignore_patterns WHERE id = {placeholder}", (args.id,)
        )
        conn.commit()

        print(f"✓ Removed pattern #{args.id}: {pattern}")

        if args.apply:
            print("\nRe-applying patterns to existing scans...")
            from diskindex.patterns import reapply_patterns

            reapply_patterns(config, verbose=True)

    finally:
        cursor.close()
        conn.close()


def cmd_patterns_apply(args):
    """Re-apply ignore patterns to existing scans."""
    config = load_config()

    from diskindex.patterns import reapply_patterns

    print("Re-applying ignore patterns to existing files...")
    stats = reapply_patterns(config, scan_id=args.scan_id, verbose=True)

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Diskindex - File scanning and duplicate management system"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize database and configuration"
    )
    init_parser.add_argument(
        "-b",
        "--backend",
        choices=["sqlite", "sqlite3", "postgresql", "postgres", "pgsql", "pg"],
        default="sqlite",
        help="Database backend: sqlite (default), postgresql (aliases: pg, pgsql, postgres)",
    )
    init_parser.add_argument(
        "-d", "--database", help="Database name (PostgreSQL) or file path (SQLite)"
    )
    init_parser.add_argument(
        "-H", "--host", default="localhost", help="PostgreSQL host (default: localhost)"
    )
    init_parser.add_argument(
        "-p", "--port", type=int, default=5432, help="PostgreSQL port (default: 5432)"
    )
    init_parser.add_argument(
        "-U", "--user", default="postgres", help="PostgreSQL user (default: postgres)"
    )
    init_parser.add_argument(
        "-W",
        "--password",
        help="PostgreSQL password (prefer PGPASSWORD env var or ~/.pgpass)",
    )
    init_parser.add_argument(
        "--save-config",
        action="store_true",
        help="Save configuration to ~/.config/diskindex/config.json",
    )

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory")
    scan_parser.add_argument("path", help="Path to scan")
    scan_parser.add_argument("--notes", help="Notes about this scan")
    scan_parser.add_argument(
        "--no-hash", action="store_true", help="Skip MD5 hash computation"
    )
    scan_parser.add_argument(
        "--batch-size", type=int, default=1000, help="Batch size for database commits"
    )
    scan_parser.add_argument(
        "--one-filesystem",
        "-x",
        action="store_true",
        help="Do not cross filesystem boundaries during scan",
    )

    # List scans command
    list_parser = subparsers.add_parser("list-scans", help="List all scans")

    # Delete scan command
    delete_scan_parser = subparsers.add_parser(
        "delete-scan", help="Delete a scan and all associated data"
    )
    delete_scan_parser.add_argument(
        "scan_id", type=int, help="ID of the scan to delete"
    )
    delete_scan_parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompt"
    )

    # Patterns command with subcommands
    patterns_parser = subparsers.add_parser("patterns", help="Manage ignore patterns")
    patterns_subparsers = patterns_parser.add_subparsers(
        dest="patterns_command", help="Pattern operations"
    )

    # patterns list
    patterns_list_parser = patterns_subparsers.add_parser(
        "list", help="List all ignore patterns"
    )

    # patterns add
    patterns_add_parser = patterns_subparsers.add_parser(
        "add", help="Add a new ignore pattern"
    )
    patterns_add_parser.add_argument(
        "pattern", help="Pattern to add (e.g., '*.tmp' or '.git/')"
    )
    patterns_add_parser.add_argument(
        "--exception",
        "-e",
        action="store_true",
        help="Pattern is an exception (won't be ignored even if matches other patterns)",
    )
    patterns_add_parser.add_argument(
        "--applies-to",
        dest="applies_to",
        default="all",
        help="Pattern scope (default: all)",
    )
    patterns_add_parser.add_argument("--notes", help="Notes about this pattern")
    patterns_add_parser.add_argument(
        "--apply",
        action="store_true",
        help="Re-apply patterns to existing scans after adding",
    )

    # patterns remove
    patterns_remove_parser = patterns_subparsers.add_parser(
        "remove", help="Remove an ignore pattern"
    )
    patterns_remove_parser.add_argument("id", type=int, help="Pattern ID to remove")
    patterns_remove_parser.add_argument(
        "--apply",
        action="store_true",
        help="Re-apply patterns to existing scans after removing",
    )

    # patterns apply
    patterns_apply_parser = patterns_subparsers.add_parser(
        "apply", help="Re-apply ignore patterns to existing scans"
    )
    patterns_apply_parser.add_argument(
        "--scan-id", type=int, help="Apply to specific scan only (default: all scans)"
    )

    # Web UI command
    webui_parser = subparsers.add_parser("webui", help="Start web interface")
    webui_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)"
    )
    webui_parser.add_argument(
        "--port", type=int, default=5000, help="Port to bind to (default: 5000)"
    )
    webui_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    try:
        if args.command == "init":
            return cmd_init(args)
        elif args.command == "scan":
            cmd_scan(args)
            return 0
        elif args.command == "list-scans":
            cmd_list_scans(args)
            return 0
        elif args.command == "delete-scan":
            return cmd_delete_scan(args)
        elif args.command == "patterns":
            if args.patterns_command == "list":
                cmd_patterns_list(args)
                return 0
            elif args.patterns_command == "add":
                cmd_patterns_add(args)
                return 0
            elif args.patterns_command == "remove":
                return cmd_patterns_remove(args)
            elif args.patterns_command == "apply":
                return cmd_patterns_apply(args)
            else:
                patterns_parser.print_help()
                return 1
        elif args.command == "webui":
            return cmd_webui(args)
        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        if "--debug" in sys.argv or "-v" in sys.argv:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
