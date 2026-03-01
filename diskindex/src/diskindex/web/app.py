"""Flask web application for diskindex."""

from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime
import os

from diskindex.config import load_config
from diskindex.database import DatabaseConfig


def get_page_args():
    """Get pagination parameters from request."""
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    try:
        per_page = int(request.args.get("per_page", 50))
    except ValueError:
        per_page = 50

    # Clamp values
    page = max(1, page)
    per_page = min(max(10, per_page), 500)  # Between 10 and 500

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_cached_count(cache_key: str):
    """Get cached count from session or return None."""
    if "counts" not in session:
        session["counts"] = {}
    return session["counts"].get(cache_key)


def set_cached_count(cache_key: str, count: int):
    """Cache count in session."""
    if "counts" not in session:
        session["counts"] = {}
    session["counts"][cache_key] = count


def get_pagination_info(total_count: int, page: int, per_page: int):
    """Calculate pagination information."""
    total_pages = (total_count + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages

    return {
        "total_count": total_count,
        "total_pages": total_pages,
        "page": page,
        "per_page": per_page,
        "has_prev": has_prev,
        "has_next": has_next,
        "prev_page": page - 1 if has_prev else None,
        "next_page": page + 1 if has_next else None,
    }


def create_app(config: DatabaseConfig | None = None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Store config in app context
    if config is None:
        config = load_config()
    app.config["DB_CONFIG"] = config

    @app.route("/")
    def index():
        """Home page with dashboard."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get scan statistics
            cursor.execute("SELECT COUNT(*) FROM scans")
            scan_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM files WHERE deleted_at IS NULL AND NOT COALESCE(ignored, false)"
            )
            file_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT SUM(size) FROM files WHERE deleted_at IS NULL AND NOT COALESCE(ignored, false)"
            )
            total_size = cursor.fetchone()[0] or 0

            # Get recent scans
            cursor.execute(
                "SELECT id, scan_date, scan_path, duration_seconds, notes "
                "FROM scans ORDER BY scan_date DESC LIMIT 5"
            )
            recent_scans = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    scan_id, scan_date, scan_path, duration, notes = row
                else:
                    scan_id = row["id"]
                    scan_date = row["scan_date"]
                    scan_path = row["scan_path"]
                    duration = row["duration_seconds"]
                    notes = row["notes"]

                # Get file count for this scan
                cursor.execute(
                    f"SELECT COUNT(*) FROM files WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, false)"
                )
                files_in_scan = cursor.fetchone()[0]

                recent_scans.append(
                    {
                        "id": scan_id,
                        "date": scan_date,
                        "path": scan_path,
                        "duration": duration,
                        "notes": notes,
                        "file_count": files_in_scan,
                    }
                )

            return render_template(
                "index.html",
                scan_count=scan_count,
                file_count=file_count,
                total_size=total_size,
                recent_scans=recent_scans,
            )
        finally:
            cursor.close()
            conn.close()

    @app.route("/scans")
    def scans():
        """List all scans."""
        page, per_page, offset = get_page_args()

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get total count (cached in session)
            cache_key = "scans_count"
            total_count = get_cached_count(cache_key)

            if total_count is None:
                cursor.execute("SELECT COUNT(*) FROM scans")
                total_count = cursor.fetchone()[0]
                set_cached_count(cache_key, total_count)

            # Get paginated scans
            cursor.execute(
                f"SELECT id, scan_date, scan_path, duration_seconds, notes "
                f"FROM scans ORDER BY scan_date DESC LIMIT {per_page} OFFSET {offset}"
            )

            scan_list = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    scan_id, scan_date, scan_path, duration, notes = row
                else:
                    scan_id = row["id"]
                    scan_date = row["scan_date"]
                    scan_path = row["scan_path"]
                    duration = row["duration_seconds"]
                    notes = row["notes"]

                # Get root directory ID
                cursor.execute(
                    f"SELECT id FROM directories "
                    f"WHERE scan_id = {scan_id} AND parent_id IS NULL LIMIT 1"
                )
                root_dir_row = cursor.fetchone()
                root_dir_id = root_dir_row[0] if root_dir_row else None

                # Get file count and total size
                cursor.execute(
                    f"SELECT COUNT(*), SUM(size) FROM files "
                    f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, false)"
                )
                count_row = cursor.fetchone()
                file_count = count_row[0]
                total_size = count_row[1] or 0

                scan_list.append(
                    {
                        "id": scan_id,
                        "date": scan_date,
                        "path": scan_path,
                        "duration": duration,
                        "notes": notes,
                        "file_count": file_count,
                        "total_size": total_size,
                        "root_directory_id": root_dir_id,
                    }
                )

            pagination = get_pagination_info(total_count, page, per_page)
            return render_template("scans.html", scans=scan_list, pagination=pagination)
        finally:
            cursor.close()
            conn.close()

    @app.route("/scan/<int:scan_id>")
    def scan_detail(scan_id):
        """View details of a specific scan."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get scan info
            cursor.execute(
                f"SELECT id, scan_date, scan_path, duration_seconds, notes "
                f"FROM scans WHERE id = {scan_id}"
            )
            row = cursor.fetchone()

            if not row:
                return "Scan not found", 404

            if isinstance(row, tuple):
                scan_data = {
                    "id": row[0],
                    "date": row[1],
                    "path": row[2],
                    "duration": row[3],
                    "notes": row[4],
                }
            else:
                scan_data = {
                    "id": row["id"],
                    "date": row["scan_date"],
                    "path": row["scan_path"],
                    "duration": row["duration_seconds"],
                    "notes": row["notes"],
                }

            # Get root directory ID for this scan
            cursor.execute(
                f"SELECT id FROM directories "
                f"WHERE scan_id = {scan_id} AND parent_id IS NULL LIMIT 1"
            )
            root_dir_row = cursor.fetchone()
            scan_data["root_directory_id"] = root_dir_row[0] if root_dir_row else None

            # Get file statistics
            cursor.execute(
                f"SELECT COUNT(*), SUM(size) FROM files "
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, false)"
            )
            count_row = cursor.fetchone()
            scan_data["file_count"] = count_row[0]
            scan_data["total_size"] = count_row[1] or 0

            # Get file type breakdown
            cursor.execute(
                f"SELECT extension, COUNT(*), SUM(size) FROM files "
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, false) "
                f"GROUP BY extension ORDER BY COUNT(*) DESC LIMIT 10"
            )
            extensions = []
            for ext_row in cursor.fetchall():
                extensions.append(
                    {
                        "ext": ext_row[0] or "(no extension)",
                        "count": ext_row[1],
                        "size": ext_row[2] or 0,
                    }
                )

            # Get volume information
            cursor.execute(
                f"SELECT label, filesystem_type, total_size, free_space, "
                f"mount_options, uuid, drive_type "
                f"FROM volumes WHERE scan_id = {scan_id}"
            )
            volumes = []
            for vol_row in cursor.fetchall():
                if isinstance(vol_row, tuple):
                    volumes.append(
                        {
                            "label": vol_row[0] or "(no label)",
                            "filesystem": vol_row[1],
                            "total_size": vol_row[2],
                            "free_space": vol_row[3],
                            "mount_options": vol_row[4],
                            "uuid": vol_row[5],
                            "drive_type": vol_row[6],
                        }
                    )
                else:
                    volumes.append(
                        {
                            "label": vol_row["label"] or "(no label)",
                            "filesystem": vol_row["filesystem_type"],
                            "total_size": vol_row["total_size"],
                            "free_space": vol_row["free_space"],
                            "mount_options": vol_row["mount_options"],
                            "uuid": vol_row["uuid"],
                            "drive_type": vol_row["drive_type"],
                        }
                    )

            return render_template(
                "scan_detail.html",
                scan=scan_data,
                extensions=extensions,
                volumes=volumes,
            )
        finally:
            cursor.close()
            conn.close()

    @app.route("/scan/<int:scan_id>/delete", methods=["POST"])
    def delete_scan(scan_id):
        """Delete a scan and all associated data."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Verify scan exists first
            cursor.execute(f"SELECT scan_path FROM scans WHERE id = {scan_id}")
            row = cursor.fetchone()

            if not row:
                flash(f"Scan #{scan_id} not found", "error")
                return redirect(url_for("scans"))

            # Manually delete related rows instead of relying on DB CASCADE
            cursor.execute(f"DELETE FROM files WHERE scan_id = {scan_id}")
            cursor.execute(f"DELETE FROM directories WHERE scan_id = {scan_id}")
            cursor.execute(f"DELETE FROM volumes WHERE scan_id = {scan_id}")
            cursor.execute(f"DELETE FROM scans WHERE id = {scan_id}")
            conn.commit()

            # Clear cached counts since data changed
            if "counts" in session:
                session.pop("counts")

            flash(f"Scan #{scan_id} deleted successfully", "success")
            return redirect(url_for("scans"))

        except Exception as e:
            conn.rollback()
            flash(f"Error deleting scan: {e}", "error")
            return redirect(url_for("scans"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/search")
    def search():
        """Search for files."""
        query = request.args.get("q", "")
        extension = request.args.get("ext", "")
        min_size = request.args.get("min_size", type=int)
        max_size = request.args.get("max_size", type=int)
        unique_only = request.args.get("unique_only") == "1"
        scan_id = request.args.get("scan_id", type=int)
        page, per_page, offset = get_page_args()

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get all scans for dropdown
            cursor.execute(
                """
                SELECT scans.id, scans.scan_path, scans.scan_date,
                       COUNT(files.id) as file_count
                FROM scans
                LEFT JOIN files ON scans.id = files.scan_id
                    AND files.deleted_at IS NULL
                    AND NOT COALESCE(files.ignored, false)
                GROUP BY scans.id, scans.scan_path, scans.scan_date
                ORDER BY scans.scan_date DESC
            """
            )

            scans_list = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    sid, spath, sdate, fcount = row
                else:
                    sid = row["id"]
                    spath = row["scan_path"]
                    sdate = row["scan_date"]
                    fcount = row["file_count"]

                scans_list.append(
                    {"id": sid, "path": spath, "date": sdate, "file_count": fcount}
                )

            # Build search query
            conditions = [
                "files.deleted_at IS NULL",
                "NOT COALESCE(files.ignored, false)",
            ]
            params = []

            if query:
                conditions.append("files.filename LIKE ?")
                params.append(f"%{query}%")

            if extension:
                conditions.append("files.extension = ?")
                params.append(
                    extension if extension.startswith(".") else f".{extension}"
                )

            if min_size is not None:
                conditions.append("files.size >= ?")
                params.append(min_size)

            if max_size is not None:
                conditions.append("files.size <= ?")
                params.append(max_size)

            if scan_id:
                conditions.append("files.scan_id = ?")
                params.append(scan_id)

            # Add unique files filter (exclude files with duplicate hashes)
            if unique_only:
                # If a specific scan is selected, only filter duplicates within that scan
                # Otherwise, filter duplicates across all scans
                if scan_id:
                    conditions.append(
                        """
                        files.md5_hash NOT IN (
                            SELECT md5_hash FROM files
                            WHERE scan_id = ?
                              AND deleted_at IS NULL
                              AND NOT COALESCE(ignored, false)
                              AND md5_hash IS NOT NULL
                              AND md5_hash != ''
                            GROUP BY md5_hash
                            HAVING COUNT(*) > 1
                        )
                    """
                    )
                    params.append(scan_id)
                else:
                    conditions.append(
                        """
                        files.md5_hash NOT IN (
                            SELECT md5_hash FROM files
                            WHERE deleted_at IS NULL
                              AND NOT COALESCE(ignored, false)
                              AND md5_hash IS NOT NULL
                              AND md5_hash != ''
                            GROUP BY md5_hash
                            HAVING COUNT(*) > 1
                        )
                    """
                    )

            where_clause = " AND ".join(conditions)

            # Get total count (cached with search params)
            cache_key = f"search_count_{hash((query, extension, min_size, max_size, unique_only, scan_id))}"
            total_count = get_cached_count(cache_key)

            if total_count is None:
                count_sql = f"""
                    SELECT COUNT(*)
                    FROM files
                    WHERE {where_clause}
                """
                cursor.execute(count_sql, params)
                total_count = cursor.fetchone()[0]
                set_cached_count(cache_key, total_count)

            # Get paginated results
            sql = f"""
                SELECT files.id, files.filename, files.extension, files.size,
                       files.mtime, files.md5_hash, files.directory_id,
                       directories.path, scans.scan_path
                FROM files
                JOIN directories ON files.directory_id = directories.id
                JOIN scans ON files.scan_id = scans.id
                WHERE {where_clause}
                ORDER BY files.size DESC
                LIMIT {per_page} OFFSET {offset}
            """

            cursor.execute(sql, params)

            results = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    (
                        file_id,
                        filename,
                        ext,
                        size,
                        mtime,
                        md5,
                        dir_id,
                        dir_path,
                        scan_path,
                    ) = row
                else:
                    file_id = row["id"]
                    filename = row["filename"]
                    ext = row["extension"]
                    size = row["size"]
                    mtime = row["mtime"]
                    md5 = row["md5_hash"]
                    dir_id = row["directory_id"]
                    dir_path = row["path"]
                    scan_path = row["scan_path"]

                full_path = os.path.join(dir_path, filename)

                results.append(
                    {
                        "id": file_id,
                        "directory_id": dir_id,
                        "filename": filename,
                        "extension": ext,
                        "size": size,
                        "mtime": mtime,
                        "md5": md5,
                        "path": full_path,
                        "scan_path": scan_path,
                    }
                )

            pagination = get_pagination_info(total_count, page, per_page)
            return render_template(
                "search.html",
                query=query,
                extension=extension,
                min_size=min_size,
                max_size=max_size,
                unique_only=unique_only,
                scan_id=scan_id,
                scans=scans_list,
                results=results,
                pagination=pagination,
            )
        finally:
            cursor.close()
            conn.close()

    @app.route("/duplicates")
    def duplicates():
        """Find and display duplicate files."""
        min_size = (
            request.args.get("min_size", 1, type=int) * 1024
        )  # Default 1KB minimum
        scan_id = request.args.get("scan_id", type=int)
        mode = request.args.get(
            "mode", "across_scans"
        )  # "within_scan" or "across_scans"
        page, per_page, offset = get_page_args()

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get list of scans for filter dropdown
            cursor.execute(
                "SELECT id, scan_path, scan_date FROM scans ORDER BY scan_date DESC"
            )
            scans = cursor.fetchall()

            # Build WHERE clauses based on filters
            where_clauses = [
                "deleted_at IS NULL",
                "NOT COALESCE(ignored, false)",
                "md5_hash IS NOT NULL",
                "md5_hash != ''",
            ]

            hash_col = "md5_hash" if config.backend == "sqlite" else "md5_hash"
            placeholder = "?" if config.backend == "sqlite" else "%s"

            # Get total count of duplicate groups
            cache_key = f"duplicates_count_{min_size}_{scan_id}_{mode}"
            total_count = get_cached_count(cache_key)

            if total_count is None:
                if scan_id and mode == "across_scans":
                    # Count files in selected scan that have duplicates in other scans (different paths)
                    count_sql = f"""
                        SELECT COUNT(DISTINCT f1.{hash_col}) FROM files f1
                        WHERE f1.scan_id = {placeholder} AND f1.size >= {placeholder}
                          AND f1.deleted_at IS NULL
                          AND NOT COALESCE(f1.ignored, false)
                          AND f1.{hash_col} IS NOT NULL
                          AND f1.{hash_col} != ''
                          AND EXISTS (
                              SELECT 1 FROM files f2
                              WHERE f2.{hash_col} = f1.{hash_col}
                                AND f2.size = f1.size
                                AND f2.scan_id != {placeholder}
                                AND f2.deleted_at IS NULL
                                AND NOT COALESCE(f2.ignored, false)
                          )
                    """
                    cursor.execute(count_sql, (scan_id, min_size, scan_id))
                elif scan_id and mode == "within_scan":
                    # Count duplicate groups within selected scan (different paths in same scan)
                    count_sql = f"""
                        SELECT COUNT(*) FROM (
                            SELECT {hash_col}, size
                            FROM files
                            WHERE scan_id = {placeholder} AND size >= {placeholder}
                              AND deleted_at IS NULL
                              AND NOT COALESCE(ignored, false)
                              AND {hash_col} IS NOT NULL
                              AND {hash_col} != ''
                            GROUP BY {hash_col}, size
                            HAVING COUNT(DISTINCT directory_id || '/' || filename) > 1
                        )
                    """
                    cursor.execute(count_sql, (scan_id, min_size))
                else:
                    # All duplicates across all scans (different paths only)
                    count_sql = f"""
                        SELECT COUNT(*) FROM (
                            SELECT {hash_col}, size
                            FROM files
                            WHERE size >= {placeholder}
                              AND deleted_at IS NULL
                              AND NOT COALESCE(ignored, false)
                              AND {hash_col} IS NOT NULL
                              AND {hash_col} != ''
                            GROUP BY {hash_col}, size
                            HAVING COUNT(DISTINCT directory_id || '/' || filename) > 1
                        )
                    """
                    cursor.execute(count_sql, (min_size,))
                total_count = cursor.fetchone()[0]
                set_cached_count(cache_key, total_count)

            # Find duplicate files with pagination
            if scan_id and mode == "across_scans":
                # Files from selected scan with duplicates in other scans
                sql = f"""
                    SELECT f1.{hash_col}, f1.size, COUNT(DISTINCT f2.id) + 1 as dup_count
                    FROM files f1
                    JOIN files f2 ON f2.{hash_col} = f1.{hash_col}
                        AND f2.size = f1.size
                        AND f2.scan_id != f1.scan_id
                        AND f2.deleted_at IS NULL
                        AND NOT COALESCE(f2.ignored, false)
                    WHERE f1.scan_id = {placeholder} AND f1.size >= {placeholder}
                      AND f1.deleted_at IS NULL
                      AND NOT COALESCE(f1.ignored, false)
                      AND f1.{hash_col} IS NOT NULL
                      AND f1.{hash_col} != ''
                    GROUP BY f1.{hash_col}, f1.size
                    ORDER BY f1.size DESC, dup_count DESC
                    LIMIT {per_page} OFFSET {offset}
                """
                cursor.execute(sql, (scan_id, min_size))
            elif scan_id and mode == "within_scan":
                # Duplicates within selected scan only
                sql = f"""
                    SELECT {hash_col}, size, COUNT(*) as dup_count
                    FROM files
                    WHERE scan_id = {placeholder} AND size >= {placeholder}
                      AND deleted_at IS NULL
                      AND NOT COALESCE(ignored, false)
                      AND {hash_col} IS NOT NULL
                      AND {hash_col} != ''
                    GROUP BY {hash_col}, size
                    HAVING COUNT(DISTINCT directory_id || '/' || filename) > 1
                    ORDER BY size DESC, dup_count DESC
                    LIMIT {per_page} OFFSET {offset}
                """
                cursor.execute(sql, (scan_id, min_size))
            else:
                # All duplicates (different paths only)
                sql = f"""
                    SELECT {hash_col}, size, COUNT(*) as dup_count
                    FROM files
                    WHERE size >= {placeholder}
                      AND deleted_at IS NULL
                      AND NOT COALESCE(ignored, false)
                      AND {hash_col} IS NOT NULL
                      AND {hash_col} != ''
                    GROUP BY {hash_col}, size
                    HAVING COUNT(DISTINCT directory_id || '/' || filename) > 1
                    ORDER BY size DESC, dup_count DESC
                    LIMIT {per_page} OFFSET {offset}
                """
                cursor.execute(sql, (min_size,))

            duplicate_groups = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    md5, size, count = row
                else:
                    md5 = row[hash_col]
                    size = row["size"]
                    count = row["dup_count"]

                # Get all files in this duplicate group (across all scans for context)
                cursor.execute(
                    f"""
                    SELECT files.id, files.filename, files.scan_id, files.directory_id,
                           directories.path, scans.scan_path, scans.scan_date
                    FROM files
                    JOIN directories ON files.directory_id = directories.id
                    JOIN scans ON files.scan_id = scans.id
                    WHERE files.{hash_col} = {placeholder}
                      AND files.deleted_at IS NULL
                      AND NOT COALESCE(files.ignored, false)
                    ORDER BY scans.scan_date DESC, directories.path, files.filename
                    """,
                    (md5,),
                )

                files = []
                seen_paths = set()  # Track unique file paths
                for file_row in cursor.fetchall():
                    if isinstance(file_row, tuple):
                        (
                            file_id,
                            filename,
                            file_scan_id,
                            dir_id,
                            dir_path,
                            scan_path,
                            scan_date,
                        ) = file_row
                    else:
                        file_id = file_row["id"]
                        filename = file_row["filename"]
                        file_scan_id = file_row["scan_id"]
                        dir_id = file_row["directory_id"]
                        dir_path = file_row["path"]
                        scan_path = file_row["scan_path"]
                        scan_date = file_row["scan_date"]

                    full_path = os.path.join(dir_path, filename)
                    path_key = f"{dir_path}/{filename}"

                    # Mark if this is from the selected scan
                    is_selected_scan = scan_id and file_scan_id == scan_id
                    is_duplicate_path = path_key in seen_paths

                    files.append(
                        {
                            "id": file_id,
                            "filename": filename,
                            "path": full_path,
                            "directory_id": dir_id,
                            "scan_id": file_scan_id,
                            "scan_path": scan_path,
                            "scan_date": scan_date,
                            "is_selected_scan": is_selected_scan,
                            "is_duplicate_path": is_duplicate_path,
                        }
                    )
                    seen_paths.add(path_key)

                # Calculate actual duplicates (different paths only)
                unique_paths_count = len(seen_paths)
                wasted_space = (
                    size * (unique_paths_count - 1) if unique_paths_count > 1 else 0
                )

                duplicate_groups.append(
                    {
                        "md5": md5,
                        "size": size,
                        "count": count,
                        "unique_paths_count": unique_paths_count,
                        "wasted_space": wasted_space,
                        "files": files,
                    }
                )

            # Calculate total wasted space (only counting different paths)
            if total_count > 0:
                if scan_id and mode == "across_scans":
                    # Wasted space for files in selected scan that have external duplicates
                    cursor.execute(
                        f"""
                        SELECT SUM(f1.size) FROM files f1
                        WHERE f1.scan_id = {placeholder} AND f1.size >= {placeholder}
                          AND f1.deleted_at IS NULL
                          AND NOT COALESCE(f1.ignored, false)
                          AND f1.{hash_col} IS NOT NULL
                          AND f1.{hash_col} != ''
                          AND EXISTS (
                              SELECT 1 FROM files f2
                              WHERE f2.{hash_col} = f1.{hash_col}
                                AND f2.size = f1.size
                                AND f2.scan_id != {placeholder}
                                AND f2.deleted_at IS NULL
                                AND NOT COALESCE(f2.ignored, false)
                          )
                        """,
                        (scan_id, min_size, scan_id),
                    )
                else:
                    # Total wasted space from unique path duplicates
                    cursor.execute(
                        f"""
                        SELECT SUM(size * (path_count - 1)) FROM (
                            SELECT size, COUNT(DISTINCT directory_id || '/' || filename) as path_count
                            FROM files
                            WHERE size >= {placeholder}
                              AND deleted_at IS NULL
                              AND NOT COALESCE(ignored, false)
                              AND {hash_col} IS NOT NULL
                              AND {hash_col} != ''
                            GROUP BY {hash_col}, size
                            HAVING COUNT(DISTINCT directory_id || '/' || filename) > 1
                        )
                        """,
                        (min_size,),
                    )
                total_wasted = cursor.fetchone()[0] or 0
            else:
                total_wasted = 0

            pagination = get_pagination_info(total_count, page, per_page)
            return render_template(
                "duplicates.html",
                duplicate_groups=duplicate_groups,
                total_wasted=total_wasted,
                min_size=min_size,
                scans=scans,
                selected_scan_id=scan_id,
                mode=mode,
                pagination=pagination,
            )
        finally:
            cursor.close()
            conn.close()

    @app.template_filter("filesizeformat")
    def filesizeformat(bytes_value):
        """Format bytes as human-readable size."""
        if bytes_value is None:
            return "0 B"

        # for decimals:
        bytes_value = float(bytes_value)

        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    @app.template_filter("datetimeformat")
    def datetimeformat(value):
        """Format datetime for display."""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except:
                return value

        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return ""

    @app.route("/patterns")
    def patterns():
        """List and manage ignore patterns."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, pattern, is_exception, applies_to, notes "
                "FROM ignore_patterns ORDER BY is_exception DESC, pattern"
            )

            pattern_list = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    pattern_id, pattern, is_exception, applies_to, notes = row
                else:
                    pattern_id = row["id"]
                    pattern = row["pattern"]
                    is_exception = row["is_exception"]
                    applies_to = row["applies_to"]
                    notes = row["notes"]

                pattern_list.append(
                    {
                        "id": pattern_id,
                        "pattern": pattern,
                        "is_exception": is_exception,
                        "applies_to": applies_to,
                        "notes": notes,
                    }
                )

            return render_template("patterns.html", patterns=pattern_list)
        finally:
            cursor.close()
            conn.close()

    @app.route("/patterns/add", methods=["POST"])
    def patterns_add():
        """Add a new ignore pattern."""
        pattern = request.form.get("pattern", "").strip()
        is_exception = request.form.get("is_exception") == "on"
        applies_to = request.form.get("applies_to", "all")
        notes = request.form.get("notes", "").strip()

        if not pattern:
            return "Pattern is required", 400

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            placeholder = "?" if config.backend == "sqlite" else "%s"
            cursor.execute(
                f"INSERT INTO ignore_patterns (pattern, is_exception, applies_to, notes) "
                f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
                (pattern, is_exception, applies_to, notes),
            )
            conn.commit()

            # Clear cached counts (pattern changes may affect search results)
            session.pop("counts", None)

            from flask import redirect, url_for

            return redirect(url_for("patterns"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/patterns/<int:pattern_id>/delete", methods=["POST"])
    def patterns_delete(pattern_id):
        """Delete an ignore pattern."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            placeholder = "?" if config.backend == "sqlite" else "%s"
            cursor.execute(
                f"DELETE FROM ignore_patterns WHERE id = {placeholder}",
                (pattern_id,),
            )
            conn.commit()

            # Clear cached counts
            session.pop("counts", None)

            from flask import redirect, url_for

            return redirect(url_for("patterns"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/patterns/apply", methods=["POST"])
    def patterns_apply():
        """Re-apply ignore patterns to all files."""
        from diskindex.patterns import reapply_patterns

        # Run re-apply in background (this could take a while)
        stats = reapply_patterns(config, verbose=False)

        # Clear cached counts since file visibility changed
        session.pop("counts", None)

        from flask import redirect, url_for

        # Note: Flask flash requires session support which is already configured
        return redirect(url_for("patterns"))

    @app.route("/file/<int:file_id>/delete/soft", methods=["POST"])
    def delete_file_soft(file_id):
        """Soft delete a file (mark deleted_at timestamp)."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Check if file exists and get info
            cursor.execute(
                f"SELECT filename, deleted_at FROM files WHERE id = {file_id}"
            )
            row = cursor.fetchone()

            if not row:
                flash(f"File #{file_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            filename = row[0] if isinstance(row, tuple) else row["filename"]
            deleted_at = row[1] if isinstance(row, tuple) else row["deleted_at"]

            if deleted_at:
                flash(f"File {filename} is already marked as deleted", "warning")
            else:
                # Mark as deleted
                placeholder = "?" if config.backend == "sqlite" else "%s"
                cursor.execute(
                    f"UPDATE files SET deleted_at = {placeholder} WHERE id = {placeholder}",
                    (datetime.now(), file_id),
                )
                conn.commit()
                flash(f"File {filename} marked as deleted", "success")

                # Clear cached counts
                session.pop("counts", None)

            return redirect(request.referrer or url_for("index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error deleting file: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/file/<int:file_id>/delete/hard", methods=["POST"])
    def delete_file_hard(file_id):
        """Hard delete a file (remove from filesystem and mark deleted_at)."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get file info including full path
            cursor.execute(
                f"""
                SELECT files.filename, files.deleted_at, directories.path, scans.scan_path
                FROM files
                JOIN directories ON files.directory_id = directories.id
                JOIN scans ON files.scan_id = scans.id
                WHERE files.id = {file_id}
                """
            )
            row = cursor.fetchone()

            if not row:
                flash(f"File #{file_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            if isinstance(row, tuple):
                filename, deleted_at, dir_path, scan_path = row
            else:
                filename = row["filename"]
                deleted_at = row["deleted_at"]
                dir_path = row["path"]
                scan_path = row["scan_path"]

            full_path = os.path.join(dir_path, filename)

            # Check if file exists on disk
            if not os.path.exists(full_path):
                flash(
                    f"File {filename} not found on disk at {full_path}. "
                    f"Use soft delete if this is from removable/unmounted media.",
                    "error",
                )
                return redirect(request.referrer or url_for("index"))

            # Delete file from disk
            try:
                os.remove(full_path)

                # Mark as deleted in database
                placeholder = "?" if config.backend == "sqlite" else "%s"
                cursor.execute(
                    f"UPDATE files SET deleted_at = {placeholder} WHERE id = {placeholder}",
                    (datetime.now(), file_id),
                )
                conn.commit()

                flash(
                    f"File {filename} deleted from disk and marked as deleted",
                    "success",
                )

                # Clear cached counts
                session.pop("counts", None)

            except OSError as e:
                flash(f"Error deleting file from disk: {e}", "error")
                return redirect(request.referrer or url_for("index"))

            return redirect(request.referrer or url_for("index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>/delete/soft", methods=["POST"])
    def delete_directory_soft(dir_id):
        """Soft delete a directory and all its files."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory info
            cursor.execute(f"SELECT path FROM directories WHERE id = {dir_id}")
            row = cursor.fetchone()

            if not row:
                flash(f"Directory #{dir_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            dir_path = row[0] if isinstance(row, tuple) else row["path"]

            # Count files to be marked
            cursor.execute(
                f"SELECT COUNT(*) FROM files WHERE directory_id = {dir_id} AND deleted_at IS NULL"
            )
            count = cursor.fetchone()[0]

            if count == 0:
                flash(f"No active files in directory {dir_path}", "warning")
            else:
                # Mark all files in directory as deleted
                placeholder = "?" if config.backend == "sqlite" else "%s"
                cursor.execute(
                    f"UPDATE files SET deleted_at = {placeholder} "
                    f"WHERE directory_id = {placeholder} AND deleted_at IS NULL",
                    (datetime.now(), dir_id),
                )
                conn.commit()
                flash(
                    f"Marked {count} file(s) in directory {dir_path} as deleted",
                    "success",
                )

                # Mark directory as deleted
                cursor.execute(
                    f"UPDATE directories SET deleted_at = {placeholder} WHERE id = {placeholder}",
                    (datetime.now(), dir_id),
                )
                conn.commit()

                # Clear cached counts
                session.pop("counts", None)

            return redirect(request.referrer or url_for("index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error deleting directory: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>/delete/hard", methods=["POST"])
    def delete_directory_hard(dir_id):
        """Hard delete a directory and all its files from filesystem."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory info and files
            cursor.execute(f"SELECT path FROM directories WHERE id = {dir_id}")
            row = cursor.fetchone()

            if not row:
                flash(f"Directory #{dir_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            dir_path = row[0] if isinstance(row, tuple) else row["path"]

            # Get all files in directory
            cursor.execute(
                f"SELECT id, filename FROM files WHERE directory_id = {dir_id} AND deleted_at IS NULL"
            )
            files = cursor.fetchall()

            if not files:
                flash(f"No active files in directory {dir_path}", "warning")
                return redirect(request.referrer or url_for("index"))

            # Check if directory exists
            if not os.path.exists(dir_path):
                flash(
                    f"Directory {dir_path} not found on disk. "
                    f"Use soft delete if this is from removable/unmounted media.",
                    "error",
                )
                return redirect(request.referrer or url_for("index"))

            # Delete each file
            deleted_count = 0
            error_count = 0
            for file_row in files:
                file_id = file_row[0] if isinstance(file_row, tuple) else file_row["id"]
                filename = (
                    file_row[1] if isinstance(file_row, tuple) else file_row["filename"]
                )
                full_path = os.path.join(dir_path, filename)

                try:
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        deleted_count += 1
                except OSError:
                    # Could not delete this file - increment error count
                    error_count += 1

            # Mark all files as deleted in database
            placeholder = "?" if config.backend == "sqlite" else "%s"
            cursor.execute(
                f"UPDATE files SET deleted_at = {placeholder} "
                f"WHERE directory_id = {placeholder}",
                (datetime.now(), dir_id),
            )
            conn.commit()

            # Try to remove directory if empty
            try:
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    flash(
                        f"Deleted {deleted_count} file(s) and removed empty directory {dir_path}",
                        "success",
                    )
                else:
                    flash(
                        f"Deleted {deleted_count} file(s) from {dir_path}"
                        + (f" ({error_count} errors)" if error_count else ""),
                        "success" if error_count == 0 else "warning",
                    )
            except OSError:
                flash(
                    f"Deleted {deleted_count} file(s) from {dir_path} (directory not empty)",
                    "success",
                )

            # Mark directory as deleted in database
            cursor.execute(
                f"UPDATE directories SET deleted_at = {placeholder} WHERE id = {placeholder}",
                (datetime.now(), dir_id),
            )
            conn.commit()

            # Clear cached counts
            session.pop("counts", None)

            return redirect(request.referrer or url_for("index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>/delete/soft/recursive", methods=["POST"])
    def delete_directory_soft_recursive(dir_id):
        """Recursively soft delete a directory tree (all subdirs and files)."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory info
            cursor.execute(f"SELECT path, scan_id FROM directories WHERE id = {dir_id}")
            row = cursor.fetchone()

            if not row:
                flash(f"Directory #{dir_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            dir_path = row[0] if isinstance(row, tuple) else row["path"]
            scan_id = row[1] if isinstance(row, tuple) else row["scan_id"]

            # Get all subdirectories recursively using path prefix matching
            cursor.execute(
                f"SELECT id FROM directories WHERE scan_id = {scan_id} "
                f"AND (id = {dir_id} OR path LIKE {dir_path}{'/%' if dir_path else '%'})"
            )
            all_dir_ids = [r[0] if isinstance(r, tuple) else r["id"] for r in cursor.fetchall()]

            # Count files to be marked across all subdirectories
            dir_ids_str = ",".join(str(d) for d in all_dir_ids)
            cursor.execute(
                f"SELECT COUNT(*) FROM files "
                f"WHERE directory_id IN ({dir_ids_str}) AND deleted_at IS NULL"
            )
            files_count = cursor.fetchone()[0]

            # Define placeholder for parameterized queries
            placeholder = "?" if config.backend == "sqlite" else "%s"

            # Mark all files in directory tree as deleted
            if files_count > 0:
                cursor.execute(
                    f"UPDATE files SET deleted_at = {placeholder} "
                    f"WHERE directory_id IN ({dir_ids_str}) AND deleted_at IS NULL",
                    (datetime.now(),),
                )

            # Mark all directories in tree as deleted
            cursor.execute(
                f"UPDATE directories SET deleted_at = {placeholder} "
                f"WHERE id IN ({dir_ids_str}) AND deleted_at IS NULL",
                (datetime.now(),),
            )

            dirs_marked = cursor.rowcount
            conn.commit()

            if files_count == 0 and dirs_marked == 0:
                flash(f"No active files or directories in {dir_path}", "warning")
            else:
                flash(
                    f"Marked {files_count} file(s) and {dirs_marked} director{'y' if dirs_marked == 1 else 'ies'} "
                    f"in tree {dir_path} as deleted",
                    "success",
                )

            # Clear cached counts
            session.pop("counts", None)

            return redirect(url_for("directory_view", dir_id=dir_id))
        except Exception as e:
            conn.rollback()
            flash(f"Error deleting directory tree: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>/delete/hard/recursive", methods=["POST"])
    def delete_directory_hard_recursive(dir_id):
        """Recursively hard delete a directory tree from filesystem with detailed reporting."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory info
            cursor.execute(f"SELECT path, scan_id FROM directories WHERE id = {dir_id}")
            row = cursor.fetchone()

            if not row:
                flash(f"Directory #{dir_id} not found", "error")
                return redirect(request.referrer or url_for("index"))

            dir_path = row[0] if isinstance(row, tuple) else row["path"]
            scan_id = row[1] if isinstance(row, tuple) else row["scan_id"]

            # Check if directory exists on disk
            if not os.path.exists(dir_path):
                flash(
                    f"Directory {dir_path} not found on disk. "
                    f"Use soft delete if this is from removable/unmounted media.",
                    "error",
                )
                return redirect(request.referrer or url_for("index"))

            # Get all subdirectories recursively
            cursor.execute(
                f"SELECT id, path FROM directories WHERE scan_id = {scan_id} "
                f"AND (id = {dir_id} OR path LIKE '{dir_path}/%') "
                f"ORDER BY LENGTH(path) DESC"  # Process deepest first
            )
            all_dirs = cursor.fetchall()

            # Initialize tracking
            stats = {
                "files_marked": 0,
                "files_deleted": 0,
                "files_present": 0,
                "dirs_marked": 0,
                "dirs_deleted": 0,
                "errors": []
            }

            # Process each directory (deepest first for proper deletion)
            for dir_row in all_dirs:
                d_id = dir_row[0] if isinstance(dir_row, tuple) else dir_row["id"]
                d_path = dir_row[1] if isinstance(dir_row, tuple) else dir_row["path"]

                # Get all files in this directory
                cursor.execute(
                    f"SELECT id, filename FROM files WHERE directory_id = {d_id} AND deleted_at IS NULL"
                )
                files = cursor.fetchall()

                # Delete each file
                for file_row in files:
                    f_id = file_row[0] if isinstance(file_row, tuple) else file_row["id"]
                    filename = file_row[1] if isinstance(file_row, tuple) else file_row["filename"]
                    full_path = os.path.join(d_path, filename)

                    # Check if file exists
                    if os.path.exists(full_path):
                        stats["files_present"] += 1
                        try:
                            os.remove(full_path)
                            stats["files_deleted"] += 1
                        except PermissionError:
                            stats["errors"].append(f"Permission denied: {full_path}")
                        except OSError as e:
                            stats["errors"].append(f"Error deleting {full_path}: {e}")

                # Mark all files in this directory as deleted
                if files:
                    placeholder = "?" if config.backend == "sqlite" else "%s"
                    cursor.execute(
                        f"UPDATE files SET deleted_at = {placeholder} "
                        f"WHERE directory_id = {placeholder}",
                        (datetime.now(), d_id),
                    )
                    stats["files_marked"] += cursor.rowcount

                # Try to remove directory if it exists and is empty
                if os.path.exists(d_path):
                    try:
                        # Check for unindexed files
                        dir_contents = os.listdir(d_path)
                        if dir_contents:
                            stats["errors"].append(
                                f"Directory not empty (has {len(dir_contents)} unindexed items): {d_path}"
                            )
                        else:
                            os.rmdir(d_path)
                            stats["dirs_deleted"] += 1
                    except PermissionError:
                        stats["errors"].append(f"Permission denied for directory: {d_path}")
                    except OSError as e:
                        stats["errors"].append(f"Error removing directory {d_path}: {e}")

                # Mark directory as deleted
                placeholder = "?" if config.backend == "sqlite" else "%s"
                cursor.execute(
                    f"UPDATE directories SET deleted_at = {placeholder} WHERE id = {placeholder}",
                    (datetime.now(), d_id),
                )
                stats["dirs_marked"] += cursor.rowcount

            conn.commit()

            # Clear cached counts
            session.pop("counts", None)

            # Render summary page
            return render_template(
                "directory_delete_summary.html",
                directory_path=dir_path,
                stats=stats,
            )

        except Exception as e:
            conn.rollback()
            flash(f"Critical error: {e}", "error")
            return redirect(request.referrer or url_for("index"))
        finally:
            cursor.close()
            conn.close()

    @app.route("/file/<int:file_id>/check_exists", methods=["GET"])
    def check_file_exists(file_id):
        """Check if a file exists on disk (for AJAX)."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"""
                SELECT files.filename, directories.path
                FROM files
                JOIN directories ON files.directory_id = directories.id
                WHERE files.id = {file_id}
                """
            )
            row = cursor.fetchone()

            if not row:
                return {"exists": False, "error": "File not found in database"}

            if isinstance(row, tuple):
                filename, dir_path = row
            else:
                filename = row["filename"]
                dir_path = row["path"]

            full_path = os.path.join(dir_path, filename)
            exists = os.path.exists(full_path)

            return {"exists": exists, "path": full_path}
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>")
    def directory_view(dir_id):
        """View directory contents and manage files."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory info
            cursor.execute(
                f"""
                SELECT directories.id, directories.path, directories.scan_id,
                       directories.parent_id, scans.scan_path
                FROM directories
                JOIN scans ON directories.scan_id = scans.id
                WHERE directories.id = {dir_id}
                """
            )
            row = cursor.fetchone()

            if not row:
                flash(f"Directory #{dir_id} not found", "error")
                return redirect(url_for("index"))

            if isinstance(row, tuple):
                dir_id, dir_path, scan_id, parent_id, scan_path = row
            else:
                dir_id = row["id"]
                dir_path = row["path"]
                scan_id = row["scan_id"]
                parent_id = row["parent_id"]
                scan_path = row["scan_path"]

            # Get subdirectories
            cursor.execute(
                f"""
                SELECT id, path
                FROM directories
                WHERE parent_id = {dir_id} AND deleted_at IS NULL
                ORDER BY path
                """
            )
            subdirs = []
            for subdir_row in cursor.fetchall():
                if isinstance(subdir_row, tuple):
                    sub_id, sub_path = subdir_row
                else:
                    sub_id = subdir_row["id"]
                    sub_path = subdir_row["path"]
                subdirs.append({"id": sub_id, "path": sub_path})

            # Get files in this directory
            cursor.execute(
                f"""
                SELECT id, filename, extension, size, mtime, md5_hash, deleted_at
                FROM files
                WHERE directory_id = {dir_id} AND deleted_at IS NULL
                ORDER BY filename
                """
            )
            files = []
            for file_row in cursor.fetchall():
                if isinstance(file_row, tuple):
                    fid, fname, ext, size, mtime, md5, deleted = file_row
                else:
                    fid = file_row["id"]
                    fname = file_row["filename"]
                    ext = file_row["extension"]
                    size = file_row["size"]
                    mtime = file_row["mtime"]
                    md5 = file_row["md5_hash"]
                    deleted = file_row["deleted_at"]

                files.append(
                    {
                        "id": fid,
                        "filename": fname,
                        "extension": ext,
                        "size": size,
                        "mtime": mtime,
                        "md5": md5,
                    }
                )

            # Count total files and size
            total_files = len(files)
            total_size = sum(f["size"] for f in files)

            return render_template(
                "directory.html",
                directory={
                    "id": dir_id,
                    "path": dir_path,
                    "scan_id": scan_id,
                    "parent_id": parent_id,
                    "scan_path": scan_path,
                },
                subdirs=subdirs,
                files=files,
                total_files=total_files,
                total_size=total_size,
            )
        finally:
            cursor.close()
            conn.close()

    @app.route("/directory/<int:dir_id>/check_duplicates", methods=["POST"])
    def directory_check_duplicates(dir_id):
        """Check for duplicates within a directory tree."""
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get directory path for display
            cursor.execute(f"SELECT path FROM directories WHERE id = {dir_id}")
            dir_row = cursor.fetchone()
            if not dir_row:
                flash("Directory not found", "error")
                return redirect(url_for("index"))

            dir_path = dir_row[0] if isinstance(dir_row, tuple) else dir_row["path"]

            # Get all subdirectories recursively using a recursive query approach
            # First, collect all descendant directory IDs
            all_dir_ids = [dir_id]
            cursor.execute(f"SELECT id FROM directories WHERE parent_id = {dir_id}")
            child_dirs = [
                r[0] if isinstance(r, tuple) else r["id"] for r in cursor.fetchall()
            ]

            while child_dirs:
                all_dir_ids.extend(child_dirs)
                placeholders = ",".join(str(d) for d in child_dirs)
                cursor.execute(
                    f"SELECT id FROM directories WHERE parent_id IN ({placeholders})"
                )
                child_dirs = [
                    r[0] if isinstance(r, tuple) else r["id"] for r in cursor.fetchall()
                ]

            # Get all files in this directory tree
            dir_ids_str = ",".join(str(d) for d in all_dir_ids)
            cursor.execute(
                f"""
                SELECT id, filename, size, md5_hash, directory_id
                FROM files
                WHERE directory_id IN ({dir_ids_str})
                  AND deleted_at IS NULL
                  AND NOT COALESCE(ignored, false)
                  AND md5_hash IS NOT NULL
                  AND md5_hash != ''
                """
            )

            files_by_hash = {}
            all_files = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    fid, fname, size, md5, did = row
                else:
                    fid = row["id"]
                    fname = row["filename"]
                    size = row["size"]
                    md5 = row["md5_hash"]
                    did = row["directory_id"]

                file_info = {
                    "id": fid,
                    "filename": fname,
                    "size": size,
                    "md5": md5,
                    "directory_id": did,
                }
                all_files.append(file_info)

                if md5 not in files_by_hash:
                    files_by_hash[md5] = []
                files_by_hash[md5].append(file_info)

            # Find duplicates (files with same hash appearing multiple times)
            duplicate_hashes = {
                h: files for h, files in files_by_hash.items() if len(files) > 1
            }

            # Calculate statistics
            total_files = len(all_files)
            total_size = sum(f["size"] for f in all_files)

            duplicate_files = []
            duplicate_size = 0
            for hash_val, files_list in duplicate_hashes.items():
                duplicate_files.extend(files_list)
                # Wasted space is (count - 1) * size
                duplicate_size += files_list[0]["size"] * (len(files_list) - 1)

            unique_files = [f for f in all_files if f["md5"] not in duplicate_hashes]

            # Get up to 10 examples of duplicates
            duplicate_examples = []
            for hash_val, files_list in list(duplicate_hashes.items())[:10]:
                # Get directory paths for each file
                file_paths = []
                for f in files_list:
                    cursor.execute(
                        f"SELECT path FROM directories WHERE id = {f['directory_id']}"
                    )
                    path_row = cursor.fetchone()
                    path = (
                        path_row[0] if isinstance(path_row, tuple) else path_row["path"]
                    )
                    file_paths.append(
                        {
                            "id": f["id"],
                            "filename": f["filename"],
                            "path": os.path.join(path, f["filename"]),
                            "size": f["size"],
                        }
                    )

                duplicate_examples.append(
                    {
                        "md5": hash_val,
                        "count": len(files_list),
                        "size": files_list[0]["size"],
                        "files": file_paths,
                    }
                )

            # Get up to 10 examples of unique files
            unique_examples = []
            for f in unique_files[:10]:
                cursor.execute(
                    f"SELECT path FROM directories WHERE id = {f['directory_id']}"
                )
                path_row = cursor.fetchone()
                path = path_row[0] if isinstance(path_row, tuple) else path_row["path"]
                unique_examples.append(
                    {
                        "id": f["id"],
                        "filename": f["filename"],
                        "path": os.path.join(path, f["filename"]),
                        "size": f["size"],
                    }
                )

            return render_template(
                "directory_duplicates.html",
                directory_id=dir_id,
                directory_path=dir_path,
                total_files=total_files,
                total_size=total_size,
                duplicate_count=len(duplicate_files),
                duplicate_size=duplicate_size,
                duplicate_examples=duplicate_examples,
                unique_count=len(unique_files),
                unique_examples=unique_examples,
            )

        finally:
            cursor.close()
            conn.close()

    return app


def run_server(host="127.0.0.1", port=5000, debug=True):
    """Run the Flask development server."""
    app = create_app()
    print("\n🌐 Starting diskindex web UI...")
    print(f"📍 Open your browser to: http://{host}:{port}")
    print("⏹️  Press Ctrl+C to stop\n")
    app.run(host=host, port=port, debug=debug)
