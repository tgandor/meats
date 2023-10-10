import json
from collections import defaultdict

# works just fine:
dd = defaultdict(list)
dd["x"].append(1)
print(json.dumps(dd))
