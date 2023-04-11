#!/usr/bin/env python

import argparse
import json
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("dump_file")
parser.add_argument("find")
parser.add_argument("replace", nargs="?")
parser.add_argument("--count", "-c", action="store_true")
parser.add_argument("--show", "-s", action="store_true")
args = parser.parse_args()


def search_table_simple(tab):
    fields = set()
    for row in tab["data"]:
        for key, val in row.items():
            if not isinstance(val, str):
                continue
            if args.find in val:
                fields.add(key)
    if fields:
        print(tab["name"], fields)


def search_table_count(tab):
    fields = Counter()
    for row in tab["data"]:
        for key, val in row.items():
            if not isinstance(val, str):
                continue
            if args.find in val:
                fields[key] += 1
    if fields:
        print(tab["name"], fields)


def search_table_show(tab):
    for row in tab["data"]:
        for key, val in row.items():
            if not isinstance(val, str):
                continue
            if args.find in val:
                print(f"{tab['name']}.{key}: {val}")


def search_table_replace(tab):
    fields = set()
    for row in tab["data"]:
        for key, val in row.items():
            if not isinstance(val, str):
                continue
            if args.find in val:
                fields.add(key)
    for field in fields:
        print(
            f"update {tab['name']} set {field} = replace({field}, '{args.find}', '{args.replace}') "
            f"where {field} like '%{args.find}%';"
        )


def search_table(tab):
    if args.count:
        search_table_count(tab)
    elif args.show:
        search_table_show(tab)
    elif args.replace is not None:
        search_table_replace(tab)
    else:
        search_table_simple(tab)


with open(args.dump_file) as df:
    data = json.load(df)

assert isinstance(data, list)

for obj in data:
    if obj["type"] == "table":
        search_table(obj)
