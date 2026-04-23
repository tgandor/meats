#!/usr/bin/env python

import argparse
from pathlib import Path
from packaging.requirements import Requirement
from packaging.version import Version, InvalidVersion
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def load_req_file(path: Path):
    """Parse requirements/constraints file into dict: {name: Requirement}"""
    result = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            req = Requirement(line)
            result[req.name.lower()] = req
        except Exception:
            console.print(f"[red]Warning: cannot parse line:[/red] {line}")
    return result


def compare_dicts(lhs: dict, rhs: dict):
    lhs_keys = set(lhs.keys())
    rhs_keys = set(rhs.keys())
    common = lhs_keys & rhs_keys
    only_lhs = lhs_keys - rhs_keys
    only_rhs = rhs_keys - lhs_keys
    return common, only_lhs, only_rhs


def extract_version(req: Requirement):
    """Return pinned version if exists, else None."""
    if req.specifier:
        for spec in req.specifier:
            if spec.operator == "==":
                return spec.version
    return None


def pick_version(vA, vB, strategy):
    if strategy == "lhs":
        return vA
    if strategy == "rhs":
        return vB
    if strategy == "none":
        return None
    if strategy == "older":
        try:
            return min(Version(vA), Version(vB)).public
        except InvalidVersion:
            return vA
    if strategy == "newer":
        try:
            return max(Version(vA), Version(vB)).public
        except InvalidVersion:
            return vB
    raise ValueError(f"Unknown strategy: {strategy}")


def write_requirements(path: Path, reqs: dict):
    lines = []
    for name, req in sorted(reqs.items()):
        lines.append(str(req))
    path.write_text("\n".join(lines) + "\n")


def merge_requirements(lhs_reqs, rhs_reqs, strategy):
    merged = {}
    common, only_lhs, only_rhs = compare_dicts(lhs_reqs, rhs_reqs)

    # common
    for name in common:
        rA = lhs_reqs[name]
        rB = rhs_reqs[name]
        vA = extract_version(rA)
        vB = extract_version(rB)

        if vA == vB:
            merged[name] = rA
            continue

        chosen = pick_version(vA, vB, strategy)
        if chosen is None:
            merged[name] = Requirement(name)
        else:
            merged[name] = Requirement(f"{name}=={chosen}")

    # only lhs
    for name in only_lhs:
        merged[name] = lhs_reqs[name]

    # only rhs
    for name in only_rhs:
        merged[name] = rhs_reqs[name]

    return merged


def detect_req_vs_constraints_conflicts(reqs, constr):
    conflicts = []
    for name, req in reqs.items():
        if name not in constr:
            continue
        v_req = extract_version(req)
        v_con = extract_version(constr[name])
        if v_req and v_con and v_req != v_con:
            conflicts.append((name, v_req, v_con))
    return conflicts


def print_table(title, rows, headers):
    table = Table(title=title, box=box.SIMPLE_HEAVY)
    for h in headers:
        table.add_column(h)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lhs", help="Left-hand environment folder")
    parser.add_argument("rhs", help="Right-hand environment folder")
    parser.add_argument(
        "--strategy",
        default="newer",
        choices=["older", "newer", "lhs", "rhs", "none"],
        help="Conflict resolution strategy",
    )
    parser.add_argument(
        "--out", default="merged", help="Output folder for merged files"
    )
    args = parser.parse_args()

    lhs = Path(args.lhs)
    rhs = Path(args.rhs)
    out = Path(args.out)
    out.mkdir(exist_ok=True)

    # Load files
    lhs_req = load_req_file(lhs / "requirements.txt")
    lhs_con = load_req_file(lhs / "constraints.txt")
    rhs_req = load_req_file(rhs / "requirements.txt")
    rhs_con = load_req_file(rhs / "constraints.txt")

    # Compare top-level requirements
    common, only_lhs, only_rhs = compare_dicts(lhs_req, rhs_req)
    print_table(
        "Top-level requirements",
        [(n,) for n in sorted(common)],
        ["Common"],
    )
    print_table(
        "Only in LHS",
        [(n,) for n in sorted(only_lhs)],
        ["Package"],
    )
    print_table(
        "Only in RHS",
        [(n,) for n in sorted(only_rhs)],
        ["Package"],
    )

    # Compare constraints
    c_common, c_only_lhs, c_only_rhs = compare_dicts(lhs_con, rhs_con)
    diff_rows = []
    for name in sorted(c_common):
        vA = extract_version(lhs_con[name])
        vB = extract_version(rhs_con[name])
        if vA != vB:
            diff_rows.append((name, vA or "-", vB or "-"))
    print_table(
        "Constraint differences",
        diff_rows,
        ["Package", "LHS", "RHS"],
    )

    # Detect req vs constraints conflicts
    conflicts_lhs = detect_req_vs_constraints_conflicts(lhs_req, lhs_con)
    conflicts_rhs = detect_req_vs_constraints_conflicts(rhs_req, rhs_con)

    if conflicts_lhs:
        print_table(
            "Conflicts in LHS (requirements vs constraints)",
            [(n, r, c) for n, r, c in conflicts_lhs],
            ["Package", "Req", "Con"],
        )
    if conflicts_rhs:
        print_table(
            "Conflicts in RHS (requirements vs constraints)",
            [(n, r, c) for n, r, c in conflicts_rhs],
            ["Package", "Req", "Con"],
        )

    # Merge
    merged_req = merge_requirements(lhs_req, rhs_req, args.strategy)
    merged_con = merge_requirements(lhs_con, rhs_con, args.strategy)

    write_requirements(out / "requirements.txt", merged_req)
    write_requirements(out / "constraints.txt", merged_con)

    console.print(f"[green]Merged files written to {out}[/green]")


if __name__ == "__main__":
    main()
