"""File scanner for diskindex.

Scans directories recursively, computes MD5 hashes, builds directory hierarchy,
and stores results in database with progress tracking and batch commits.
"""

import hashlib
import os
import pathlib
import platform
import time
import uuid
from datetime import datetime
from fnmatch import fnmatch
from typing import Optional, Union

try:
    from tqdm import tqdm

    show = tqdm.write
except ImportError:
    tqdm = lambda x, **kwargs: x  # identity function
    show = print

from diskindex.database import DatabaseConfig
from diskindex.models import Scan, Volume


def compute_md5(file_path: pathlib.Path) -> str:
    """Compute MD5 hash of a file."""
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            # Read in 64KB chunks for efficiency
            for chunk in iter(lambda: f.read(65536), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except (OSError, IOError) as e:
        show(f"Warning: Cannot read {file_path}: {e}")
        return ""


def get_volume_info(path: pathlib.Path) -> Optional[Volume]:
    """Get volume information for a path."""
    volume = Volume()

    try:
        if platform.system() == "Windows":
            # Get drive letter
            drive_letter = os.path.splitdrive(str(path))[0]
            letter = None if not drive_letter else drive_letter.rstrip(":")

            if drive_letter:
                volume.mount_point = drive_letter + "\\"
                volume.device_path = drive_letter

                # Try to get volume label and drive type using PowerShell
                try:
                    import subprocess

                    ps_command = f"""
                    $vol = Get-Volume -DriveLetter '{letter}'
                    $vol.FileSystemLabel
                    $vol.DriveType
                    """
                    output = (
                        subprocess.check_output(
                            ["powershell", "-Command", ps_command],
                            text=True,
                            stderr=subprocess.DEVNULL,
                        )
                        .strip()
                        .split("\n")
                    )
                    if len(output) >= 1 and output[0]:
                        volume.label = output[0].strip()
                    if len(output) >= 2 and output[1]:
                        volume.drive_type = output[1].strip()
                except Exception:
                    pass

                # Get filesystem info and free space
                try:
                    import shutil

                    usage = shutil.disk_usage(volume.mount_point)
                    volume.total_size = usage.total
                    volume.free_space = usage.free
                except Exception:
                    pass

                # Try to get volume serial number as UUID
                try:
                    import subprocess

                    ps_command = f"(Get-Volume -DriveLetter '{letter}').UniqueId"
                    uuid = subprocess.check_output(
                        ["powershell", "-Command", ps_command],
                        text=True,
                        stderr=subprocess.DEVNULL,
                    ).strip()
                    if uuid:
                        volume.uuid = uuid
                except Exception:
                    pass
        else:
            # Unix-like systems - find mount point
            current = path.resolve()
            while current != current.parent:
                if current.is_mount():
                    volume.mount_point = str(current)
                    break
                current = current.parent
            else:
                volume.mount_point = "/"

            # Try to get filesystem type and mount options from /proc/mounts
            try:
                with open("/proc/mounts", "r") as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) >= 4 and parts[1] == volume.mount_point:
                            volume.device_path = parts[0]
                            volume.filesystem_type = parts[2]
                            volume.mount_options = parts[3]
                            break
            except Exception:
                pass

            # Get total size and free space
            try:
                import shutil

                usage = shutil.disk_usage(volume.mount_point)
                volume.total_size = usage.total
                volume.free_space = usage.free
            except Exception:
                pass

            # Try to get UUID using blkid
            if volume.device_path:
                try:
                    import subprocess

                    output = subprocess.check_output(
                        ["blkid", "-s", "UUID", "-o", "value", volume.device_path],
                        text=True,
                        stderr=subprocess.DEVNULL,
                    ).strip()
                    if output:
                        volume.uuid = output
                except Exception:
                    # blkid may not be available or require sudo
                    pass

        return volume
    except Exception as e:
        show(f"Warning: Cannot get volume info for {path}: {e}")
        return None


def load_ignore_patterns(conn) -> tuple[list[str], list[str]]:
    """Load ignore patterns from database.

    Returns:
        tuple of (regular_patterns, exception_patterns)
    """
    cursor = conn.cursor()

    try:
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

        return regular_patterns, exception_patterns
    finally:
        cursor.close()


