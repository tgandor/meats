import argparse
import os

from sqlalchemy import create_engine

parser = argparse.ArgumentParser()
parser.add_argument("conn_string")
args = parser.parse_args()

conn_string = (
    open(args.conn_string).read()
    if os.path.exists(args.conn_string)
    else args.conn_string
)

engine = create_engine(conn_string)

while True:
    query = input("sql> ")
    if not query:
        continue
    if query == "q":
        break
    result = engine.execute(query)
    for i, row in enumerate(result):
        if not i:
            print(tuple(row.keys()))
        print(row)
    print(i + 1, "rows returned")
