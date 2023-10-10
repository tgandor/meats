#!/usr/bin/env python

import argparse
import csv
import datetime
import json

import psycopg2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials_file")
    parser.add_argument("schema")
    parser.add_argument("table")
    parser.add_argument("--key", "-k", action="store_true", help="only save PK")
    parser.add_argument("--output", "-o")
    parser.add_argument("--chunk", "-c", type=int, default=1000000)
    return parser.parse_args()


def load(path):
    with open(path) as p:
        return json.load(p)


def connect(path):
    return psycopg2.connect(**load(path))


def get_primary_keys(conn, schema, table):
    try:
        cursor = conn.cursor()
        sql_query = f"""
        SELECT column_name
        FROM information_schema.key_column_usage
        where key_column_usage.position_in_unique_constraint is null
        AND table_schema = '{schema}'
        AND table_name = '{table}';
        """
        print(sql_query)
        cursor.execute(sql_query)
        return [row[0] for row in cursor.fetchall()]
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


def export_table_to_csv(
    conn, schema, table, columns, keys, csv_filename=None, chunk_size=1000000
):
    if csv_filename is None:
        csv_filename = ".".join((schema, table, "csv"))

    try:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_rows = cursor.fetchone()[0]
        print(f"{total_rows=}")

        with open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write column headers
            cursor.execute(f"SELECT {', '.join(columns)} FROM {table} LIMIT 0")
            column_names = [desc[0] for desc in cursor.description]
            csv_writer.writerow(column_names)

            offset = 0
            cursor.execute(
                f"SELECT {', '.join(columns)} FROM {table} order by {', '.join(keys)}"
            )
            while offset < total_rows:
                # Fetch data in chunks using fetchmany()
                rows = cursor.fetchmany(chunk_size)
                csv_writer.writerows(rows)
                offset += chunk_size
                print(datetime.datetime.now(), offset)

        print(f"Data from table '{table}' exported to '{csv_filename}' successfully.")
    except (psycopg2.Error, IOError) as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def main():
    args = parse_args()
    try:
        conn = connect(args.credentials_file)
        pks = get_primary_keys(conn, args.schema, args.table)
        print(f"Primary key(s): {pks}")
        export_table_to_csv(
            conn, args.schema, args.table, pks if args.key else "*", pks, args.output
        )
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
