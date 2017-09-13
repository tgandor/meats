
import os
import sys

try:
    from wmi import WMI
except ImportError:
    print('Missing wmi package')
    os.system('pip install wmi')
    exit()

class_name = sys.argv[1]
c = WMI()

for item in getattr(c, class_name)():
    print(item)
    for prop in item.properties.keys():
        print('{}: {}'.format(prop, getattr(item, prop)))
    print('-' * 60)


