#!/usr/bin/env python

import importlib.metadata


def list_entry_points():
    distributions = importlib.metadata.distributions()
    for dist in distributions:
        if not dist.entry_points:
            continue
        print(f"Package: {dist.metadata['Name']}")
        for entry_point in dist.entry_points:
            print(f"   - {entry_point.name}: {entry_point.value}")


if __name__ == "__main__":
    list_entry_points()
