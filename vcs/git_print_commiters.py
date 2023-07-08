#!/usr/bin/env python

from git import Repo


def print_commiters(repo_path):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits())

    committers = set()

    for commit in commits:
        committer = commit.committer
        committers.add(committer.name)

    for committer in committers:
        print(committer)


repo_path = "."

print_commiters(repo_path)
