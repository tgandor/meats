#!/usr/bin/env python

import luddite

requirements = []

with open("requirements.txt", "r") as fp:
    for line in fp.readlines():
        package, current = line.strip().split("==")
        try:
            latest_version = luddite.get_versions_pypi(package)[-1]
            requirements.append(f"{package}=={latest_version}")
            if current != latest_version:
                print(f"{package}: {current} -> {latest_version}")
        except:
            print(f"Failed to get version for {package}")
            requirements.append(line.strip())

with open("requirements.txt", "w") as fp:
    for req in requirements:
        fp.write(f"{req}\n")
