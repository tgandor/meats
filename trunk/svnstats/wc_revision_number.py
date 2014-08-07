#!/usr/bin/env python

import os
import sys

def get_current_revision(wc_root):
    entries_file = os.path.join(wc_root, '.svn', 'entries')
    if os.path.exists(entries_file):
        # pre 1.7 format
        return list(open(entries_file))[3].strip()
    wcdb_file = os.path.join(wc_root, '.svn', 'wc.db')

def main():
    if len(sys.argv) < 2:
        print get_current_revision('.')
    elif len(sys.argv) == 2:
        print get_current_revision(sys.argv[1])
    elif len(sys.argv) == 4:
        version = get_current_revision(sys.argv[1])
        template = open(sys.argv[2]).read()
        open(sys.argv[3], 'w').write(template.replace('$WCREV$', version))

if __name__ == '__main__':
    main()
