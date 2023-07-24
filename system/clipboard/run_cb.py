#!/usr/bin/env python

import argparse
import queue
import subprocess
import threading
import time

from pyperclip import paste


class Runner:
    def __init__(self, verbose) -> None:
        self.verbose = verbose
    def run(self, command):
        if self.verbose:
            print(command)
        subprocess.call(command)
        if self.verbose:
            print("done.")


class AsyncRunner(Runner):
    def __init__(self, verbose) -> None:
        super().__init__(verbose)
        self.queue = queue.Queue()
        self.worker = threading.Thread(target=self._worker, daemon=True)
        self.worker.start()

    def run(self, command):
        self.queue.put(command)
        if self.verbose:
            print(command, "(queued)")

    def _worker(self):
        while True:
            command = self.queue.get()
            try:
                super().run(command)
            except FileNotFoundError as e:
                print("Warning, run failed:", e)


MARKER = "{}"

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--single-word", "-S", action="store_true")
parser.add_argument("--queue", "-q", action="store_true", help="use async queue")
parser.add_argument("args", nargs=argparse.REMAINDER)
opts = parser.parse_args()

args = opts.args
runner = (AsyncRunner if opts.queue else Runner)(opts.verbose)

if not any(MARKER in arg for arg in args):
    args.append(MARKER)

old = paste()

while True:
    time.sleep(0.1)
    new = paste()
    if new != old:
        old = new

        if opts.single_word and len(new.split()) > 1:
            print("Skipping:", new)
            continue

        command = [arg.replace(MARKER, new) for arg in args]
        runner.run(command)
