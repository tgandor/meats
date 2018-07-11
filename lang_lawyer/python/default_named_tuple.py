
import typing

class Stats(typing.NamedTuple):
    average: float = 0.0
    stdev: float = 0.0

s = Stats(average=1.0)
print(s)

s = Stats(**{'stdev': 1.0})
print(s)
