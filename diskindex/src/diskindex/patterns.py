"""Pattern re-application utilities for diskindex.

Provides functions to re-apply ignore patterns to existing scanned files,
marking them as ignored or un-ignored based on current pattern rules.
"""

import pathlib
from typing import Optional

from diskindex.database import DatabaseConfig
from diskindex.scanner import should_ignore


def reapply_patterns(
    config: DatabaseConfig, scan_id: Optional[int] = None, verbose: bool = True
) -> dict:
    """Re-apply ignore patterns to files in database.

    Args:
        config: Database configuration
        scan_id: Optional scan ID to limit re-application (None = all scans)
        verbose: Print progress messages

    Returns:
        Dictionary with statistics: {'marked_ignored': int, 'marked_visible': int, 'total_checked': int}
    """
    conn = config.get_connection()
    cursor = conn.cursor()

    stats = {
        "marked_ignored": 0,
        "marked_visible": 0,
        "total_checked": 0,
    }

    try:
        # Load current ignore patterns
        cursor.execute(
            "SELECT pattern, is_exception FROM ignore_patterns ORDER BY is_exception ASC"
        )

        regular_patterns = []
        exception_patterns = []

        for row in cursor.fetchall():
            pattern = row[0] if isinstance(row, tuple) else row["pattern"]
            is_exception = row[1] if isinstance(row, tuple) else row["is_exception"]

            if is_exception:
                exception_patterns.append(pattern)
            else:
                regular_patterns.append(pattern)

        if verbose:
            print(
                f"Loaded {len(regular_patterns)} ignore patterns, {len(exception_patterns)} exceptions"
            )

        # Build query to get all files (or files from specific scan)
        where_clause = ""
        params = []
        if scan_id is not None:
            placeholder = "?" if config.backend == "sqlite" else "%s"
            where_clause = f"WHERE files.scan_id = {placeholder}"
            params = [scan_id]

        # Get files with their directory paths
        sql = f"""
            SELECT files.id, files.filename, directories.path, scans.scan_path, files.ignored
            FROM files
            JOIN directories ON files.directory_id = directories.id
            JOIN scans ON files.scan_id = scans.id
            {where_clause}
        """

        cursor.execute(sql, params)
        files = cursor.fetchall()

        if verbose:
            print(f"Checking {len(files)} files...")

        # Check each file against patterns
        updates_ignored = []
        updates_visible = []
        placeholder = "?" if config.backend == "sqlite" else "%s"

        for row in files:
            if isinstance(row, tuple):
                file_id, filename, dir_path, scan_path, currently_ignored = row
            else:
                file_id = row["id"]
                filename = row["filename"]
                dir_path = row["path"]
                scan_path = row["scan_path"]
                currently_ignored = row["ignored"]

            # Build relative path for pattern matching
            full_path = pathlib.Path(dir_path) / filename
            try:
                rel_path = full_path.relative_to(scan_path)
            except ValueError:
                rel_path = full_path

            # Check if file should be ignored
            should_be_ignored = should_ignore(
                str(rel_path), regular_patterns, exception_patterns
            )

            # Update if status changed
            if should_be_ignored and not currently_ignored:
                updates_ignored.append((file_id,))
                stats["marked_ignored"] += 1
            elif not should_be_ignored and currently_ignored:
                updates_visible.append((file_id,))
                stats["marked_visible"] += 1

            stats["total_checked"] += 1

        # Batch update files
        if updates_ignored:
            cursor.executemany(
                f"UPDATE files SET ignored = 1 WHERE id = {placeholder}",
                updates_ignored,
            )

        if updates_visible:
            cursor.executemany(
                f"UPDATE files SET ignored = 0 WHERE id = {placeholder}",
                updates_visible,
            )

        conn.commit()

        if verbose:
            print(f"✓ Marked {stats['marked_ignored']} files as ignored")
            print(f"✓ Marked {stats['marked_visible']} files as visible")
            print(f"✓ Total checked: {stats['total_checked']}")

        return stats

    finally:
        cursor.close()
        conn.close()
