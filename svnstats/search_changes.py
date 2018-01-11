#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse


def arguments():
    parser = argparse.ArgumentParser(description="Search through file's or directory's SVN history: logs and diffs")
    parser.add_argument('-b', '--branch', action='store_true', help='Stay on current branch')
    parser.add_argument('--diff', type=str, help='Search phrase in diff')
    parser.add_argument('--new', action='store_true', help='Show only added lines in diff')
    parser.add_argument('--log', type=str, help='Search phrase in log')
    parser.add_argument('path', type=str, help='file or directory to consider')
    return parser.parse_args()


def revisions_for_path(path, stay_on_branch=False):
    rev = re.compile('^r(\d+)', re.MULTILINE)
    stop_option = '--stop-on-copy' if stay_on_branch else ''
    command = 'svn log -q %s %s' % (stop_option, path)
    log = os.popen(command).read()
    return rev.findall(log)
    

def list_summary(list_, sample_size=2):
    if len(list_) <= 2 * sample_size:
        return repr(list_)
    head = repr(list_[:sample_size])
    tail = repr(list_[-sample_size:])
    return head[:-1] + ', ..., ' + tail[1:]
    

def revision_diff(path, revision):
    command = 'svn diff -c %s %s' % (revision, path)
    return os.popen(command).read()


def revision_log(revision):
    command = 'svn log -r %s' % (revision,)
    return os.popen(command).read()

    
def report_diff(diff, args):
    if not args.diff:
        return
    diff_lines = diff.split('\n')
    for line in diff_lines:
        if args.diff in line and (not args.new or line.startswith('+')):
            print(line)

            
def main():
    args = arguments()
    revisions = revisions_for_path(args.path, args.branch)
    print(len(revisions), 'revisions to check', list_summary(revisions))
    for revision in revisions:
        diff_ok, log_ok = True, True
        diff = revision_diff(args.path, revision)
        log = revision_log(revision)
        if args.log and log.find(args.log) == -1:
            log_ok = False
        if args.diff and diff.find(args.diff) == -1:
            diff_ok = False
        if log_ok and diff_ok:
            print(revision)
            print('-' * len(str(revision)))
            report_diff(diff, args)
            if args.log:
                print(log)
            print()


if __name__ == '__main__':  
    main()
