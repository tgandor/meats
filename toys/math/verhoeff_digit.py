d_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

p_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

inv_table = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def verhoeff_check_digit(number: str, debug: bool = False) -> int:
    """Returns the Verhoeff check digit for the given number (without the check digit)."""
    c = 0
    reversed_digits = map(int, reversed(number))
    for i, digit in enumerate(reversed_digits, start=1):
        # indexing from 1, because 0 is reserved for the check digit.
        c = d_table[c][p_table[i % 8][digit]]
        if debug:
            print(f"Step {i}: c = {c}, digit = {digit}")
    return inv_table[c]


def verhoeff_validate(number: str, debug: bool = False) -> bool:
    """Validates whether the full number (with check digit) is correct."""
    c = 0
    reversed_digits = map(int, reversed(number))
    for i, digit in enumerate(reversed_digits):
        c = d_table[c][p_table[i % 8][digit]]
        if debug:
            print(f"Step {i}: c = {c}, digit = {digit}")
    return c == 0


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate or verify the Verhoeff check digit."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        "--check-digit",
        help="Calculate the check digit for the given number (without the check digit).",
    )
    group.add_argument(
        "-v",
        "--validate",
        help="Verify the correctness of the full number (with check digit).",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print intermediate values for debugging purposes.",
    )
    args = parser.parse_args()

    if args.check_digit is not None:
        check_digit = verhoeff_check_digit(args.check_digit, debug=args.debug)
        print(f"Check digit for number {args.check_digit}: {check_digit}")

    if args.validate is not None:
        is_valid = verhoeff_validate(args.validate, debug=args.debug)
        print(f"Number {args.validate} is {'valid' if is_valid else 'invalid'}")
        if not is_valid:
            expected_check_digit = verhoeff_check_digit(args.validate[:-1], debug=args.debug)
            print(
                f"Expected check digit for {args.validate[:-1]}: {expected_check_digit}"
            )


if __name__ == "__main__":
    main()
