import glob
import os


for f in glob.glob('/usr/bin/i686*'):
    mingw32ver = f.replace('i686-w64-mingw32', 'i586-mingw32msvc')
    if not os.path.exists(mingw32ver):
        print 'ln -s %s %s' % (f, mingw32ver)
        os.link(f, mingw32ver)
