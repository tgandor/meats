#!/usr/bin/env python

import argparse
import json
import os
import shutil
import stat

CONFIG = "monorepo.json"
LOCAL = "mr.py"


def _load_cfg(ignore_missing=False):
    if os.path.exists(CONFIG):
        with open(CONFIG) as cfg:
            return json.load(cfg)
    if ignore_missing:
        print("Creating new monorepo config.")
        if not os.path.exists(LOCAL):
            shutil.copyfile(__file__, LOCAL)
            mode = os.stat(LOCAL).st_mode
            os.chmod(LOCAL, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"Local copy of script {LOCAL} created.")
        return {}


def _save_cfg(config):
    with open(CONFIG, "w") as cfg:
        json.dump(config, cfg, indent=2)
        print(file=cfg)


def _url_to_dir(url):
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
    if os.path.exists(directory):
        print(f"directory {directory} already exists, not in config.")
    else:
        ret = os.system(f"git clone {args.url}")
        if ret != 0:
            print("Clone failed")
        return

    config[directory] = {"origin": args.url}

    _save_cfg(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("url")
    up_parser = subparsers.add_parser("up")

    args = parser.parse_args()

    locals()[args.cmd](args)
