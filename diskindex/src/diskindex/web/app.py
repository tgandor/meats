"""Flask web application for diskindex."""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

from diskindex.config import load_config
from diskindex.database import DatabaseConfig


def create_app(config: DatabaseConfig = None):
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

            cursor.execute("SELECT COUNT(*) FROM files WHERE deleted_at IS NULL")
            file_count = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(size) FROM files WHERE deleted_at IS NULL")
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
                    f"SELECT COUNT(*) FROM files WHERE scan_id = {scan_id} AND deleted_at IS NULL"
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
        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, scan_date, scan_path, duration_seconds, notes "
                "FROM scans ORDER BY scan_date DESC"
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
                    f"WHERE scan_id = {scan_id} AND deleted_at IS NULL"
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

            return render_template("scans.html", scans=scan_list)
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
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL"
            )
            count_row = cursor.fetchone()
            scan_data["file_count"] = count_row[0]
            scan_data["total_size"] = count_row[1] or 0

            # Get file type breakdown
            cursor.execute(
                f"SELECT extension, COUNT(*), SUM(size) FROM files "
                f"WHERE scan_id = {scan_id} AND deleted_at IS NULL "
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

    @app.route("/search")
    def search():
        """Search for files."""
        query = request.args.get("q", "")
        extension = request.args.get("ext", "")
        min_size = request.args.get("min_size", type=int)
        max_size = request.args.get("max_size", type=int)

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Build search query
            conditions = ["files.deleted_at IS NULL"]
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

            # Get results
            sql = f"""
                SELECT files.id, files.filename, files.extension, files.size,
                       files.mtime, files.md5_hash, directories.path, scans.scan_path
                FROM files
                JOIN directories ON files.directory_id = directories.id
                JOIN scans ON files.scan_id = scans.id
                WHERE {where_clause}
                ORDER BY files.size DESC
                LIMIT 100
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

            return render_template(
                "search.html", query=query, extension=extension, results=results
            )
        finally:
            cursor.close()
            conn.close()

    @app.route("/duplicates")
    def duplicates():
        """Find and display duplicate files."""
        min_size = request.args.get("min_size", 1024, type=int)  # Default 1KB minimum

        conn = config.get_connection()
        cursor = conn.cursor()

        try:
            # Find files with same size and hash (duplicates)
            sql = """
                SELECT md5_hash, size, COUNT(*) as dup_count
                FROM files
                WHERE deleted_at IS NULL
                  AND md5_hash IS NOT NULL
                  AND md5_hash != ''
                  AND size >= ?
                GROUP BY md5_hash, size
                HAVING COUNT(*) > 1
                ORDER BY size DESC, dup_count DESC
                LIMIT 100
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
                    WHERE files.md5_hash = ? AND files.deleted_at IS NULL
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

            # Calculate total wasted space
            total_wasted = sum(g["wasted_space"] for g in duplicate_groups)

            return render_template(
                "duplicates.html",
                duplicate_groups=duplicate_groups,
                total_wasted=total_wasted,
                min_size=min_size,
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

    return app


def run_server(host="127.0.0.1", port=5000, debug=True):
    """Run the Flask development server."""
    app = create_app()
    print(f"\n🌐 Starting diskindex web UI...")
    print(f"📍 Open your browser to: http://{host}:{port}")
    print(f"⏹️  Press Ctrl+C to stop\n")
    app.run(host=host, port=port, debug=debug)
