#!/usr/bin/env python

import argparse
import datetime
import glob
import json
import os
import re
import shutil
import stat
import subprocess
import sys

CONFIG = "monorepo.json"
LOCAL = "mr.py"
SYMLINK = True


def _install():
    if sys.platform.startswith("linux"):
        if not SYMLINK:
            shutil.copyfile(__file__, LOCAL)
            mode = os.stat(LOCAL).st_mode
            os.chmod(LOCAL, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"Local copy '{LOCAL}' of script '{__file__}' created.")
        else:
            os.symlink(os.path.abspath(__file__), LOCAL)
            print(f"Local symlink '{LOCAL}' to '{__file__}' created.")
    else:
        with open("mr.bat", "w") as mr:
            print("@echo off", file=mr)
            print(f'"{sys.executable}" "{os.path.abspath(__file__)}" %*', file=mr)
            print(f"Local entrypoint 'mr.bat' to '{__file__}' created.")


def _load_cfg(ignore_missing=False):
    if os.path.exists(CONFIG):
        with open(CONFIG) as cfg:
            return json.load(cfg)
    if ignore_missing:
        print("Creating new monorepo config.")
        if not os.path.exists(LOCAL):
            _install()
        return {}


def _save_cfg(config):
    with open(CONFIG, "w") as cfg:
        json.dump(config, cfg, indent=2)
        print(file=cfg)


def _url_to_dir(url):
    if os.path.isdir(url):
        return url

    if "*" in url:
        matches = glob.glob(url)
        if len(matches) == 1 and os.path.isdir(m := matches[0]):
            return m

    chunks = url.replace(".git", "").split("/")
    if chunks[-1] == "":
        chunks.pop()
    return chunks[-1]


def up(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.keys():
        os.chdir(directory)
        print(directory)
        os.system("git pull")
        os.chdir(home)


def add(args):
    config = _load_cfg(ignore_missing=True)

    if args.url in config:
        print(f"{args.url} already included.")
        return

    directory = _url_to_dir(args.url)

    if directory in config:
        print(f"Directory {directory} already in config")
        return

    if os.path.exists(directory):
        print(f"directory {directory} already exists, not in config.")
    else:
        ret = os.system(f"git clone {args.url}")
        if ret != 0:
            print("Clone failed")
            return

    config[directory] = {"origin": args.url}

    _save_cfg(config)


def _walk(path="."):
    GIT = os.path.sep + ".git"
    TOX = os.path.sep + ".tox"

    for p, d, f in os.walk("."):
        if GIT in p:
            continue
        if TOX in p:
            continue
        yield p, d, f


def _wcgrep(args, prefix="."):
    regex = re.compile(args.expr)

    for p, d, f in _walk():
        for fn in f:
            path = os.path.join(p, fn)
            name = os.path.join(prefix, path.replace("." + os.path.sep, ""))
            try:
                with open(path) as fp:
                    for ln, line in enumerate(fp, start=1):
                        if regex.search(line):
                            if args.list:
                                print(name)
                                break
                            print(name, ":", ln, ": ", line, sep="")
            except UnicodeDecodeError:
                continue


def grep(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.keys():
        os.chdir(directory)
        _wcgrep(args, directory)
        os.chdir(home)


def exe(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.keys():
        print(directory)
        print("=" * len(directory))
        os.chdir(directory)
        subprocess.call(args.commands)
        os.chdir(home)
        print("-" * 60)


def _find(args, prefix="."):
    pat = args.pattern
    if args.case_insensitive:
        pat = pat.casefold()

    if pat in (prefix.casefold() if args.case_insensitive else prefix):
        print(prefix)

    for p, d, f in _walk():
        for fn in d + f:
            path = os.path.join(p, fn)
            name = os.path.join(prefix, path.replace("." + os.path.sep, ""))
            if args.case_insensitive:
                fn = fn.casefold()
            if pat in fn:
                print(name)


def find(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.keys():
        os.chdir(directory)
        _find(args, directory)
        os.chdir(home)


def forget(args):
    config = _load_cfg()
    if not args.like:
        if args.name not in config:
            exit(f"Error: no {args.name} in current repositories. Use --like for substring match.")
        del config[args.name]
        _save_cfg(config)
        return
    matches = [k for k in config.keys() if args.name in k]
    if not matches:
        exit(f"No repositories matched {args.name}")

    for k in matches:
        print(f"Forgetting: {k}")
        del config[k]
    _save_cfg(config)


def reset(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.keys():

        os.chdir(directory)
        res = os.system("git checkout main")
        if res:
            res = os.system("git checkout master")
        if res:
            print(f"ERROR: {directory} checkout failed.")

        os.chdir(home)


def upgrade(args):
    if os.path.abspath(__file__) == os.path.abspath(LOCAL):
        print("Running locally, can't upgrade myself.")
    else:
        _install()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("url")
    exe_parser = subparsers.add_parser("exe")
    exe_parser.add_argument("commands", nargs=argparse.REMAINDER)
    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("pattern")
    find_parser.add_argument("--case-insensitive", "-i", action="store_true")
    forget_parser = subparsers.add_parser("forget")
    forget_parser.add_argument("--like", "-l", action="store_true")
    forget_parser.add_argument("name")
    grep_parser = subparsers.add_parser("grep")
    grep_parser.add_argument("expr")
    grep_parser.add_argument("--list", "-l", action="store_true")
    subparsers.add_parser("up")
    subparsers.add_parser("reset")
    subparsers.add_parser("upgrade")

    args = parser.parse_args()
    start = datetime.datetime.now()
    locals()[args.cmd](args)
    print(
        f"{str(datetime.datetime.now())[:-7]} Finished in {datetime.datetime.now() - start}."
    )
