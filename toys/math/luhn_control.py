def luhn_valid(number: str) -> bool:
    number = number.replace(" ", "")

    if not number.isdigit():
        raise ValueError("Numer musi zawierać wyłącznie cyfry")

    total = 0

    # Idziemy od prawej. Ostatnia cyfra jest kontrolna,
    # więc podwajamy co drugą cyfrę, zaczynając od przedostatniej.
    for position, char in enumerate(reversed(number)):
        digit = int(char)

        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0


number = input("Numer do sprawdzenia: ").strip()

print("Luhn pasuje:", luhn_valid(number))
