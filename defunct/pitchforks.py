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
        new_bonus_percent = new_percent + percent_raise

        effective_ratio = (new_bonus_percent * (100 + pitchfork) / 100) / start
        effective_percent = (effective_ratio - 1) * 100

        print(f'{level}, from: {start:3}%, after pf: {new_percent:5.1f}%, nom: {percent_raise:3}%,'
              f' to: {new_bonus_percent:5.1f}% effective {effective_percent:.1f}%')
