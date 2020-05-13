#!/usr/bin/env python

'''
There are many EPUB libraries... But first I tried my own class.
'''

import zipfile
import xml.etree as ET


def find_files(suffix, root='.'):
    import os

    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith(suffix):
                yield os.path.join(path, f)


class Epub(zipfile.ZipFile):
    def open_container(self):
        return self.open('META-INF/container.xml')

    @property
    def container(self):
        with self.open_container() as c:
            return c.read().decode()

    @property
    def container_et(self):
        with self.open_container() as c:
            return ET.parse(c)

    @property
    def rootfile_et(self):
        return self.container_et.find('.//container:rootfile', {'container': 'urn:oasis:names:tc:opendocument:xmlns:container'})

    @property
    def rootfile_path(self):
        return self.rootfile_et.attrib['full-path']

    @property
    def rootfile(self):
        return self.read(self.rootfile_path)

    def read(self, file_path):
        with self.open(file_path) as rf:
            return rf.read().decode()

    def find_files(self, pred):
        for info in self.filelist:
            if pred(info):
                yield info.filename


if __name__ == '__main__':
    for book in find_files('.epub'):
        print(book)
        epub = Epub(book)
        for css in epub.find_files(lambda i: i.filename.endswith('.css')):
            print(css)
            print(epub.read(css))
        print('-' * 60)
