#!/usr/bin/env python

def main():
    import re
    import sys
    unselfclosed = re.compile('<(img|input|hr|br) [^>]+[^/]>|<br>|<hr>')
    def repl(match):
        orig = match.group()
        print '   ', orig
        if orig[-2] == ' ':
            return orig[:-1] + '/>'
        return orig[:-1] + ' />'
    for f in sys.argv[1:]:
        print "--- Processing: %s ---" % f
        body = open(f).read()
        body, changes = unselfclosed.subn(repl, body)
        print "... %d changes ..." % changes
        if changes > 0:
            open(f, 'w').write(body)

if __name__=='__main__':
    main()
