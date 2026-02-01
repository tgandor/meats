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

        # Manually delete related rows to avoid relying on DB-level foreign keys
        cursor.execute(f"DELETE FROM files WHERE scan_id = {args.scan_id}")
        cursor.execute(f"DELETE FROM directories WHERE scan_id = {args.scan_id}")
        cursor.execute(f"DELETE FROM volumes WHERE scan_id = {args.scan_id}")
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


def cmd_export(args):
    """Export database to SQLite file."""
    import sqlite3
    import os

    config = load_config()
    output_path = args.output

    # Check if output file exists
    if os.path.exists(output_path) and not args.force:
        print(f"Error: Output file '{output_path}' already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    try:
        print(f"Exporting database to {output_path}...")

        # Create SQLite export database
        if os.path.exists(output_path):
            os.remove(output_path)

        export_conn = sqlite3.connect(output_path)
        export_cursor = export_conn.cursor()

        # Copy data from source database
        source_conn = config.get_connection()
        source_cursor = source_conn.cursor()

        # For export, create tables based on source schema structure
        # Export scans
        source_cursor.execute("SELECT id, guid, scan_date, scan_path, notes FROM scans ORDER BY id")
        scans = source_cursor.fetchall()

        # Create scans table
        export_cursor.execute("""
            CREATE TABLE scans (
                id INTEGER PRIMARY KEY,
                guid TEXT UNIQUE,
                scan_date DATETIME,
                scan_path TEXT,
                notes TEXT
            )
        """)
        export_cursor.executemany(
            "INSERT INTO scans (id, guid, scan_date, scan_path, notes) VALUES (?, ?, ?, ?, ?)",
            scans
        )
        print(f"  Exported {len(scans)} scans")

        # Get volumes table structure from source
        if config.backend == "sqlite":
            source_cursor.execute("PRAGMA table_info(volumes)")
            volume_schema = [(row[1], row[2]) for row in source_cursor.fetchall()]
        else:
            source_cursor.execute(
                "SELECT column_name, data_type FROM information_schema.columns "
                "WHERE table_name = 'volumes' ORDER BY ordinal_position"
            )
            volume_schema = source_cursor.fetchall()

        # Create volumes table with exact source schema
        if volume_schema:
            volume_cols = [name for name, _ in volume_schema]
            col_defs = []
            for col_name, col_type in volume_schema:
                if col_name == 'id':
                    col_defs.append(f"{col_name} INTEGER PRIMARY KEY")
                else:
                    # Simplify type mapping for SQLite
                    sqlite_type = 'INTEGER' if 'INT' in col_type.upper() else 'TEXT'
                    col_defs.append(f"{col_name} {sqlite_type}")

            export_cursor.execute(f"CREATE TABLE volumes ({', '.join(col_defs)})")

            source_cursor.execute(f"SELECT {', '.join(volume_cols)} FROM volumes ORDER BY id")
            volumes = source_cursor.fetchall()
            if volumes:
                placeholders = ', '.join(['?'] * len(volume_cols))
                export_cursor.executemany(
                    f"INSERT INTO volumes ({', '.join(volume_cols)}) VALUES ({placeholders})",
                    volumes
                )
            print(f"  Exported {len(volumes)} volumes")
        else:
            print(f"  Exported 0 volumes")

        # Export directories
        export_cursor.execute("""
            CREATE TABLE directories (
                id INTEGER PRIMARY KEY,
                scan_id INTEGER,
                parent_id INTEGER,
                path TEXT
            )
        """)
        source_cursor.execute("SELECT id, scan_id, parent_id, path FROM directories ORDER BY id")
        directories = source_cursor.fetchall()
        if directories:
            export_cursor.executemany(
                "INSERT INTO directories (id, scan_id, parent_id, path) VALUES (?, ?, ?, ?)",
                directories
            )
        print(f"  Exported {len(directories)} directories")

        # Export files - check for column names
        if config.backend == "sqlite":
            source_cursor.execute("PRAGMA table_info(files)")
            file_cols_info = source_cursor.fetchall()
            file_cols = [row[1] for row in file_cols_info]
        else:
            source_cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'files' ORDER BY ordinal_position"
            )
            file_cols = [row[0] for row in source_cursor.fetchall()]

        # Map old/new column names
        hash_col = 'md5' if 'md5' in file_cols else 'md5_hash'

        # Create files table
        export_cursor.execute("""
            CREATE TABLE files (
                id INTEGER PRIMARY KEY,
                scan_id INTEGER,
                directory_id INTEGER,
                filename TEXT,
                size INTEGER,
                mtime DATETIME,
                md5 TEXT,
                ignored INTEGER DEFAULT 0
            )
        """)

        # Build SELECT with available columns
        file_select = f"SELECT id, scan_id, directory_id, filename, size, mtime, {hash_col}"
        if 'ignored' in file_cols:
            file_select += ", ignored"
        else:
            file_select += ", 0"  # Default value
        file_select += " FROM files ORDER BY id"

        source_cursor.execute(file_select)
        files = source_cursor.fetchall()
        if files:
            export_cursor.executemany(
                "INSERT INTO files (id, scan_id, directory_id, filename, size, mtime, md5, ignored) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                files
            )
        print(f"  Exported {len(files)} files")

        # Export patterns - check table name
        pattern_table = 'patterns' if config.backend == "sqlite" else 'patterns'
        try:
            source_cursor.execute(f"SELECT id, pattern, is_exception, applies_to, notes, created FROM {pattern_table} ORDER BY id")
            patterns = source_cursor.fetchall()
        except:
            # Try alternate table name
            try:
                source_cursor.execute(f"SELECT id, pattern, is_exception, applies_to, notes, created FROM ignore_patterns ORDER BY id")
                patterns = source_cursor.fetchall()
            except:
                patterns = []

        if patterns:
            export_cursor.execute("""
                CREATE TABLE patterns (
                    id INTEGER PRIMARY KEY,
                    pattern TEXT,
                    is_exception INTEGER,
                    applies_to TEXT,
                    notes TEXT,
                    created DATETIME
                )
            """)
            export_cursor.executemany(
                "INSERT INTO patterns (id, pattern, is_exception, applies_to, notes, created) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                patterns
            )
        print(f"  Exported {len(patterns)} patterns")

        # Export schema_version
        export_cursor.execute("""
            CREATE TABLE schema_version (
                version INTEGER PRIMARY KEY,
                updated DATETIME
            )
        """)
        source_cursor.execute("SELECT version, updated FROM schema_version")
        schema_versions = source_cursor.fetchall()
        if schema_versions:
            export_cursor.executemany(
                "INSERT INTO schema_version (version, updated) VALUES (?, ?)",
                schema_versions
            )

        export_conn.commit()
        export_conn.close()
        source_conn.close()

        # Show file size
        file_size = os.path.getsize(output_path)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"

        print(f"\n✓ Export complete: {output_path} ({size_str})")
        return 0

    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_import(args):
    """Import data from SQLite file into current database."""
    import sqlite3
    import os

    config = load_config()
    input_path = args.input

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return 1

    try:
        print(f"Importing from {input_path}...")

        # Open import database
        import_conn = sqlite3.connect(input_path)
        import_cursor = import_conn.cursor()

        # Open destination database
        dest_conn = config.get_connection()
        dest_cursor = dest_conn.cursor()

        # Check for duplicate scans by GUID
        import_cursor.execute("SELECT guid FROM scans WHERE guid IS NOT NULL AND guid != ''")
        import_guids = [row[0] for row in import_cursor.fetchall()]

        if import_guids:
            placeholder = "?" if config.backend == "sqlite" else "%s"
            placeholders = ",".join([placeholder] * len(import_guids))
            dest_cursor.execute(
                f"SELECT guid FROM scans WHERE guid IN ({placeholders})",
                import_guids
            )
            existing_guids = {row[0] for row in dest_cursor.fetchall()}

            if existing_guids:
                print(f"\n⚠️  Found {len(existing_guids)} scans already imported:")
                import_cursor.execute(
                    f"SELECT id, guid, scan_date, scan_path FROM scans WHERE guid IN ({','.join(['?'] * len(existing_guids))})",
                    list(existing_guids)
                )
                for scan_id, guid, scan_date, scan_path in import_cursor.fetchall():
                    print(f"  - Scan #{scan_id}: {scan_path} ({scan_date})")

                if not args.skip_duplicates:
                    print("\nThese scans will be skipped. Use --skip-duplicates to suppress this check.")
                    if not args.yes:
                        response = input("\nContinue with import? [y/N]: ")
                        if response.lower() not in ("y", "yes"):
                            print("Import cancelled.")
                            return 0
        else:
            existing_guids = set()

        # Import scans (excluding duplicates)
        import_cursor.execute("SELECT id, guid, scan_date, scan_path, notes FROM scans ORDER BY id")
        scans = import_cursor.fetchall()

        scan_id_map = {}  # old_id -> new_id
        imported_scans = 0
        skipped_scans = 0

        for old_id, guid, scan_date, scan_path, notes in scans:
            if guid and guid in existing_guids:
                skipped_scans += 1
                continue

            placeholder = "?" if config.backend == "sqlite" else "%s"
            dest_cursor.execute(
                f"INSERT INTO scans (guid, scan_date, scan_path, notes) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
                (guid, scan_date, scan_path, notes)
            )

            if config.backend == "sqlite":
                new_id = dest_cursor.lastrowid
            else:
                dest_cursor.execute("SELECT lastval()")
                new_id = dest_cursor.fetchone()[0]

            scan_id_map[old_id] = new_id
            imported_scans += 1

        print(f"  Imported {imported_scans} scans (skipped {skipped_scans} duplicates)")

        if not scan_id_map:
            print("\n✓ No new scans to import.")
            dest_conn.close()
            import_conn.close()
            return 0

        # Import volumes - handle dynamic schema
        import_cursor.execute("PRAGMA table_info(volumes)")
        import_volume_cols = [row[1] for row in import_cursor.fetchall()]

        # Get destination volume columns
        if config.backend == "sqlite":
            dest_cursor.execute("PRAGMA table_info(volumes)")
            dest_volume_cols = {row[1] for row in dest_cursor.fetchall()}
        else:
            dest_cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'volumes'"
            )
            dest_volume_cols = {row[0] for row in dest_cursor.fetchall()}

        # Map columns from import to destination
        col_map = {
            'total_space': 'total_size',  # Map if dest has total_size
            'total_size': 'total_space',  # Map if dest has total_space
        }

        # Build column list for SELECT and INSERT
        select_cols = []
        insert_cols = []
        for col in import_volume_cols:
            if col == 'id':
                continue  # Skip id, will be auto-generated

            # Try direct match first
            if col in dest_volume_cols:
                select_cols.append(col)
                insert_cols.append(col)
            elif col in col_map and col_map[col] in dest_volume_cols:
                # Use mapped column name
                select_cols.append(col)
                insert_cols.append(col_map[col])

        if select_cols:
            import_cursor.execute(f"SELECT scan_id, {', '.join(select_cols[1:])} FROM volumes ORDER BY id")
            volumes = import_cursor.fetchall()

            imported_volumes = 0
            placeholder = "?" if config.backend == "sqlite" else "%s"
            placeholders = ', '.join([placeholder] * len(insert_cols))

            for row in volumes:
                scan_id = row[0]
                if scan_id not in scan_id_map:
                    continue  # Skip volumes for duplicate scans

                new_scan_id = scan_id_map[scan_id]
                values = [new_scan_id] + list(row[1:])

                dest_cursor.execute(
                    f"INSERT INTO volumes ({', '.join(insert_cols)}) VALUES ({placeholders})",
                    values
                )
                imported_volumes += 1
        else:
            imported_volumes = 0

        print(f"  Imported {imported_volumes} volumes")

        # Import directories - handle name column
        import_cursor.execute("PRAGMA table_info(directories)")
        import_dir_cols = {row[1] for row in import_cursor.fetchall()}

        # Check if destination needs name column
        if config.backend == "sqlite":
            dest_cursor.execute("PRAGMA table_info(directories)")
            dest_dir_cols = {row[1] for row in dest_cursor.fetchall()}
        else:
            dest_cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'directories'"
            )
            dest_dir_cols = {row[0] for row in dest_cursor.fetchall()}

        dest_needs_name = 'name' in dest_dir_cols
        import_has_name = 'name' in import_dir_cols

        # Build SELECT query
        if import_has_name:
            import_cursor.execute("SELECT id, scan_id, parent_id, path, name FROM directories ORDER BY id")
        else:
            import_cursor.execute("SELECT id, scan_id, parent_id, path FROM directories ORDER BY id")

        directories = import_cursor.fetchall()

        dir_id_map = {}  # old_id -> new_id
        dir_to_scan_map = {}  # new_directory_id -> scan_id
        imported_dirs = 0
        placeholder = "?" if config.backend == "sqlite" else "%s"

        for row in directories:
            if import_has_name:
                old_id, scan_id, parent_id, path, name = row
            else:
                old_id, scan_id, parent_id, path = row
                # Extract name from path
                name = path.rstrip('/').split('/')[-1] if path else ''

            if scan_id not in scan_id_map:
                continue  # Skip directories for duplicate scans

            new_scan_id = scan_id_map[scan_id]
            new_parent_id = dir_id_map.get(parent_id) if parent_id else None

            if dest_needs_name:
                dest_cursor.execute(
                    f"INSERT INTO directories (scan_id, parent_id, path, name) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
                    (new_scan_id, new_parent_id, path, name)
                )
            else:
                dest_cursor.execute(
                    f"INSERT INTO directories (scan_id, parent_id, path) VALUES ({placeholder}, {placeholder}, {placeholder})",
                    (new_scan_id, new_parent_id, path)
                )

            if config.backend == "sqlite":
                new_id = dest_cursor.lastrowid
            else:
                dest_cursor.execute("SELECT lastval()")
                new_id = dest_cursor.fetchone()[0]

            dir_id_map[old_id] = new_id
            dir_to_scan_map[new_id] = new_scan_id  # Track scan_id for files
            imported_dirs += 1

        print(f"  Imported {imported_dirs} directories")

        # Import files in batches - handle column name differences
        import_cursor.execute("PRAGMA table_info(files)")
        import_file_cols = {row[1] for row in import_cursor.fetchall()}

        # Check destination columns
        if config.backend == "sqlite":
            dest_cursor.execute("PRAGMA table_info(files)")
            dest_file_cols = {row[1] for row in dest_cursor.fetchall()}
        else:
            dest_cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'files'"
            )
            dest_file_cols = {row[0] for row in dest_cursor.fetchall()}

        # Determine hash column names
        import_hash_col = 'md5' if 'md5' in import_file_cols else 'md5_hash'
        dest_hash_col = 'md5' if 'md5' in dest_file_cols else 'md5_hash'

        # Check for scan_id vs directory_id
        import_has_scan_id = 'scan_id' in import_file_cols
        dest_has_scan_id = 'scan_id' in dest_file_cols

        # Build SELECT query
        if import_has_scan_id:
            import_cursor.execute(f"SELECT scan_id, directory_id, filename, size, mtime, {import_hash_col}, ignored FROM files ORDER BY id")
        else:
            import_cursor.execute(f"SELECT directory_id, filename, size, mtime, {import_hash_col}, ignored FROM files ORDER BY id")

        batch_size = args.batch_size if hasattr(args, 'batch_size') else 1000
        files_batch = []
        imported_files = 0
        placeholder = "?" if config.backend == "sqlite" else "%s"

        for row in import_cursor:
            if import_has_scan_id:
                scan_id, directory_id, filename, size, mtime, hash_val, ignored = row
            else:
                directory_id, filename, size, mtime, hash_val, ignored = row

            if directory_id not in dir_id_map:
                continue  # Skip files for duplicate scans

            new_directory_id = dir_id_map[directory_id]

            # Build row for insertion
            if dest_has_scan_id:
                # Look up scan_id from directory mapping
                file_scan_id = dir_to_scan_map.get(new_directory_id)
                if not file_scan_id:
                    # Fallback: query the directory
                    dest_cursor.execute(f"SELECT scan_id FROM directories WHERE id = {placeholder}", (new_directory_id,))
                    result = dest_cursor.fetchone()
                    file_scan_id = result[0] if result else None

                if file_scan_id:
                    files_batch.append((file_scan_id, new_directory_id, filename, size, mtime, hash_val, ignored))
                else:
                    continue  # Skip if we can't determine scan_id
            else:
                files_batch.append((new_directory_id, filename, size, mtime, hash_val, ignored))

            if len(files_batch) >= batch_size:
                if dest_has_scan_id:
                    dest_cursor.executemany(
                        f"INSERT INTO files (scan_id, directory_id, filename, size, mtime, {dest_hash_col}, ignored) "
                        f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
                        files_batch
                    )
                else:
                    dest_cursor.executemany(
                        f"INSERT INTO files (directory_id, filename, size, mtime, {dest_hash_col}, ignored) "
                        f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
                        files_batch
                    )
                imported_files += len(files_batch)
                files_batch = []
                dest_conn.commit()
                print(f"  Imported {imported_files} files...", end='\r')

        # Insert remaining files
        if files_batch:
            if dest_has_scan_id:
                dest_cursor.executemany(
                    f"INSERT INTO files (scan_id, directory_id, filename, size, mtime, {dest_hash_col}, ignored) "
                    f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
                    files_batch
                )
            else:
                dest_cursor.executemany(
                    f"INSERT INTO files (directory_id, filename, size, mtime, {dest_hash_col}, ignored) "
                    f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
                    files_batch
                )
            imported_files += len(files_batch)

        print(f"  Imported {imported_files} files      ")

        # Import patterns (merge, skip duplicates) - handle table name
        try:
            import_cursor.execute(
                "SELECT pattern, is_exception, applies_to, notes FROM patterns ORDER BY id"
            )
            patterns = import_cursor.fetchall()
        except sqlite3.OperationalError:
            # Try alternate table name
            try:
                import_cursor.execute(
                    "SELECT pattern, is_exception, applies_to, notes FROM ignore_patterns ORDER BY id"
                )
                patterns = import_cursor.fetchall()
            except:
                patterns = []

        # Determine destination table name
        if config.backend == "sqlite":
            dest_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('patterns', 'ignore_patterns')")
            dest_pattern_table = dest_cursor.fetchone()
            dest_pattern_table = dest_pattern_table[0] if dest_pattern_table else 'patterns'
        else:
            dest_pattern_table = 'patterns'

        # Get existing patterns
        dest_cursor.execute(f"SELECT pattern FROM {dest_pattern_table}")
        existing_patterns = {row[0] for row in dest_cursor.fetchall()}

        imported_patterns = 0
        for pattern, is_exception, applies_to, notes in patterns:
            if pattern in existing_patterns:
                continue  # Skip duplicate patterns

            placeholder = "?" if config.backend == "sqlite" else "%s"
            if config.backend == "sqlite":
                dest_cursor.execute(
                    f"INSERT INTO {dest_pattern_table} (pattern, is_exception, applies_to, notes, created) "
                    f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, datetime('now'))",
                    (pattern, is_exception, applies_to, notes)
                )
            else:
                dest_cursor.execute(
                    f"INSERT INTO {dest_pattern_table} (pattern, is_exception, applies_to, notes, created) "
                    f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, NOW())",
                    (pattern, is_exception, applies_to, notes)
                )
            imported_patterns += 1

        print(f"  Imported {imported_patterns} patterns")

        dest_conn.commit()
        dest_conn.close()
        import_conn.close()

        print(f"\n✓ Import complete!")
        return 0

    except Exception as e:
        if 'dest_conn' in locals():
            dest_conn.rollback()
        print(f"Error during import: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_migrate(args):
    """Run database migrations or set schema version."""
    config = load_config()
    conn = config.get_connection()
    cursor = conn.cursor()

    try:
        # Get current schema version
        cursor.execute("SELECT MAX(version) FROM schema_version")
        result = cursor.fetchone()
        current_version = result[0] if result and result[0] else 0

        print(f"Current schema version: {current_version}")

        if args.set_version is not None:
            # Set schema version manually (for workarounds)
            new_version = args.set_version
            print(f"\n⚠️  Manually setting schema version to {new_version}")
            print(
                "This is a workaround and should only be used if you know what you're doing!"
            )

            if not args.yes:
                response = input(f"\nSet schema version to {new_version}? [y/N]: ")
                if response.lower() not in ("y", "yes"):
                    print("Cancelled.")
                    return 0

            # Delete all existing schema versions and insert new one
            cursor.execute("DELETE FROM schema_version")

            if config.backend == "sqlite":
                cursor.execute(
                    "INSERT INTO schema_version (version, updated) VALUES (?, datetime('now'))",
                    (new_version,),
                )
            else:  # postgresql
                cursor.execute(
                    "INSERT INTO schema_version (version, updated) VALUES (%s, NOW())",
                    (new_version,),
                )
            conn.commit()
            print(f"✓ Schema version set to {new_version}")

        # Run migrations
        print("\nRunning migrations...")
        cursor.close()
        conn.close()

        run_migrations(config)
        print("✓ Migrations complete")

        # Show final version
        conn = config.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(version) FROM schema_version")
        result = cursor.fetchone()
        final_version = result[0] if result and result[0] else 0
        print(f"\nFinal schema version: {final_version}")

        return 0

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}", file=sys.stderr)
        return 1
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

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export database to SQLite file"
    )
    export_parser.add_argument(
        "output", help="Output SQLite file path"
    )
    export_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing output file"
    )

    # Import command
    import_parser = subparsers.add_parser(
        "import", help="Import data from SQLite file"
    )
    import_parser.add_argument(
        "input", help="Input SQLite file path"
    )
    import_parser.add_argument(
        "--batch-size", type=int, default=1000, help="Batch size for file imports"
    )
    import_parser.add_argument(
        "--skip-duplicates", action="store_true",
        help="Skip duplicate scans without prompting"
    )
    import_parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip all confirmation prompts"
    )

    # Migrate command
    migrate_parser = subparsers.add_parser(
        "migrate", help="Run database migrations or set schema version"
    )
    migrate_parser.add_argument(
        "--set-version",
        type=int,
        metavar="VERSION",
        help="Manually set schema version (for workarounds only!)",
    )
    migrate_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompt when setting version",
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
        elif args.command == "export":
            return cmd_export(args)
        elif args.command == "import":
            return cmd_import(args)
        elif args.command == "migrate":
            return cmd_migrate(args)
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
