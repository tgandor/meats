#!/usr/bin/env python

import os
import subprocess
from collections import defaultdict

SNAPS_DIR = "/var/lib/snapd/snaps"


def run(cmd):
    return subprocess.check_output(cmd, text=True).splitlines()


def get_snap_sizes():
    """Zwraca dict: nazwa_snap -> rozmiar w MB (float)."""
    sizes = {}
    if not os.path.isdir(SNAPS_DIR):
        return sizes

    for fname in os.listdir(SNAPS_DIR):
        if not fname.endswith(".snap"):
            continue
        path = os.path.join(SNAPS_DIR, fname)
        try:
            st = os.stat(path)
        except FileNotFoundError:
            continue

        # nazwa snapa to część przed _revision.snap
        base = fname.rsplit(".snap", 1)[0]
        name = base.split("_", 1)[0]
        mb = st.st_size / (1024 * 1024)
        # bierzemy największy rozmiar (ostatnia rewizja zwykle największa)
        sizes[name] = max(mb, sizes.get(name, 0))
    return sizes


def get_installed_snaps():
    """Zwraca listę nazw z `snap list`."""
    lines = run(["snap", "list"])
    snaps = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            snaps.append(parts[0])
    return snaps


def parse_connections():
    """
    Buduje graf zależności:
    dep_graph[A] = {B, C, ...}  -> A zależy od B, C...
    """
    dep_graph = defaultdict(set)

    snaps = get_installed_snaps()
    for snap in snaps:
        try:
            lines = run(["snap", "connections", snap])
        except subprocess.CalledProcessError:
            continue

        # Format: Interface  Plug  Slot  Notes
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 3:
                continue
            plug = parts[1]
            slot = parts[2]

            # plug:  snapname:plugname  lub -
            # slot:  snapname:slotname  lub -
            if ":" in plug:
                plug_snap = plug.split(":", 1)[0]
            else:
                plug_snap = None

            if ":" in slot:
                slot_snap = slot.split(":", 1)[0]
            else:
                slot_snap = None

            # jeśli plug_snap zależy od slot_snap
            if plug_snap and slot_snap and plug_snap != slot_snap:
                dep_graph[plug_snap].add(slot_snap)

    # upewnij się, że wszystkie snapy są w grafie
    for s in snaps:
        dep_graph.setdefault(s, set())

    return dep_graph


def invert_graph(dep_graph):
    """Buduje odwrotny graf: kto zależy od kogo."""
    rev = defaultdict(set)
    for a, deps in dep_graph.items():
        for b in deps:
            rev[b].add(a)
    # upewnij się, że wszystkie węzły istnieją
    for n in dep_graph.keys():
        rev.setdefault(n, set())
    return rev


def print_tree(dep_graph, sizes):
    rev = invert_graph(dep_graph)

    # rooty: snapy, od których nikt nie zależy (brak reverse deps)
    roots = [s for s, rdeps in rev.items() if not rdeps]
    roots.sort()

    seen = set()

    def fmt_size(name):
        mb = sizes.get(name)
        if mb is None:
            return ""
        return f" ({mb:.1f} MB)"

    def dfs(node, prefix=""):
        first_time = node not in seen
        if first_time:
            seen.add(node)
            extra = fmt_size(node)
        else:
            extra = " (*)"

        print(f"{node}{extra}")

        if not first_time:
            return

        children = sorted(dep_graph.get(node, []))
        for i, child in enumerate(children):
            last = (i == len(children) - 1)
            branch = "└─ " if last else "├─ "
            print(f"{prefix}{branch}", end="")
            child_prefix = ("   " if last else "│  ") + prefix
            dfs(child, child_prefix)

    for root in sorted(roots):
        dfs(root)
        print()


def main():
    sizes = get_snap_sizes()
    dep_graph = parse_connections()
    print_tree(dep_graph, sizes)


if __name__ == "__main__":
    main()
