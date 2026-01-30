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
                "SELECT COUNT(*) FROM files WHERE deleted_at IS NULL AND NOT COALESCE(ignored, 0)"
            )
            file_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT SUM(size) FROM files WHERE deleted_at IS NULL AND NOT COALESCE(ignored, 0)"
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
                    f"SELECT COUNT(*) FROM files WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, 0)"
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

                # Get file count and total size
                cursor.execute(
                    f"SELECT COUNT(*), SUM(size) FROM files "
                    f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, 0)"
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

            # Get file statistics
            cursor.execute(
                f"SELECT COUNT(*), SUM(size) FROM files "
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, 0)"
            )
            count_row = cursor.fetchone()
            scan_data["file_count"] = count_row[0]
            scan_data["total_size"] = count_row[1] or 0

            # Get file type breakdown
            cursor.execute(
                f"SELECT extension, COUNT(*), SUM(size) FROM files "
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL AND NOT COALESCE(ignored, 0) "
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

            return render_template(
                "scan_detail.html", scan=scan_data, extensions=extensions
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

            # Delete the scan (CASCADE will delete all related records)
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
        page, per_page, offset = get_page_args()

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Build search query
            conditions = ["files.deleted_at IS NULL", "NOT COALESCE(files.ignored, 0)"]
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

            where_clause = " AND ".join(conditions)

            # Get total count (cached with search params)
            cache_key = f"search_count_{hash((query, extension, min_size, max_size))}"
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
                       files.mtime, files.md5_hash, directories.path, scans.scan_path
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
                    file_id, filename, ext, size, mtime, md5, dir_path, scan_path = row
                else:
                    file_id = row["id"]
                    filename = row["filename"]
                    ext = row["extension"]
                    size = row["size"]
                    mtime = row["mtime"]
                    md5 = row["md5_hash"]
                    dir_path = row["path"]
                    scan_path = row["scan_path"]

                full_path = os.path.join(dir_path, filename)

                results.append(
                    {
                        "id": file_id,
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
        page, per_page, offset = get_page_args()

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Get total count of duplicate groups (cached with min_size)
            cache_key = f"duplicates_count_{min_size}"
            total_count = get_cached_count(cache_key)

            if total_count is None:
                count_sql = """
                    SELECT COUNT(*) FROM (
                        SELECT md5_hash
                        FROM files
                        WHERE deleted_at IS NULL
                          AND NOT COALESCE(ignored, 0)
                          AND md5_hash IS NOT NULL
                          AND md5_hash != ''
                          AND size >= ?
                        GROUP BY md5_hash, size
                        HAVING COUNT(*) > 1
                    )
                """
                cursor.execute(count_sql, (min_size,))
                total_count = cursor.fetchone()[0]
                set_cached_count(cache_key, total_count)

            # Find files with same size and hash (duplicates) with pagination
            sql = f"""
                SELECT md5_hash, size, COUNT(*) as dup_count
                FROM files
                WHERE deleted_at IS NULL
                  AND NOT COALESCE(ignored, 0)
                  AND md5_hash IS NOT NULL
                  AND md5_hash != ''
                  AND size >= ?
                GROUP BY md5_hash, size
                HAVING COUNT(*) > 1
                ORDER BY size DESC, dup_count DESC
                LIMIT {per_page} OFFSET {offset}
            """

            cursor.execute(sql, (min_size,))

            duplicate_groups = []
            for row in cursor.fetchall():
                if isinstance(row, tuple):
                    md5, size, count = row
                else:
                    md5 = row["md5_hash"]
                    size = row["size"]
                    count = row["dup_count"]

                # Get all files in this duplicate group
                cursor.execute(
                    """
                    SELECT files.filename, directories.path, scans.scan_path, files.id
                    FROM files
                    JOIN directories ON files.directory_id = directories.id
                    JOIN scans ON files.scan_id = scans.id
                    WHERE files.md5_hash = ? AND files.deleted_at IS NULL AND NOT COALESCE(files.ignored, 0)
                    ORDER BY files.filename
                    """,
                    (md5,),
                )

                files = []
                for file_row in cursor.fetchall():
                    if isinstance(file_row, tuple):
                        filename, dir_path, scan_path, file_id = file_row
                    else:
                        filename = file_row["filename"]
                        dir_path = file_row["path"]
                        scan_path = file_row["scan_path"]
                        file_id = file_row["id"]

                    full_path = os.path.join(dir_path, filename)
                    files.append(
                        {
                            "id": file_id,
                            "filename": filename,
                            "path": full_path,
                            "scan_path": scan_path,
                        }
                    )

                wasted_space = size * (count - 1)  # Space used by duplicates

                duplicate_groups.append(
                    {
                        "md5": md5,
                        "size": size,
                        "count": count,
                        "wasted_space": wasted_space,
                        "files": files,
                    }
                )

            # Calculate total wasted space across ALL duplicates (not just this page)
            if total_count > 0:
                cursor.execute(
                    """
                    SELECT SUM(size * (dup_count - 1)) FROM (
                        SELECT size, COUNT(*) as dup_count
                        FROM files
                        WHERE deleted_at IS NULL
                          AND NOT COALESCE(ignored, 0)
                          AND md5_hash IS NOT NULL
                          AND md5_hash != ''
                          AND size >= ?
                        GROUP BY md5_hash, size
                        HAVING COUNT(*) > 1
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

    return app


def run_server(host="127.0.0.1", port=5000, debug=True):
    """Run the Flask development server."""
    app = create_app()
    print("\n🌐 Starting diskindex web UI...")
    print(f"📍 Open your browser to: http://{host}:{port}")
    print("⏹️  Press Ctrl+C to stop\n")
    app.run(host=host, port=port, debug=debug)
