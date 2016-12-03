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
        # 'cp949, cp891' Windows Korean
        #'-e': 'cp1250', # Windows ANSI CE
        '-e': 'cp852', # Windows console CE
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


def _sanitize(s):
    """Replace 'bad' characters in string with underscore."""
    return ''.join(map(lambda c: c if 31 < ord(c) < 128 else '_', s))


def _filename2(fileinfo):
    if (fileinfo.flag_bits & 0x800):
        # unicode
        return fileinfo.filename
    try:
        return fileinfo.filename.decode(options['-e'])
    except UnicodeDecodeError:
        gelded = _sanitize(fileinfo.filename)
        sys.stderr.write('Error decoding {}, using {} instead\n'.format(repr(fileinfo.filename), gelded))
        return gelded


def _filename3(fileinfo):
    # print(fileinfo.filename, fileinfo.flag_bits)
    if (fileinfo.flag_bits & 0x800):
        # unicode
        return fileinfo.filename
    try:
        # https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
        filename_bin = fileinfo.filename.encode('cp437')
        # print(repr(fileinfo.filename), ' -> ', filename_bin)
        filename_str = filename_bin.decode(options['-e'])
        # print(filename_bin, ' -> ', filename_str, fileinfo.flag_bits)
        return filename_str
    except UnicodeDecodeError:
        gelded = _sanitize(fileinfo.filename)
        sys.stderr.write('Error decoding {}, using {} instead\n'.format(repr(fileinfo.filename), gelded))
        return gelded


if sys.version_info.major == 2:
    _filename = _filename2
else:
    _filename = _filename3


def _print_short(fi):
    try:
        print("%9d  %d-%02d-%02d %02d:%02d   %s" % (
            (fi.file_size,) + fi.date_time[:-1] + (_filename(fi),)
        ))
    except:
        print("%9d  %d-%02d-%02d %02d:%02d   %s(ERR)" % (
            (fi.file_size,) + fi.date_time[:-1] + (fi.filename,)
        ))

def _full_info(fileinfo):
    print(_filename(fileinfo))
    for f in dir(fileinfo):
        if not f.startswith('__'):
            print(f, getattr(fileinfo, f))
    print('-'*40)

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
            try:
                print("%11s: %s" % ('inflating', name))
            except:
                print("%11s: %s(ERR)" % ('inflating', fi.filename))
        elif not flags['-q']:
            try:
                print("%11s: %s" % ('extracting', name))
            except:
                print("%11s: %s(ERR)" % ('extracting', name))
    elif not flags['-q']:
        print("%11s: %s" % ('creating', name))

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
        print("""---------                     %s------
%9d                     %d files""" % ('-'*len(str(num)), total, num))

def _header(arg):
    print("Archive:  %s" % arg)
    if flags['-l']:
        print(""" Length      Date    Time    Name
---------  ---------- -----   ----""")

def main():
    args = parseopts()
    _header(args[0])
    z = zipfile.ZipFile(args[0])
    process(z, list(map(str, args[1:])))

if __name__=='__main__':
    main()
