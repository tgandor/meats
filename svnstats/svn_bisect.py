import argparse
import os
import re
import logging


def arguments():
    parser = argparse.ArgumentParser(description="Search through file's or directory's SVN history: logs and diffs")
    parser.add_argument('--limit', '-l', type=int, help='Script to execute to check if correct revision', default=100)
    parser.add_argument('-b', '--branch', action='store_true', help='Stay on current branch')
    parser.add_argument('--log', type=str, help='Path to log file')
    parser.add_argument('script', type=str, help='Script to execute to check if correct revision')
    parser.add_argument('path', type=str, help='file or directory to consider', nargs='?', default='')
    return parser.parse_args()


def revisions_for_path(path, stay_on_branch=False, limit=0):
    rev = re.compile('^r(\d+)', re.MULTILINE)
    stop_option = '--stop-on-copy' if stay_on_branch else ''
    limit_option = '-l {}'.format(limit) if limit > 0 else ''
    print('Reading revisions...')
    command = 'svn log -q {} {} {}'.format(stop_option, path, limit_option)
    log = os.popen(command).read()
    return rev.findall(log)


def list_summary(list_, sample_size=2):
    if len(list_) <= 2 * sample_size:
        return repr(list_)
    head = repr(list_[:sample_size])
    tail = repr(list_[-sample_size:])
    return head[:-1] + ', ..., ' + tail[1:]


def main():
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    args = arguments()
    if args.log:
        file_handler = logging.FileHandler(args.log)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    revisions = revisions_for_path(args.path, args.branch, args.limit)
    logger.debug('%d revisions to check: %s', len(revisions), list_summary(revisions))
    for revision in revisions:
        logger.debug(revision)
        res = os.system(args.script)
        logger.debug('Result for %s : %s', revision, res)


if __name__ == '__main__':
    main()

