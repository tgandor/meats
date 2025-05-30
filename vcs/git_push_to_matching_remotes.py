#!/usr/bin/env python

import subprocess


def get_current_branch():
    result = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True
    )
    return result.stdout.strip()


def get_remotes():
    result = subprocess.run(["git", "remote"], capture_output=True, text=True)
    return result.stdout.split()


def remote_has_branch(remote, branch):
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", remote, branch],
        capture_output=True,
    )
    return result.returncode == 0


def push_to_remote(remote, branch):
    subprocess.run(["git", "push", remote, branch])


def main():
    branch = get_current_branch()
    remotes = get_remotes()

    for remote in remotes:
        if remote_has_branch(remote, branch):
            print(f"Pushing to {remote}/{branch}")
            push_to_remote(remote, branch)
        else:
            print(f"Skipping {remote} — branch '{branch}' not found")


if __name__ == "__main__":
    main()
