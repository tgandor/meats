#!/usr/bin/env python

import os

import requests
import six.moves
import bs4

style = """
<style>
table {
  border-collapse: collapse;
}
table, th, td {
  border: 1px solid black;
}
td {
  text-align: center;
}
.zwin, .rozwin {
  display: none;
}
</style>
"""

print('Insert link(s) to route timetable:')

trip_id = 1

while True:
    url = six.moves.input()
    if not url:
        break

    data = requests.get(url).content
    html = bs4.BeautifulSoup(data)

    table = html.body.find('table')

    output = 'trip_{}.html'.format(trip_id)
    with open(output, 'w') as f:
        f.write(style)
        f.write(str(table))

    if hasattr(os, 'startfile'):
        os.startfile(output)
    else:
        os.system('xdg-open ' + output)

    trip_id += 1
