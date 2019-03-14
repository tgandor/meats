#!/usr/bin/env python3

from __future__ import print_function

"""
Script to cut of all mp3 files in a directory by a specified amount of seconds.
"""

import argparse
import glob
import itertools
import multiprocessing
import os

import pydub
import tqdm


def strip_song(song, before_s=0, after_s=0):
    if not (before_s or after_s):
        return song
    end = -int(after_s * 1000) if after_s else None
    stripped = song[int(before_s*1000):end]
    return stripped


def process_filename(name, leading, trailing):
    song = pydub.AudioSegment.from_file(name)
    cut = strip_song(song, leading, trailing)
    cut.export(os.path.join('output', name))
    before = len(song) // 1000
    after = len(cut) // 1000
    return name, before, after


def apply_pf(args):
    """Dumb hack. Partial doesnt need this. Pool.starmap would also do."""
    return process_filename(*args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--leading', '-ss', default=0, help='Leading seconds to cut off', type=float)
    parser.add_argument('--trailing', '-tt', default=0, help='Trailing seconds to cut off', type=float)
    args = parser.parse_args()

    os.makedirs('output', exist_ok=True)

    pool = multiprocessing.Pool()

    files = sorted(glob.glob('*.mp3'))

    # Python is dumb: can't pickle closure
    # and pool.map() should have extra args
    '''
    def map_func(name):
        return process_filename(name, args.leading, args.trailing)

    for name, before, after in tqdm.tqdm(pool.imap_unordered(map_func, files)):
        tqdm.tqdm.write('{name}: file cropped {before} to {after}'.format(**locals()))
    '''

    # fortunately, this does work: (passing a partial to pool)
    import functools
    map_func = functools.partial(process_filename, leading=args.leading, trailing=args.trailing)

    for name, before, after in tqdm.tqdm(pool.imap_unordered(map_func, files), total=len(files)):
        tqdm.tqdm.write('{name}: file cropped {before} to {after}'.format(**locals()))

    # so we don't need to go down this path:
    '''
    for name, before, after in tqdm.tqdm(pool.imap_unordered(apply_pf, zip(files, itertools.repeat(args.leading), itertools.repeat(args.trailing))), total=len(files)):
        tqdm.tqdm.write('{name}: file cropped {before} to {after}'.format(**locals()))
    '''

if __name__ == '__main__':
    main()
