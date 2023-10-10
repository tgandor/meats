#!/usr/bin/env python

import argparse
import json
import os
import time

import psycopg2
from pyperclip import paste


TEMPLATE = {"dbname": "", "user": "", "password": "", "host": "", "port": ""}


def gen_clipboard():
    old_clipboard = paste()
    while True:
        time.sleep(0.2)
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials_file")
    parser.add_argument("--reset", "-r", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def load(path):
    with open(path) as p:
        return json.load(p)


def save(path, data):
    with open(path, "w") as p:
        json.dump(data, p)


def test(data):
    try:
        conn = psycopg2.connect(**data)
        conn.close()
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False


def check_and_save(path, data):
    if test(data):
        save(path, data)
        print(f"Credentials saved to '{path}")
    else:
        print("Connection failed. Not saving file.")


def fill_out(verbose=False):
    gen = gen_clipboard()
    data = {}
    for key in TEMPLATE:
        print(f"Please copy '{key}':")
        value = next(gen)
        if verbose:
            print(f"  got: {value}")
        data[key] = value
    print("Done.")
    return data


def patch(data, verbose=False):
    gen = gen_clipboard()
    data = {}
    for key in ("user", "password"):
        print(f"Please copy '{key}':")
        value = next(gen)
        if verbose:
            print(f"  got: {value}")
        data[key] = value
    print("Done.")
    return data


def main():
    args = parse_args()
    path = args.credentials_file
    if not os.path.exists(path) or args.reset:
        data = fill_out(args.verbose)
        check_and_save(path, data)
        return

    data = load(args.credentials_file)
    if test(data):
        print("Credentials work. Finishing.")
    else:
        data = patch(data, args.verbose)
        check_and_save(path, data)


if __name__ == "__main__":
    main()
