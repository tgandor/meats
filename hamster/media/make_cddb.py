#!/usr/bin/env python

"""
Script for generation of cddb entries from text files.

First line in text file is album (disc) title.
Following lines contain the track titles, one per line.
"""

from __future__ import print_function

import argparse
import datetime
import os
import sys

from itertools import count

TEMPLATE = """DISCID={disc_id}
DTITLE={disc_title}
DYEAR={year}
DGENRE=
{tracks}
EXTD=
EXTT0=
EXTT1=
PLAYORDER=
"""

TRACK_TEMPLATE = "TTITLE{id}={title}"


def main():
    """
    Main function.
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--discid', help='Use specific disc-id, not computed')
    parser.add_argument('titles', type=file, help='File to read titles from')
    args = parser.parse_args(sys.argv[1:])

    disc_id = args.discid or os.popen('cd-discid').read().split()[0]

    titles = args.titles.readlines()

    tracks = '\n'.join(
        TRACK_TEMPLATE.format(id=i, title=title.strip().replace('/', '-'))
        for i, title in zip(count(0), titles[1:])
    )

    cddb_entry = TEMPLATE.format(
        year=datetime.date.today().year,
        disc_title=titles[0].strip(),
        tracks=tracks,
        disc_id=disc_id
    )

    print(cddb_entry)

    cddb_dir = os.path.expanduser('~/.cddb/user')
    if not os.path.isdir(cddb_dir):
        os.makedirs(cddb_dir)
    with open(os.path.join(cddb_dir, disc_id), 'w') as out:
        out.write(cddb_entry)

if __name__ == '__main__':
    main()
