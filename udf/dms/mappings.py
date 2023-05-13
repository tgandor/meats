#!/usr/bin/env python

import argparse
import copy
import json

import yaml

# config constants
SRC_SCHEMA = "dbo"
# magic constants
RULES = "rules"
LOCATOR = "object-locator"
TABNAME = "table-name"
SCHEMA = "schema-name"
RULE_ID = "rule-id"
RULE_NAME = "rule-name"
# rule template
TEMPLATE = {
    "rule-type": "selection",
    "rule-id": "1",
    "rule-name": "1",
    "object-locator": {"schema-name": SRC_SCHEMA, "table-name": "table"},
    "rule-action": "include",
}

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--key", "-k")
parser.add_argument("--add-table", "-a")
parser.add_argument("--add-tables", "-A")
parser.add_argument("--output", "-o")
parser.add_argument("--edit", "-w", action="store_true")
args = parser.parse_args()

maps = yaml.safe_load(open(args.input))

if not args.key:
    print("Please specify --key/-k to modify specific mappings.")
    print("Available keys:")
    print(json.dumps([*maps.keys()], indent=2))
    exit()

rules = json.loads(maps[args.key])[RULES]

all_tables = [x[LOCATOR][TABNAME] for x in rules]
existing = {*all_tables}


def _add(table):
    if table in existing:
        print(f"{table} already in mapping. Not adding.")
        return False

    rule = copy.deepcopy(TEMPLATE)  # locator is nested!
    rule[LOCATOR][TABNAME] = table
    rules.append(rule)
    return True


if args.add_table:
    _add(args.add_table)

if args.add_tables:
    tables = [x.strip() for x in open(args.add_tables)]
    done = sum(_add(table) for table in tables)
    print(f"Added {done} of {len(tables)} tables.")

new_rules = sorted(
    rules, key=lambda x: (x[LOCATOR][TABNAME] == "%", x[LOCATOR][TABNAME].lower())
)
seen = set()
filtered = []

rule_id = 1001
for rule in new_rules:
    if rule["rule-type"] == "transformation":
        filtered.append(rule)
        continue
    name = rule[LOCATOR][TABNAME]
    if name == "%":
        filtered.append(rule)
        continue
    if name in seen:
        print(f"Skipping repeated rule for {name}.")
        continue
    seen.add(name)
    rule[RULE_ID] = str(rule_id)
    rule[RULE_NAME] = str(rule_id)
    rule[LOCATOR][SCHEMA] = SRC_SCHEMA
    rule_id += 1
    filtered.append(rule)

new_rules = filtered

maps[args.key] = json.dumps({"rules": new_rules}, indent=2)


def _save(mappings, filename):
    with open(filename, "w") as cfg:
        yaml.safe_dump(mappings, cfg, default_style="|")
    print(f"Mappings saved to {filename}.")


if args.output:
    _save(maps, args.output)

if args.edit:
    _save(maps, args.input)
