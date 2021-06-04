import argparse
import getpass
import pathlib
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
    parser.add_argument("username", nargs="?")
    parser.add_argument("password", nargs="?")
    parser.add_argument("--grants", type=pathlib.Path, default="grants.txt")
    parser.add_argument("--databases", type=pathlib.Path, default="databases.txt")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def create_login(conn: pyodbc.Connection, username: str, password: str, v: bool):
    cursor = conn.cursor()
    sql = f"""
        IF NOT EXISTS(
            SELECT principal_id
            FROM sys.server_principals
            WHERE name='{username}'
        ) BEGIN
            CREATE LOGIN {username}
            WITH PASSWORD = '{password}'
        END
    """
    if v:
        print(sql)
    cursor.execute(sql)
    conn.commit()


def add_login_to_databases(
    conn: pyodbc.Connection, username: str, databases: typing.List[str], v: bool
):
    cursor = conn.cursor()

    for database in databases:
        sql = f"""
            USE {database};
            IF NOT EXISTS(
                SELECT principal_id
                FROM sys.database_principals
                WHERE name='{username}'
            ) BEGIN
                CREATE USER {username} FOR LOGIN {username}
            END
        """
        if v:
            print(sql)
        cursor.execute(sql)
        conn.commit()


def grant_permissions_to_user(
    conn: pyodbc.Connection,
    username: str,
    databases: typing.List[str],
    grants: typing.List[str],
    v: bool,
):
    cursor = conn.cursor()

    for database in databases:
        sql = f"""
            USE {database};
            GRANT {', '.join(grants)} on DATABASE::[{database}] to {username}
        """
        if v:
            print(sql)
        cursor.execute(sql)
        conn.commit()


def _lines(path: pathlib.Path) -> typing.List[str]:
    return path.read_text().strip().split("\n")


def main():
    args = _parse_cli()
    conn = ConnParams.from_file(args.credentials).get_connection()
    username = args.username or input()
    password = args.password or getpass.getpass()
    databases = _lines(args.databases)
    grants = _lines(args.grants)
    create_login(conn, username, password, args.verbose)
    add_login_to_databases(conn, username, databases, args.verbose)
    grant_permissions_to_user(conn, username, databases, grants, args.verbose)


if __name__ == "__main__":
    main()
