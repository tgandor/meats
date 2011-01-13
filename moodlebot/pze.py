#!/usr/bin/env python
import sys

"""A module with some Moodle access automatic utilities."""

class MoodleBot(object):
    """A plain HTTP[s] moodle pages fetcher."""
    
    @classmethod
    def mockbot(cls):
        """Forcing the bot to fetch test.html and not login."""
        cls.__init__ = lambda self: None
        cls.fetch = lambda self, arg: open('test.html').read()

    def __init__(self):
        """Workaround for fake singleton recipe: don't construct again."""
        if '_inst' in vars(self.__class__):
            self.__dict__ = self.__class__._inst.__dict__
            return
        import ConfigParser
        import os
        from urllib2 import build_opener, HTTPCookieProcessor
        conf = ConfigParser.RawConfigParser()
        if not os.path.exists('pze.ini'):
            import getpass
            print >>sys.stderr, "Missing config file pze.ini"
            url_base = raw_input('Enter base URL: ')
            username = raw_input('Enter username: ')
            password = getpass.getpass()
            conf.add_section('pze')
            conf.set('pze', 'url_base', url_base)
            conf.set('pze', 'username', username)
            conf.set('pze', 'password', password)
            conf.write(open('pze.ini', 'w'))
        conf.read('pze.ini')
        self.url_base = conf.get('pze', 'url_base')
        self.opener = build_opener(HTTPCookieProcessor())
        # establish session
        self.fetch('/login/index.php')
        credentials = dict([
                    ('username', conf.get('pze', 'username')),
                    ('password', conf.get('pze', 'password')),
                    ('testcookies', '1')
                    ])
        # send actual login
        self.post('/login/index.php', credentials)
        self.__class__._inst = self

    def url(self, url):
        """Optionally stick the current url_base before the url."""
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return self.url_base + url
        return self.url_base + '/' + url
    
    def post(self, url, data):
        """Send post data to specific url."""
        if isinstance(data, dict):
            from urllib import urlencode
            data = urlencode(data)
        return self.opener.open(self.url(url), data).read()
            
    def fetch(self, url):
        """Read a single page from the system (relative). Low  level."""
        print >>sys.stderr, self.url(url)
        return self.opener.open(self.url(url)).read()

    def download(self, url):
        """Fetch resource and save into a file."""
        from os.path import split
        out_filename = ''.join((c if not c in '?/\\()&' else '_')
                               for c in split(url)[-1])
        open(out_filename, 'w').write(self.fetch(url))

    def prep_rows_arg(self, arg):
        """Handle filename (read lines) or stdin if arg is None."""
        if arg is None:
            rows = sys.stdin.readlines()
            arg = 'stdin'
        else:
            rows = open(arg).readlines()
        return rows, arg
        
    def memo_load_urls(self, arg):
        """Retrieve fragments of pages (regexp matches) as specified in file."""
        import re
        rows, _ = self.prep_rows_arg(arg)
        return dict([
            (l, re.findall(l.split()[1], self.fetch(l.split()[0])))
            for l in rows])

    def memo_store_dict(self, arg):
        """Create a file with current matches (pickled dict)."""
        import cPickle
        cPickle.dump(self.memo_load_urls(arg),
            open(self.prep_rows_arg(arg)[1]+'.last.p', 'wb'))

    def memo_load_dict(self, arg):
        """Retrieve the stored dictionary, see memo_store_dict."""
        import cPickle
        arg = arg or 'stdin'
        try:
            return cPickle.load(open(arg+'.last.p'))
        except IOError:
            print >>sys.stderr, "Missing state file - run %s memorize %s" % (
                sys.argv[0], arg)
            raise

    def memo_check_update(self, arg):
        """Load both old and new versions, return the new matches."""
        current = MoodleBot().memo_load_urls(arg)
        last = MoodleBot().memo_load_dict(arg)
        return list(set.union(*[set(current[r])-set(last[r]) for r in current]))
        
def get_mails(url):
    """Retrieve user E-mails from a page (eg. grader report)."""
    from HTMLParser import HTMLParser as HP
    from urllib import unquote
    from re import findall
    get = MoodleBot().fetch
    unesc = HP().unescape
    retr = lambda url: unesc(get(url).decode('utf-8'))
    user_links = sorted(set(findall('user/view[^"]+', retr(url))))
    user_pages = [retr(l) for l in user_links]
    emails = findall('>([\w\.]+@[\w\.]+)<', "".join(user_pages))
    assert len(emails)==len(user_links)
    print "; ".join(emails)
    return zip(user_links, emails)

