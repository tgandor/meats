#!/usr/bin/env python

# Bibliograpy:
# https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
# https://stackoverflow.com/questions/311627/how-to-print-a-date-in-a-regular-format
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python

from __future__ import print_function

import argparse
import datetime

import icalendar


def is_future_datetime_or_date(datetime_or_date):
    if type(datetime_or_date) is datetime.date:
        return datetime_or_date >= datetime.date.today()
    else:
        return datetime_or_date.replace(tzinfo=None) > datetime.datetime.now()


def is_future(event):
    if is_future_datetime_or_date(event.get('dtstart').dt):
        return True

    recurrent = event.get('rrule')
    if recurrent:
        until = recurrent.get('until')

        if until is None:
            return True

        if len(until) == 0:
            # guessing
            return True

        for option in until:
            if is_future_datetime_or_date(option):
                return True

    return False


def is_all_day(event):
    start = event.get('dtstart').dt
    return (type(start) is datetime.date)


def print_event(event):
    start = event.get('dtstart').dt
    recurrent = event.get('rrule')

    def rrule_info():
        if recurrent:
            print('Repeats:', recurrent.get('freq'), ', with intervals:', recurrent.get('interval'))

    if type(start) is datetime.date:
        print(start.strftime('%Y-%m-%d (%A)'), event.get('summary'))
        rrule_info()
        return

    end = event.get('dtend').dt

    recurrent = event.get('rrule')

    if recurrent and recurrent.get('freq') == ['WEEKLY']:
        print(start.strftime('(%A) %X'), '-', end.strftime('%X'), event.get('summary'))
        return

    if recurrent and recurrent.get('freq') == ['MONTHLY']:
        print(
            'Each', recurrent.get('BYMONTHDAY'), 'day of month:',
            start.strftime('%X'), '-', end.strftime('%X'), event.get('summary')
        )
        return

    print(start.strftime('(%A) %X'), '-', end.strftime('%X'), event.get('summary'))
    rrule_info()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ical_file')
    parser.add_argument('--all', '-a', action='store_true', help='print all events, not just future')
    parser.add_argument('--full-day', '-f', action='store_true', help='print only all-day events')
    parser.add_argument('--no-full-day', '-F', action='store_true', help='print only not-all-day events')
    parser.add_argument('--search', '-s', help='filter summary by string')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--exclude', '-x', help='filter summary by string (negative)')

    args = parser.parse_args()

    cal = icalendar.Calendar.from_ical(open(args.ical_file).read())

    for component in cal.walk():
        if component.name == "VEVENT":
            if not args.all and not is_future(component):
                continue

            if args.no_full_day and is_all_day(component):
                continue

            if args.full_day and not is_all_day(component):
                continue

            if args.search and args.search not in component.get('summary'):
                continue

            if args.exclude and args.exclude in component.get('summary'):
                continue

            print_event(component)
            print('-' * 60)

        elif args.verbose:
            print('ignoring component:', component)
