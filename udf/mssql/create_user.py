import argparse
import getpass
import pathlib
import time
import typing

import pyodbc


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
    parser.add_argument("master_credentials", type=pathlib.Path)
    # parser.add_argument("databases", type=pathlib.Path)
    # parser.add_argument("grants", type=pathlib.Path)
    parser.add_argument("username", nargs="?")
    parser.add_argument("password", nargs="?")
    return parser.parse_args()


def create_login(conn: pyodbc.Connection, username: str, password: str):
    cursor = conn.cursor()
    cursor.execute(f"""
    IF NOT EXISTS(
        SELECT principal_id FROM sys.server_principals WHERE name='{username}'
    ) BEGIN
        CREATE LOGIN {username}
        WITH PASSWORD = '{password}'
    END
    """)
    conn.commit()


def main():
    args = _parse_cli()
    conn = ConnParams.from_file(args.master_credentials).get_connection()
    username = args.username or getpass.getuser()
    password = args.password or getpass.getpass()
    create_login(conn, username, password)
