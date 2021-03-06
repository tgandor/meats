import argparse
import getpass
from os import path
import pathlib
import time
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


ANSI_TABLES = """
    select table_schema, table_name
    from information_schema.tables
    where table_type='BASE TABLE'
    and table_schema not in ('pg_catalog', 'information_schema')
    order by table_schema, table_name
"""


def dump_database(
    conn: pyodbc.Connection,
    output: str,
    v: bool = False,
    dry: bool = False,
    format: str = "csv",
):
    if v:
        print(ANSI_TABLES)
    tables = pd.read_sql(ANSI_TABLES, conn)

    out_dir = pathlib.Path(output)
    if not dry:
        out_dir.mkdir(exist_ok=True)

    for idx, (schema, table) in tables.iterrows():
        sql = f"select * from [{schema}].[{table}]"
        if v:
            print(sql)
        data = pd.read_sql(sql, conn)
        if v:
            data.info()
            print("-" * 60)

        if len(data) == 0:
            print(f"Skipping empty table: {schema}.{table}")
            continue

        out_file = out_dir / f"{schema}.{table}.{format}"
        if not dry:
            if format == "csv":
                data.to_csv(out_file, index=False)
            elif format == "json":
                data.to_json(out_file, indent=2)
            else:
                print(f"Error: format {format} not yet supported.")
        else:
            print(f"Not writing to {out_file} (dry run)")


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials", type=pathlib.Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", "-n", action="store_true")
    parser.add_argument("--format", "-f", default="csv")
    parser.add_argument("--output", "-o", help="Ouput folder")
    parser.add_argument("--test", "-t", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        args.verbose = True
    return args


def main():
    args = _parse_cli()
    params = ConnParams.from_file(args.credentials)
    conn = params.get_connection()

    if args.test:
        print(conn)
        return

    output = args.output or params.database
    dump_database(conn, output, args.verbose, args.dry_run, args.format)


if __name__ == "__main__":
    start = time.time()
    try:
        main()
    finally:
        print(f"Done. {time.time()-start:.3f} s")