def should_ignore(
    path: str, regular_patterns: list[str], exception_patterns: list[str]
) -> bool:
    """Check if path should be ignored based on patterns.

    Args:
        path: Path to check (relative or absolute)
        regular_patterns: Patterns to ignore
        exception_patterns: Patterns that are exceptions to ignore rules

    Returns:
        True if should be ignored, False otherwise
    """
    # Normalize path for matching
    normalized = path.replace("\\", "/")

    # Check exception patterns first (highest priority)
    for pattern in exception_patterns:
        if pattern.endswith("/"):
            # Directory pattern
            if f"/{pattern}" in f"/{normalized}/" or normalized.endswith(
                pattern.rstrip("/")
            ):
                return False
        else:
            # File pattern
            if fnmatch(os.path.basename(normalized), pattern):
                return False
            if fnmatch(normalized, pattern):
                return False

    # Check regular ignore patterns
    for pattern in regular_patterns:
        if pattern.endswith("/"):
            # Directory pattern
            if f"/{pattern}" in f"/{normalized}/" or normalized.endswith(
                pattern.rstrip("/")
            ):
                return True
        else:
            # File pattern
            if fnmatch(os.path.basename(normalized), pattern):
                return True
            if fnmatch(normalized, pattern):
                return True

    return False


class Scanner:
    """File scanner that walks directory trees and stores metadata in database."""

    def __init__(
        self,
        config: DatabaseConfig,
        compute_hash: bool = True,
        batch_size: int = 1000,
        one_filesystem: bool = False,
    ):
        """Initialize scanner.

        Args:
            config: Database configuration
            compute_hash: Whether to compute MD5 hashes
            batch_size: Number of files to process before committing to database
            one_filesystem: If True, don't cross filesystem boundaries
        """
        self.config = config
        self.compute_hash = compute_hash
        self.batch_size = batch_size
        self.one_filesystem = one_filesystem
        self.root_device = None  # Will be set during scan
        self.stats: dict[str, int | float] = {
            "files": 0,
            "dirs": 0,
            "bytes": 0,
            "ignored": 0,
            "errors": 0,
        }
        self.directory_cache = {}  # path -> directory_id

    @property
    def ph(self) -> str:
        """DB-API parameter placeholder."""
        return self.config.ph

    def scan(
        self, scan_path: Union[str, pathlib.Path], notes: Optional[str] = None
    ) -> int:
        """Scan a directory tree.

        Args:
            scan_path: Path to scan
            notes: Optional notes about this scan

        Returns:
            Scan ID
        """
        scan_path = pathlib.Path(scan_path).resolve()

        if not scan_path.exists():
            raise ValueError(f"Path does not exist: {scan_path}")

        if not scan_path.is_dir():
            raise ValueError(f"Path is not a directory: {scan_path}")

        show(f"Starting scan of: {scan_path}")
        start_time = time.time()

        # Store root device for filesystem boundary check
        if self.one_filesystem:
            self.root_device = scan_path.stat().st_dev
            show("One-filesystem mode: will not cross filesystem boundaries")

        conn = self.config.get_connection()
        cursor = conn.cursor()

        try:
            # Create scan record with unique GUID
            scan_guid = uuid.uuid4().hex
            scan = Scan(scan_date=datetime.now(), scan_path=str(scan_path), notes=notes)

            cursor.execute(
                f"INSERT INTO scans (guid, scan_date, scan_path, notes) "
                f"VALUES ({self.ph}, {self.ph}, {self.ph}, {self.ph})",
                (scan_guid, scan.scan_date, scan.scan_path, scan.notes),
            )

            if self.config.backend == "sqlite":
                scan_id = cursor.lastrowid
            else:
                cursor.execute("SELECT lastval()")
                result = cursor.fetchone()
                scan_id = result[0] if result else 0

            if not scan_id:
                raise RuntimeError("Failed to get scan ID")

            conn.commit()
            show(f"Created scan #{scan_id}")

            # Get volume info
            volume = get_volume_info(scan_path)
            if volume:
                volume.scan_id = scan_id
                cursor.execute(
                    f"INSERT INTO volumes (scan_id, label, filesystem_type, mount_point, "
                    f"device_path, total_size, free_space, mount_options, uuid, drive_type) "
                    f"VALUES ({self.ph}, {self.ph}, {self.ph}, {self.ph}, "
                    f"{self.ph}, {self.ph}, {self.ph}, {self.ph}, {self.ph}, {self.ph})",
                    (
                        volume.scan_id,
                        volume.label,
                        volume.filesystem_type,
                        volume.mount_point,
                        volume.device_path,
                        volume.total_size,
                        volume.free_space,
                        volume.mount_options,
                        volume.uuid,
                        volume.drive_type,
                    ),
                )
                conn.commit()
                show(
                    f"Detected volume: {volume.mount_point} ({volume.label or 'no label'})"
                )

            # Load ignore patterns
            regular_patterns, exception_patterns = load_ignore_patterns(conn)
            show(
                f"Loaded {len(regular_patterns)} ignore patterns "
                f"({len(exception_patterns)} exceptions)"
            )

            # Walk directory tree
            self._scan_directory(
                conn,
                scan_id,
                scan_path,
                scan_path,
                None,
                regular_patterns,
                exception_patterns,
            )

            # Update scan duration
            duration = time.time() - start_time
            cursor.execute(
                f"UPDATE scans SET duration_seconds = {self.ph} WHERE id = {self.ph}",
                (duration, scan_id),
            )
            conn.commit()

            show("\nScan complete!")
            show(f"  Files: {self.stats['files']:,}")
            show(f"  Directories: {self.stats['dirs']:,}")
            show(
                f"  Total size: {self.stats['bytes']:,} bytes "
                f"({self.stats['bytes'] / (1024**3):.2f} GB)"
            )
            show(f"  Ignored: {self.stats['ignored']:,}")
            show(f"  Errors: {self.stats['errors']:,}")
            show(f"  Duration: {duration:.1f} seconds")

            return scan_id

        except Exception as e:
            conn.rollback()
            show(f"Error during scan: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def _get_or_create_directory(
        self,
        cursor,
        conn,
        scan_id: int,
        dir_path: pathlib.Path,
        root_path: pathlib.Path,
        parent_id: Optional[int],
    ) -> int:
        """Get or create directory record.

        Returns:
            directory_id
        """
        path_str = str(dir_path)

        # Check cache first
        if path_str in self.directory_cache:
            return self.directory_cache[path_str]

        # Try to find existing directory
        cursor.execute(
            f"SELECT id FROM directories WHERE scan_id = {self.ph} AND path = {self.ph}",
            (scan_id, path_str),
        )
        result = cursor.fetchone()

        if result:
            dir_id = result[0] if isinstance(result, tuple) else result["id"]
        else:
            # Create new directory record
            cursor.execute(
                f"INSERT INTO directories (scan_id, parent_id, path, name) "
                f"VALUES ({self.ph}, {self.ph}, {self.ph}, {self.ph})",
                (scan_id, parent_id, path_str, dir_path.name or str(dir_path)),
            )

            if self.config.backend == "sqlite":
                dir_id = cursor.lastrowid
            else:
                cursor.execute("SELECT lastval()")
                dir_id = cursor.fetchone()[0]

            self.stats["dirs"] += 1

        # Cache the result
        self.directory_cache[path_str] = dir_id

        return dir_id

    def _scan_directory(
        self,
        conn,
        scan_id: int,
        dir_path: pathlib.Path,
        root_path: pathlib.Path,
        parent_id: Optional[int],
        regular_patterns: list[str],
        exception_patterns: list[str],
    ) -> None:
        """Recursively scan a directory.

        Args:
            conn: Database connection
            scan_id: Scan ID
            dir_path: Current directory path
            root_path: Root scan path
            parent_id: Parent directory ID
            regular_patterns: Ignore patterns
            exception_patterns: Exception patterns
        """
        cursor = conn.cursor()

        try:
            # Get or create directory record
            dir_id = self._get_or_create_directory(
                cursor, conn, scan_id, dir_path, root_path, parent_id
            )

            # List directory contents
            try:
                entries = list(dir_path.iterdir())
            except (OSError, PermissionError) as e:
                show(f"Warning: Cannot read directory {dir_path}: {e}")
                self.stats["errors"] += 1
                return

            # Process files and subdirectories
            file_batch = []

            for entry in tqdm(entries, desc=str(dir_path.name), leave=False):
                # Get relative path for pattern matching
                try:
                    rel_path = entry.relative_to(root_path)
                except ValueError:
                    rel_path = entry

                # Check if should be ignored
                if should_ignore(str(rel_path), regular_patterns, exception_patterns):
                    self.stats["ignored"] += 1
                    continue

                # Check file type with error handling for Windows issues
                try:
                    is_symlink = entry.is_symlink()
                    is_dir = entry.is_dir()
                    is_file = entry.is_file()
                except OSError as e:
                    # Handle Windows errors like winerror 1920 (can't access file)
                    show(f"Warning: Cannot access {entry}: {e}")
                    self.stats["errors"] += 1
                    continue

                if is_symlink:
                    # Skip symlinks to avoid loops
                    continue

                if is_dir:
                    # Check filesystem boundary if one_filesystem is enabled
                    if self.one_filesystem and self.root_device is not None:
                        try:
                            entry_device = entry.stat().st_dev
                            if entry_device != self.root_device:
                                show(f"Skipping {entry}: different filesystem")
                                self.stats["ignored"] += 1
                                continue
                        except (OSError, PermissionError):
                            pass  # If we can't stat it, let the recursive call handle the error

                    # Recursively scan subdirectory
                    self._scan_directory(
                        conn,
                        scan_id,
                        entry,
                        root_path,
                        dir_id,
                        regular_patterns,
                        exception_patterns,
                    )
                elif is_file:
                    # Process file
                    try:
                        stat = entry.stat()

                        # Compute MD5 if requested
                        md5_hash = None
                        if self.compute_hash:
                            md5_hash = compute_md5(entry)

                        # Get extension
                        extension = entry.suffix.lower() if entry.suffix else None

                        file_batch.append(
                            (
                                scan_id,
                                dir_id,
                                entry.name,
                                extension,
                                stat.st_size,
                                datetime.fromtimestamp(stat.st_mtime),
                                md5_hash,
                            )
                        )

                        self.stats["files"] += 1
                        self.stats["bytes"] += stat.st_size

                        # Batch commit
                        if len(file_batch) >= self.batch_size:
                            self._commit_file_batch(cursor, conn, file_batch)
                            file_batch = []

                    except (OSError, PermissionError) as e:
                        show(f"Warning: Cannot process {entry}: {e}")
                        self.stats["errors"] += 1

            # Commit remaining files
            if file_batch:
                self._commit_file_batch(cursor, conn, file_batch)

        finally:
            cursor.close()

    def _commit_file_batch(self, cursor, conn, file_batch: list) -> None:
        """Commit a batch of files to database."""
        cursor.executemany(
            f"INSERT INTO files (scan_id, directory_id, filename, extension, "
            f"size, mtime, md5_hash) VALUES ({self.ph}, {self.ph}, "
            f"{self.ph}, {self.ph}, {self.ph}, {self.ph}, {self.ph})",
            file_batch,
        )
        conn.commit()

    @staticmethod
    def _parse_mtime(mtime_val) -> Optional[datetime]:
        """Parse mtime from DB value (may be str or datetime)."""
        if mtime_val is None:
            return None
        if isinstance(mtime_val, datetime):
            return mtime_val
        if isinstance(mtime_val, str):
            try:
                return datetime.fromisoformat(mtime_val)
            except ValueError:
                return None
        return None

    def rescan(self, scan_id: int) -> dict:
        """Re-scan a previously scanned directory, updating changed files.

        - Fails immediately if the scan path does not exist (e.g. disconnected device).
        - Marks deleted files/directories with deleted_at timestamp.
        - Updates hash and mtime for changed files.
        - Inserts newly appeared files.
        - Restores files/dirs that had deleted_at set but reappeared.

        Args:
            scan_id: ID of an existing scan to re-scan.

        Returns:
            Statistics dictionary.
        """
        conn = self.config.get_connection()
        cursor = conn.cursor()

        try:
            # Fetch scan info
            cursor.execute(
                f"SELECT scan_path FROM scans WHERE id = {self.ph}",
                (scan_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Scan #{scan_id} not found")

            scan_path_str = row[0] if isinstance(row, tuple) else row["scan_path"]
            scan_path = pathlib.Path(scan_path_str)

            # Fail fast – don't mark everything deleted if device is just disconnected
            if not scan_path.exists():
                raise FileNotFoundError(
                    f"Scan path does not exist: {scan_path}\n"
                    "If this is an external device, please connect it first."
                )
            if not scan_path.is_dir():
                raise ValueError(f"Scan path is not a directory: {scan_path}")

            show(f"Re-scanning: {scan_path}")
            start_time = time.time()

            if self.one_filesystem:
                self.root_device = scan_path.stat().st_dev
                show("One-filesystem mode: will not cross filesystem boundaries")

            # Load ignore patterns
            regular_patterns, exception_patterns = load_ignore_patterns(conn)
            show(
                f"Loaded {len(regular_patterns)} ignore patterns "
                f"({len(exception_patterns)} exceptions)"
            )

            # Load existing files: (dir_path, filename) -> info dict
            cursor.execute(
                f"""
                SELECT files.id, directories.path, files.filename,
                       files.size, files.mtime, files.md5_hash,
                       files.deleted_at, COALESCE(files.ignored, 0) AS ignored
                FROM files
                JOIN directories ON files.directory_id = directories.id
                WHERE files.scan_id = {self.ph}
                """,
                (scan_id,),
            )
            existing_files: dict = {}
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    fid, dir_path, filename, size, mtime, md5, deleted_at, ignored = row
                else:
                    fid = row["id"]
                    dir_path = row["path"]
                    filename = row["filename"]
                    size = row["size"]
                    mtime = row["mtime"]
                    md5 = row["md5_hash"]
                    deleted_at = row["deleted_at"]
                    ignored = row["ignored"]
                existing_files[(dir_path, filename)] = {
                    "id": fid,
                    "size": size,
                    "mtime": mtime,
                    "md5": md5,
                    "deleted_at": deleted_at,
                    "ignored": bool(ignored),
                }

            # Load existing directories: path -> info dict
            cursor.execute(
                f"SELECT id, path, parent_id, deleted_at FROM directories WHERE scan_id = {self.ph}",
                (scan_id,),
            )
            existing_dirs: dict = {}
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    did, dpath, parent_id, deleted_at = row
                else:
                    did = row["id"]
                    dpath = row["path"]
                    parent_id = row["parent_id"]
                    deleted_at = row["deleted_at"]
                existing_dirs[dpath] = {
                    "id": did,
                    "parent_id": parent_id,
                    "deleted_at": deleted_at,
                }
                # Pre-populate directory cache so _get_or_create_directory works
                self.directory_cache[dpath] = did

            show(
                f"Loaded {len(existing_files)} existing files, "
                f"{len(existing_dirs)} directories"
            )

            # Reset stats
            self.stats = {
                "files": 0,
                "dirs": 0,
                "bytes": 0,
                "ignored": 0,
                "errors": 0,
                "new": 0,
                "updated": 0,
                "undeleted": 0,
            }

            # Walk directory tree
            seen_files: set = set()
            seen_dirs: set = set()

            self._rescan_directory(
                conn,
                scan_id,
                scan_path,
                scan_path,
                None,
                regular_patterns,
                exception_patterns,
                existing_files,
                existing_dirs,
                seen_files,
                seen_dirs,
            )

            # Mark files not seen as deleted
            now = datetime.now()
            deleted_files = 0
            for key, info in existing_files.items():
                if (
                    key not in seen_files
                    and info["deleted_at"] is None
                    and not info["ignored"]
                ):
                    cursor.execute(
                        f"UPDATE files SET deleted_at = {self.ph} WHERE id = {self.ph}",
                        (now, info["id"]),
                    )
                    deleted_files += 1

            # Mark directories not seen as deleted
            deleted_dirs = 0
            for dpath, info in existing_dirs.items():
                if dpath not in seen_dirs and info["deleted_at"] is None:
                    cursor.execute(
                        f"UPDATE directories SET deleted_at = {self.ph} WHERE id = {self.ph}",
                        (now, info["id"]),
                    )
                    deleted_dirs += 1

            conn.commit()

            # Update scan duration
            duration = time.time() - start_time
            cursor.execute(
                f"UPDATE scans SET duration_seconds = {self.ph} WHERE id = {self.ph}",
                (duration, scan_id),
            )
            conn.commit()

            self.stats["deleted_files"] = deleted_files
            self.stats["deleted_dirs"] = deleted_dirs
            self.stats["duration"] = duration

            show("\nRe-scan complete!")
            show(
                f"  Files: {self.stats['files']:,} seen "
                f"({self.stats['new']} new, {self.stats['updated']} updated, "
                f"{self.stats['undeleted']} restored)"
            )
            show(f"  Deleted: {deleted_files} files, {deleted_dirs} dirs")
            show(f"  Ignored: {self.stats['ignored']:,}")
            show(f"  Errors: {self.stats['errors']:,}")
            show(f"  Duration: {duration:.1f} seconds")

            return self.stats

        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def _rescan_directory(
        self,
        conn,
        scan_id: int,
        dir_path: pathlib.Path,
        root_path: pathlib.Path,
        parent_id: Optional[int],
        regular_patterns: list[str],
        exception_patterns: list[str],
        existing_files: dict,
        existing_dirs: dict,
        seen_files: set,
        seen_dirs: set,
    ) -> None:
        """Recursively re-scan a directory, updating the database in place."""
        cursor = conn.cursor()

        try:
            dir_path_str = str(dir_path)
            seen_dirs.add(dir_path_str)

            # Get or create directory record
            if dir_path_str in existing_dirs:
                dir_id = existing_dirs[dir_path_str]["id"]
                # Restore directory if it was previously marked deleted
                if existing_dirs[dir_path_str]["deleted_at"] is not None:
                    cursor.execute(
                        f"UPDATE directories SET deleted_at = NULL WHERE id = {self.ph}",
                        (dir_id,),
                    )
                    conn.commit()
            else:
                dir_id = self._get_or_create_directory(
                    cursor, conn, scan_id, dir_path, root_path, parent_id
                )
                existing_dirs[dir_path_str] = {
                    "id": dir_id,
                    "parent_id": parent_id,
                    "deleted_at": None,
                }

            # List directory contents
            try:
                entries = list(dir_path.iterdir())
            except (OSError, PermissionError) as e:
                show(f"Warning: Cannot read directory {dir_path}: {e}")
                self.stats["errors"] += 1
                return

            file_batch_insert = []

            for entry in tqdm(entries, desc=str(dir_path.name), leave=False):
                try:
                    rel_path = entry.relative_to(root_path)
                except ValueError:
                    rel_path = entry

                if should_ignore(str(rel_path), regular_patterns, exception_patterns):
                    self.stats["ignored"] += 1
                    continue

                try:
                    is_symlink = entry.is_symlink()
                    is_dir = entry.is_dir()
                    is_file = entry.is_file()
                except OSError as e:
                    show(f"Warning: Cannot access {entry}: {e}")
                    self.stats["errors"] += 1
                    continue

                if is_symlink:
                    continue

                if is_dir:
                    if self.one_filesystem and self.root_device is not None:
                        try:
                            if entry.stat().st_dev != self.root_device:
                                show(f"Skipping {entry}: different filesystem")
                                self.stats["ignored"] += 1
                                continue
                        except (OSError, PermissionError):
                            pass

                    self._rescan_directory(
                        conn,
                        scan_id,
                        entry,
                        root_path,
                        dir_id,
                        regular_patterns,
                        exception_patterns,
                        existing_files,
                        existing_dirs,
                        seen_files,
                        seen_dirs,
                    )

                elif is_file:
                    try:
                        stat = entry.stat()
                        key = (dir_path_str, entry.name)
                        seen_files.add(key)

                        if key in existing_files:
                            info = existing_files[key]
                            new_mtime = datetime.fromtimestamp(stat.st_mtime)
                            existing_mtime_dt = self._parse_mtime(info["mtime"])

                            size_changed = stat.st_size != info["size"]
                            if existing_mtime_dt is None:
                                mtime_changed = True
                            else:
                                mtime_changed = (
                                    abs((new_mtime - existing_mtime_dt).total_seconds())
                                    > 1
                                )

                            was_deleted = info["deleted_at"] is not None
                            content_changed = size_changed or mtime_changed

                            if was_deleted or content_changed:
                                new_md5 = info["md5"]
                                if content_changed and self.compute_hash:
                                    new_md5 = compute_md5(entry)

                                cursor.execute(
                                    f"UPDATE files SET size = {self.ph}, mtime = {self.ph}, "
                                    f"md5_hash = {self.ph}, deleted_at = NULL "
                                    f"WHERE id = {self.ph}",
                                    (stat.st_size, new_mtime, new_md5, info["id"]),
                                )

                                if was_deleted:
                                    self.stats["undeleted"] += 1
                                if content_changed:
                                    self.stats["updated"] += 1

                            self.stats["files"] += 1
                            self.stats["bytes"] += stat.st_size

                        else:
                            # New file not in DB
                            md5_hash = compute_md5(entry) if self.compute_hash else None
                            extension = entry.suffix.lower() if entry.suffix else None
                            new_mtime = datetime.fromtimestamp(stat.st_mtime)

                            file_batch_insert.append(
                                (
                                    scan_id,
                                    dir_id,
                                    entry.name,
                                    extension,
                                    stat.st_size,
                                    new_mtime,
                                    md5_hash,
                                )
                            )
                            self.stats["files"] += 1
                            self.stats["bytes"] += stat.st_size
                            self.stats["new"] += 1

                            if len(file_batch_insert) >= self.batch_size:
                                self._commit_file_batch(cursor, conn, file_batch_insert)
                                file_batch_insert = []

                    except (OSError, PermissionError) as e:
                        show(f"Warning: Cannot process {entry}: {e}")
                        self.stats["errors"] += 1

            if file_batch_insert:
                self._commit_file_batch(cursor, conn, file_batch_insert)
            conn.commit()

        finally:
            cursor.close()
