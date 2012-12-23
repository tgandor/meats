#!/usr/bin/env python

import zipfile
import sys
import os
import errno
import codecs

flags = {
        '-v': False,
        '-l': False,
        '-q': False,
}

options = {
        '-e': 'cp1250',
        '-d': '.',
}

def parseopts():
    args = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in flags.keys():
            flags[sys.argv[i]] = True
            i += 1
        elif sys.argv[i] in options.keys():
            options[sys.argv[i]] = sys.argv[i+1]
            i += 2
        else:
            args.append(sys.argv[i])
            i += 1
    return args

def _filename(fileinfo):
    return fileinfo.filename.decode(options['-e'])

def _print_short(fi):
    print "%9d  %d-%02d-%02d %02d:%02d   %s" % (
            (fi.file_size,) + fi.date_time[:-1] + (_filename(fi),)
    )

def _full_info(fileinfo):
    print _filename(fileinfo)
    for f in dir(fileinfo):
        if not f.startswith('__'):
            print f, getattr(fileinfo, f)
    print '-'*40

def _extract(fi, z):
    name = _filename(fi)
    if name.startswith('/') or name.startswith('../') or name.find('/../') != -1:
        print >>sys.stderr, "Malicious path found: %s, not extracting." % name
        return
    if options['-d'] != '.':
        name = os.path.join(options['-d'], name)
    dirname = os.path.dirname(name)
    if dirname != '' and not os.path.exists(dirname):
        os.makedirs(dirname)
    basename = os.path.basename(name)
    if basename != '':
        data = z.read(fi)
        open(name, 'wb').write(data)
        if not flags['-q'] and fi.compress_type:
            print "%11s: %s" % ('inflating', name)
        elif not flags['-q']:
            print "%11s: %s" % ('extracting', name)
    elif not flags['-q']:
        print "%11s: %s" % ('creating', name)

def process_single(fileinfo, zipfile):
    if flags['-l']:
        _print_short(fileinfo)
    elif flags['-v']:
        _full_info(fileinfo)
    else:
        _extract(fileinfo, zipfile)

def process(z, files):
    total, num = 0, 0
    for i in z.infolist():
        if len(files)==0 or any(_filename(i).endswith(x) for x in files):
            total += i.file_size
            num += 1
            process_single(i, z)
    _footer(total, num)

def _footer(total, num):
    if flags['-l']:
        print """---------                     %s------
%9d                     %d files""" % ('-'*len(str(num)), total, num)

def _header(arg):
    print "Archive:  %s" % arg
    if flags['-l']:
        print """ Length      Date    Time    Name
---------  ---------- -----   ----"""

def main():
    args = parseopts()
    _header(args[0])
    z = zipfile.ZipFile(args[0])
    process(z, map(unicode, args[1:]))

if __name__=='__main__':
    main()
