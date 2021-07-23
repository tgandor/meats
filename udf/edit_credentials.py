#!/usr/bin/env python

import argparse
import dataclasses
import pathlib
import time

from pyperclip import paste


def gen_clipboard():
    old_clipboard = paste()
    while True:
        time.sleep(0.2)
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


OPTIONALS = "database host port".split(" ")


@dataclasses.dataclass
class Credentials:
    engine: str
    database: str = None
    host: str = None
    port: str = None
    user: str = None
    password: str = None

    @classmethod
    def from_file(cls, file: pathlib.Path):
        with file.open() as f:
            return cls(*f)

    def save(self, file: pathlib.Path):
        with file.open("w") as f:
            print("\n".join(dataclasses.asdict(self).values()), file=f)

    def _ask(self, clip, field: str):
        print(f"Please copy: {field}")
        value = next(clip)
        print(value)
        setattr(self, field, value)

    def _ask_maybe(self, clip, field: str):
        if getattr(self, field) is None:
            self._ask(clip, field)

    def populate(self):
        cg = gen_clipboard()

        for optional in OPTIONALS:
            self._ask_maybe(cg, optional)

        self._ask(cg, "user")
        self._ask(cg, "password")


def main():
    parser = argparse.ArgumentParser("creds")
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument("--mssql", "-m", action="store_true", help="create for MS SQL")
    parser.add_argument("--port", "-p", action="store_true", help="ask for port")
    parser.add_argument(
        "--database", "-d", action="store_true", help="ask for DB instance"
    )
    parser.add_argument("--host", "-s", action="store_true", help="ask for hostname")
    args = parser.parse_args()

    if args.mssql:
        defaults = {
            "engine": "mssql",
            "port": "1433",
        }
    else:
        defaults = {
            "engine": "postgres",
            "port": "5432",
        }

    credentials = (
        Credentials.from_file(args.output)
        if args.output.exists()
        else Credentials(**defaults)
    )

    # clean
    for optional in OPTIONALS:
        if getattr(args, optional):
            setattr(credentials, optional, None)

    credentials.populate()

    credentials.save(args.output)


if __name__ == "__main__":
    main()
