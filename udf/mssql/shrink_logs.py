import argparse
import getpass
import pathlib
import typing

import pyodbc
import pandas as pd


class ConnParams(typing.NamedTuple):
    engine: str
    database: str
    host: str
    port: str
    user: str
    password: str

    @classmethod
    def from_file(cls, cred_file: pathlib.Path):
        with cred_file.open() as cf:
            return cls(*map(str.strip, cf))

    def connection_string(self) -> str:
        assert self.engine == "mssql"

        if self.user == "TRUSTED" and self.password == "CONNECTION":
            return (
                "Driver={SQL Server};"
                f"Server={self.host};"
                f"Database={self.database};"
                "Trusted_Connection=yes"
            )

        if set(self.password) == {"*"}:
            self.password = getpass.getpass(f"Password for {self.user}")

        return (
            "Driver={SQL Server};"
            f"Server={self.host};"
            f"Database={self.database};"
            f"UID={self.user};"
            f"PWD={self.password};"
            "Trusted_Connection=no"
        )

    def get_connection(self) -> pyodbc.Connection:
        return pyodbc.connect(self.connection_string())


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials", type=pathlib.Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", "-n", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        args.verbose = True
    return args


def get_log_files(conn: pyodbc.Connection, v: bool = False):
    sql = """
        SELECT DB_NAME(database_id) AS database_name,
            type_desc,
            name AS file_name,
            cast(size/128.0 as integer) AS size_mb
        FROM sys.master_files
        WHERE type_desc='LOG' AND database_id > 4
        ORDER BY DB_NAME(database_id)
    """
    if v:
        print(sql)

    return pd.read_sql(sql, conn)


def shrink_log_files(conn: pyodbc.Connection, v: bool, dry: bool):
    print('Before shrink:')
    logs = get_log_files(conn, v)
    print(logs)

    for i, row in logs.iterrows():
        sql = f"""
            USE [{row['database_name']}];
            DBCC SHRINKFILE (N'{row['file_name']}' , 0, TRUNCATEONLY)
        """
        if v:
            print(sql)
        if not dry:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.commit()

    if not dry:
        print('After shrink:')
        logs = get_log_files(conn)
        print(logs)


def main():
    args = _parse_cli()
    conn = ConnParams.from_file(args.credentials).get_connection()
    if args.test:
        print(conn)
        return
    shrink_log_files(conn, args.verbose, args.dry_run)


if __name__ == "__main__":
    main()
