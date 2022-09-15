#!/usr/bin/env python

# https://docs.python.org/3/library/enum.html#using-automatic-values

from enum import Enum, auto
import logging


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class Ordinal(AutoName):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

print(f"{list(Ordinal)=}")

print(f"{('EAST' in Ordinal.__members__)=}")
print(f"{('NNW' in Ordinal.__members__)=}")
print(f"{(Ordinal.__members__)=}")

print(f"{Ordinal('NORTH')=}")
print(f"{Ordinal('SOUTH').name=}")
print(f"{Ordinal('SOUTH').value=}")

try:
    Ordinal('NNW')
except ValueError:
    logging.exception("This throws:")
    # ValueError: 'NNW' is not a valid Ordinal
