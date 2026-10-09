def ean13_check_digit(first_12_digits: str) -> int:
    # assert len(first_12_digits) == 12
    assert first_12_digits.isdigit()

    total = sum(
        int(digit) * (1 if position % 2 == 1 else 3)
        for position, digit in enumerate(first_12_digits, start=1)
    )

    return (10 - total % 10) % 10


barcode = input("Podaj 13 (typowo...) cyfr z kodu kreskowego: ").strip()

expected = ean13_check_digit(barcode[:-1])
actual = int(barcode[-1])

print("Wyliczona cyfra kontrolna:", expected)
print("Cyfra występująca w kodzie:", actual)
print("Kod poprawny:", expected == actual)
