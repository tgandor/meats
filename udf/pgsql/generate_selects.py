import argparse
import getpass
import pathlib
import typing

import psycopg2


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
        assert self.engine == "postgres"

        if set(self.password) == {"*"}:
            self.password = getpass.getpass(f"Password for {self.user}")

        return (
            f"dbname={self.database} "
            f"host={self.host} "
            f"port={self.port} "
            f"user={self.user} "
            f"password={self.password}"
        )

    def get_connection(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(self.connection_string())


ANSI_TABLES = """
    select table_schema, table_name
    from information_schema.tables
    where table_type='BASE TABLE'
    and table_schema not in ('pg_catalog', 'information_schema')
    {filter}
"""

ANSI_COLUMNS = """
    select COLUMN_NAME
    , DATA_TYPE
    , IS_NULLABLE
    from information_schema.columns
    where TABLE_NAME='{name}' and TABLE_SCHEMA='{schema}'
    order by ORDINAL_POSITION
"""


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials", type=pathlib.Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")
    parser.add_argument("--long", "-l", action="store_true")
    parser.add_argument("--fix-bool", "-b", action="store_true")
    parser.add_argument("--name", "-n")
    args = parser.parse_args()
    return args


def find_tables(conn, filter=None, v=False):
    condition = "" if filter is None else f"and table_name like '{filter}'"
    sql = ANSI_TABLES.format(filter=condition)
    if v:
        print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def cast_bool_to_int(columns):
    return [(f"{c[0]}::int", "int", c[2]) if c[1] == "boolean" else c for c in columns]


def get_columns(conn, schema, name, v=False):
    sql = ANSI_COLUMNS.format(**locals())
    if v:
        print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def format_select(schema, name, columns, long=False):
    if not long:
        fields = ", ".join(c[0] for c in columns)
    else:
        fields = (
            "\n  , ".join(
                f"{c[0]} -- {c[1]} {'not ' if c[2]=='NO' else ''}null" for c in columns
            )
            + "\n"
        )
    return f"SELECT {fields} from {schema}.{name}"


def main():
    args = _parse_cli()
    conn = ConnParams.from_file(args.credentials).get_connection()

    if args.test:
        print(conn)
        return

    tables = find_tables(conn, args.name, args.verbose)

    for schema, name in tables:
        columns = get_columns(conn, schema, name, args.verbose)
        if args.fix_bool:
            columns = cast_bool_to_int(columns)
        print(format_select(schema, name, columns, args.long))


if __name__ == "__main__":
    main()
