import codecs
import datetime
import os
import json

with open(os.path.join(os.path.dirname(__file__), "ff_versions.json")) as js:
    versions = json.load(js)

for ver in versions:
    y, m, d = [int(x) for x in ver["release_date"].split("-")]
    num = float(ver["version"])
    my_num = (y - 2025) * 12 + m + 134
    print(ver, my_num, my_num-num, "OK" if num == my_num else "no")

td = datetime.date.today()
my_num = (td.year - 2025) * 12 + td.month + 133
user_agent = codecs.encode("Zbmvyyn/5.0 (K11; Yvahk k86_64; ei:{}.0) Trpxb/20100101 Sversbk/{}.0".format(my_num, my_num), "rot_13")
print(user_agent)
