#!/bin/bash

import argparse
import os

def or_die(command):
    print(command)
    result = os.system(command)
    if result != 0:
        print(f"{command} failed with code: {result}")
        exit(result)


parser = argparse.ArgumentParser()
parser.add_argument("--message", "-m", default="This repository has been retired.")
args = parser.parse_args()

or_die("git rm -r *")
with open("README.md", "w") as readme:
    readme.write(f"""# Empty Repository
    {args.message}
""")
or_die("git add README.md")
or_die(f'git commit -m "{args.message}"')
