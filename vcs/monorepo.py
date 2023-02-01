#!/usr/bin/env python

import argparse
import json
import os

CONFIG = "monorepo.txt"


def _load_cfg():
    with open(CONFIG) as cfg:
        return json.load(cfg)


def _save_cfg(config):
    with open(CONFIG, "w") as cfg:
        json.dump(config, cfg, indent=2)
        print(file=cfg)


def _url_to_dir(url):
    return url.replace(".git", "").split("/")[-1]


def up(args):
    config = _load_cfg()
    home = os.getcwd()
    for directory in config.values():
        os.chdir(directory)
        print(directory)
        os.system("git pull")
        os.chdir(home)


def add(args):
    if os.path.exists(CONFIG):
        config = _load_cfg()
    else:
        print("Creating new monorepo config.")
        config = {}

    if args.url in config:
        print(f"{args.url} already included.")
        return

    directory = _url_to_dir(args.url)
    if os.path.exists(directory):
        print(f"directory {directory} already exists, not in config.")
        return

    ret = os.system(f"git clone {args.url}")
    if ret != 0:
        print("Clone failed")

    config[args.url] = directory
    _save_cfg(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("url")
    up_parser = subparsers.add_parser("up")

    args = parser.parse_args()

    locals()[args.cmd](args)
