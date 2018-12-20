#!/usr/bin/env python3

levels = {
    'junior': 8,
    'medium': 8,
    'senior': 6,
}

percent_range = range(70, 131)

raise_percent = [
    (80, 7),
    (90, 6.5),
    (115, 5),
    (125, 2),
    (130, 1),
]

for level, pitchfork in levels.items():
    for start in percent_range:

        new_percent = start * 100 / (100 + pitchfork)
        percent_raise = 0
        for thresh, raise_p in raise_percent:
            if new_percent < thresh:
                percent_raise = raise_p
                break

        print(f'{level}, before: {start:3}%, after: {new_percent:5.1f}%, raise: {percent_raise}%')
