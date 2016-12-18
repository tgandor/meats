#!/usr/bin/env python

import glob
import os

fields_of_interest = ['POWER_SUPPLY_ENERGY_FULL', 'POWER_SUPPLY_ENERGY_NOW', None, None, None, 'POWER_SUPPLY_POWER_NOW']


def power_supply_data():
    batteries = glob.glob('/sys/class/power_supply/BAT?/uevent')
    if not batteries:
        print('Batteries not found.')
        exit(1)
    raw = open(batteries[0]).read()
    result = {}
    for line in raw.split('\n'):
        parts = line.split('=')
        if len(parts) == 2:
            result[parts[0]] = parts[1]
    return result


def format_fields_of_interest(data):
    return '\t'.join(data[field] if field is not None else '' for field in fields_of_interest)


def main():
    data = power_supply_data()
    print format_fields_of_interest(data)


if __name__ == '__main__':
    main()
