from __future__ import print_function

import argparse
import datetime
import glob
import os

import pytz
import pywintypes
import win32con
import win32file


def parse_date(date_str):
    try:
        from dateutil import parser
        return parser.parse(date_str)
    except ImportError:
        pass

    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pass

    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def change_file_dates(fname, newtime):
    """https://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file-from-python"""

    wintime = pywintypes.Time(newtime)

    if os.path.isdir(fname):
        winfile = win32file.CreateFile(
           fname,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            # CAUTION: NOT THIS: win32con.FILE_ATTRIBUTE_DIRECTORY,
            # thanks Joel (Rondeau, and Spolsky for SO)
            # https://stackoverflow.com/questions/4998814/createfile-getfiletime-setfiletime
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None,
        )
    elif os.path.isfile(fname):
        winfile = win32file.CreateFile(
           fname,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ
            | win32con.FILE_SHARE_WRITE
            | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None,
        )
    else:
        raise ValueError('Unknown file type: {}'.format(fname))



    win32file.SetFileTime(winfile, wintime, wintime, wintime)
    # None doesn't change, args = file, creation, last access, last write
    # win32file.SetFileTime(None, None, None, None) # does nonething
    winfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('target_glob')
    parser.add_argument('--recursive', '-r', action='store_true', help='Glob recursively, Py3 only.')
    parser.add_argument('--date', '-d', help='Optional datetime.')

    args = parser.parse_args()

    if args.recursive:
        targets = glob.glob(args.target_glob, recursive=True)
    else:
        targets = glob.glob(args.target_glob)

    if args.date:
        touch_date = parse_date(args.date)
    else:
        touch_date = datetime.datetime.now()

    for target in targets:
        if 'System Volume Information' in target:
            print('Not touching:', target)
            continue

        print('Touching:', target)
        change_file_dates(target, touch_date)