# Careful with from ... import *, when interactive: shadows help
def help():
    """Print usage information and list global functions."""
    import types
    print """
    Usage: %s <function> [arguments] 
    """ % sys.argv[0]
    print "Available functions are:"
    g = globals() 
    for f in g: 
        if type(g[f])==types.FunctionType:
            print "%-20s %s" % (f, g[f].__doc__)

def dload(*args):
    """Download global function."""
    if args == ['-']:
        args = sys.stdin.read().split()
    map(MoodleBot().download, args)

def fetch(arg):
    """Retreive URL and print to stdout. With newline."""
    print MoodleBot().fetch(arg)

def watch(arg=None):
    """Read urls and regexps from file (argument), watch for changes."""
    news = MoodleBot().memo_check_update(arg)
    if news:
        print "\n".join(map(MoodleBot().url, news))

def watch_dload(arg=None):
    """Read urls and regexps from file (argument), watch for changes."""
    news = MoodleBot().memo_check_update(arg)
    if news:
        map(MoodleBot().download, news)
    else:
        print >>sys.stderr, 'Nothing to download'

def memorize(arg=None):
    """Store the matches in a pickled dictionary in a file, see watch."""
    MoodleBot().memo_store_dict(arg)

def qtgui_watch(arg):
    """Gui (system tray) version of watch."""
    # next 2 lines blindly follow examples...
    import sip
    sip.setapi('QVariant', 2)
    from PyQt4 import QtCore, QtGui
    import threading

    class CheckerThread(QtCore.QThread):
        def __init__(self, parent=None):
            super(CheckerThread, self).__init__(parent)
            # actual variables
            self.lastNews = []
            self.cancelled = False
            self.window = parent
            self.working = False
            
        def light_sleep(self, secs):
            """Sleep shallowly to wake every second."""
            for i in xrange(secs):
                self.sleep(1)
                if self.cancelled:
                    break
                            
        def run(self):
            if self.window:
                while not self.cancelled:
                    print >>sys.stderr, 'Running the checks...'
                    self.working = True
                    self.window.trayIcon.setToolTip('MoodleBot retrieves!')
                    news = MoodleBot().memo_check_update(arg)
                    self.window.trayIcon.setToolTip('MoodleBot watches...')
                    self.working = False
                    if news:
                        self.lastNews = news
                        self.light_sleep(600)
                    else:
                        self.light_sleep(6)
                
    class Window(QtGui.QDialog):
        def __init__(self):
            super(Window, self).__init__()
            # PyQt4 stuff
            trayIconMenu = QtGui.QMenu(self)
            trayIconMenu.addAction(
                QtGui.QAction("&Quit", self, triggered=self.cancel))
            trayIcon = QtGui.QSystemTrayIcon(self)
            trayIcon.setContextMenu(trayIconMenu)
            trayIconIcon = QtGui.QIcon('moobo.svg')
            trayIcon.setIcon(trayIconIcon)
            trayIcon.setToolTip('MoodleBot is watching...')
            trayIcon.show()
            self.trayIcon = trayIcon
            thread = CheckerThread(self)
            thread.start()
            self.thread = thread
            timer = QtCore.QTimer()
            timer.singleShot(5000, self.checks)
            self.timer = timer

        def checks(self):
            if self.thread.lastNews:
                self.trayIcon.showMessage(
                    'News found!', "\n".join(self.thread.lastNews), msecs=60000)
                self.timer.singleShot(120000, self.checks)
            else:
                self.timer.singleShot(5000, self.checks)
            
        def cancel(self):
            """Stop operation. Still hangs when thread checks."""
            self.thread.cancelled = True
            self.thread.wait()
            QtGui.qApp.quit()
            
    app = QtGui.QApplication(sys.argv)
    
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
        
    window = Window()
    sys.exit(app.exec_())

if __name__=='__main__':
    try:
        # commandline calling of functions
        args = sys.argv[2:]
        globals()[sys.argv[1]](*args)
    except IndexError:
        help()
