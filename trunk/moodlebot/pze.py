#!/usr/bin/env python

"""A module with some Moodle access automatic utilities."""

class MoodleBot(object):
    """A plain HTTP[s] moodle pages fetcher."""
    
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
            print "Missing config file pze.ini"
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
        print self.url(url)
        return self.opener.open(self.url(url)).read()

    def download(self, url):
        """Fetch resource and save into a file."""
        from os.path import split
        out_filename = ''.join((c if not c in '?/\\()&' else '_') for c in split(url)[-1])
        open(out_filename, 'w').write(self.fetch(url))

def get_mails(url):
    """Retrieve user E-mails from a page (eg. grader report)."""
    from HTMLParser import HTMLParser as HP
    from urllib import unquote
    from re import findall
    get = bot.fetch
    unesc = HP().unescape
    retr = lambda url: unesc(get(url).decode('utf-8'))
    user_links = sorted(set(findall('user/view[^"]+', retr(url))))
    user_pages = [retr(l) for l in user_links]
    emails = findall('>([\w\.]+@[\w\.]+)<', "".join(user_pages))
    assert len(emails)==len(user_links)
    print "; ".join(emails)
    return zip(user_links, emails)

def help():
    import types
    print """
    Usage: %s <function> [arguments] 
    """ % sys.argv[0]
    print "Available functions are:"
    g = globals() 
    for f in g: 
        if type(g[f])==types.FunctionType:
            print f

def dload(*args):
    """Download global function."""
    map(MoodleBot().download, args)

def fetch(arg):
    print MoodleBot().fetch(arg)
    
if __name__=='__main__':
    import sys
    try:
        # commandline calling of functions
        args = sys.argv[2:]
        globals()[sys.argv[1]](*args)
    except:
        help()
