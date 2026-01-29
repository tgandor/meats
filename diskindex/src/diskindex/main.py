"""Main CLI interface for diskindex."""

import argparse
import json
import sys

from diskindex.config import (
    load_config,
    save_config,
    ensure_data_directory,
    get_config_path,
    get_default_db_path,
)
from diskindex.database import initialize_database, install_default_ignore_patterns
from diskindex.scanner import Scanner


def cmd_init(args):
    """Initialize database and configuration."""
    config_path = get_config_path()
    db_path = get_default_db_path()

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
        print(f"\nConfig:   Not saved (use --save-config to persist)")

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

    # Create scanner
    scanner = Scanner(config, compute_hash=not args.no_hash, batch_size=args.batch_size)

    # Perform scan
    scan_id = scanner.scan(args.path, notes=args.notes)
    print(f"\nScan #{scan_id} completed successfully!")


def cmd_list_scans(args):
    """List all scans."""
    config = load_config()
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
        "--backend",
        choices=["sqlite", "postgresql"],
        default="sqlite",
        help="Database backend (default: sqlite)",
    )
    init_parser.add_argument(
        "-d", "--database", help="Database name (PostgreSQL) or file path (SQLite)"
    )
    init_parser.add_argument(
        "--host", default="localhost", help="PostgreSQL host (default: localhost)"
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

    # List scans command
    list_parser = subparsers.add_parser("list-scans", help="List all scans")

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
