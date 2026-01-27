"""Main CLI interface for diskindex."""

import argparse
import sys

from config import load_config, save_config, ensure_data_directory
from database import initialize_database, install_default_ignore_patterns
from scanner import Scanner


def cmd_init(args):
    """Initialize database and configuration."""
    config = load_config()

    # Override with command-line arguments
    if args.backend:
        config.backend = args.backend
    if args.database:
        config.database = args.database
    if args.host:
        config.host = args.host
    if args.port:
        config.port = args.port
    if args.user:
        config.user = args.user

    # Ensure data directory exists
    ensure_data_directory(config)

    # Initialize database
    print(f"Initializing {config.backend} database...")
    initialize_database(config)

    # Install default ignore patterns
    print("Installing default ignore patterns...")
    install_default_ignore_patterns(config)

    # Save configuration
    if args.save_config:
        save_config(config)
        print(f"Configuration saved")

    print("Database initialized successfully!")


def cmd_scan(args):
    """Perform a full scan."""
    config = load_config()

    # Ensure database is initialized
    ensure_data_directory(config)
    initialize_database(config)

    # Create scanner
    scanner = Scanner(
        config,
        compute_hash=not args.no_hash,
        batch_size=args.batch_size
    )

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
                scan_id = row['id']
                scan_date = row['scan_date']
                scan_path = row['scan_path']
                duration = row['duration_seconds']
                notes = row['notes']

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

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize database and configuration')
    init_parser.add_argument('--backend', choices=['sqlite', 'postgresql'], help='Database backend')
    init_parser.add_argument('--database', help='Database name or path')
    init_parser.add_argument('--host', help='Database host (PostgreSQL)')
    init_parser.add_argument('--port', type=int, help='Database port (PostgreSQL)')
    init_parser.add_argument('--user', help='Database user (PostgreSQL)')
    init_parser.add_argument('--save-config', action='store_true', help='Save configuration to file')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a directory')
    scan_parser.add_argument('path', help='Path to scan')
    scan_parser.add_argument('--notes', help='Notes about this scan')
    scan_parser.add_argument('--no-hash', action='store_true', help='Skip MD5 hash computation')
    scan_parser.add_argument('--batch-size', type=int, default=1000, help='Batch size for database commits')

    # List scans command
    list_parser = subparsers.add_parser('list-scans', help='List all scans')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    try:
        if args.command == 'init':
            cmd_init(args)
        elif args.command == 'scan':
            cmd_scan(args)
        elif args.command == 'list-scans':
            cmd_list_scans(args)
        else:
            parser.print_help()
            return 1

        return 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())
