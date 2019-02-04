#!/usr/bin/env python

from itertools import groupby
from operator import itemgetter
from xml.dom import minidom
import sys

def configs(doc, name='AdditionalDependencies'):
    for el in  doc.getElementsByTagName('ItemDefinitionGroup'):
        condition = el.attributes['Condition'].value
        for libs in el.getElementsByTagName(name):
            result = libs.firstChild.nodeValue
            yield (result, condition)

def group_report(doc, element='AdditionalDependencies'):
    gn = 0
    print "=" * 60
    print "Grouping by", element
    print "=" * 60
    for k, g in groupby(sorted(configs(doc, element), key=itemgetter(0)), key=itemgetter(0)):
        gn += 1
        print "Group", gn, "\n" + "-" * 40
        cn = 0
        for cond in g:
            cn += 1
            print "%2d %s" % (cn, cond[1])
        print "Value:"
        print k
        print "-"*40
    print "End of grouping by", element
    print "=" * 60, "\n"

if __name__ == '__main__':
    doc = minidom.parse(sys.argv[1])
    group_report(doc, 'AdditionalDependencies')
    group_report(doc, 'AdditionalLibraryDirectories')
    group_report(doc, 'AdditionalIncludeDirectories')
