#!/usr/bin/env python

import re
import sys
import glob
import shutil
import datetime
import threading

IMAGE_GLOB = '*.[Jj][Pp][Gg]'
FILE_TEMPLATE = 'img_%03d.jpg'

# commandline history
try:
    import readline
    import os
    import atexit

    histfile = os.path.expanduser("~/.pic_group")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
except ImportError:
    print >>sys.stderr, 'Readline not available'
    pass


def ucfirst(str_):
    return str_[0].upper() + str_[1:]


def guess_date(date_str):
    parts = date_str.split()
    if len(parts) == 3:
        year = int(parts[0])
        if year < 100:
            year += 2000
        return datetime.date(year, int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        return datetime.date.today().replace(month=int(parts[0]), day=int(parts[1]))
    if len(parts) == 0:
        return datetime.date.today()
    day = int(date_str)
    if (day < 0):
        return datetime.date.fromordinal(datetime.date.today().toordinal() + day)
    return datetime.date.today().replace(day=day)


def make_description(description):
    return ucfirst('-'.join(description.split()))


def move_images(dirname):
    images = glob.glob(IMAGE_GLOB)
    print sorted(images), len(images)
    if os.path.exists(dirname):
        print 'Directory already exists'
        return
    os.mkdir(dirname)
    for img in images:
        shutil.move(img, dirname)


def process(cmd):
    if not cmd.strip():
        return
    if (cmd.find(',') == -1):
        date = datetime.date.today()
        description = cmd
    else:
        parts = cmd.split(',')
        date = guess_date(parts[0])
        description = parts[1]
    if not description.strip():
        return
    dirname = date.isoformat() + '-' + make_description(description)
    print dirname
    move_images(dirname)


class IntervalTimer(threading.Thread):
    def __init__(self, interval, target):
        threading.Thread.__init__(self)
        self.interval = interval
        self.target = target
        self.stopped = threading.Event()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.target()

    def stop(self):
        self.stopped.set()


def rename(filename, index=1):
    while True:
        new_filename = FILE_TEMPLATE % index
        if not os.path.exists(new_filename):
            break
        index += 1
    shutil.move(filename, new_filename)
    return new_filename, index


def autorename():
    images = glob.glob(IMAGE_GLOB)
    last_index = 1
    for img in images:
        if not re.match('[a-z0-9_]+\\.[a-z]{3}$', img, re.I):
            _, last_index = rename(img, last_index)


t = IntervalTimer(1.0, autorename)
t.start()

while True:
    try:
        cmd = raw_input('(pic)> ')
    except EOFError:
        break
    if cmd.lower() == 'q':
        break
    process(cmd)

t.stop()
t.join()
print 'Bye'
