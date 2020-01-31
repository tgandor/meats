#!/usr/bin/env python

# https://github.com/MycroftAI/pylisten

import argparse
import datetime
import math

from pylisten import Listener, WindowListener, FeatureListener

parser = argparse.ArgumentParser()
parser.add_argument('--window', action='store_true')
parser.add_argument('--feature', action='store_true')
parser.add_argument('--listener', action='store_true')
parser.add_argument('--timers', action='store_true')
parser.add_argument('--output', '-o', help='output file for volume')
parser.add_argument('--limit', '-l', type=int, help='max samples to process / save')
parser.add_argument('--sqrt', action='store_true', help='sqare root of volume (stars)')
parser.add_argument('--threshold', '-t', type=float, default=0.15)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()


def show_timers(args):
    start = next_info = last_check = datetime.datetime.now()
    time_loud = datetime.timedelta()
    time_quiet = datetime.timedelta()
    loud = False
    refresh = datetime.timedelta(seconds=1)
    # t = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    # see discussion in: https://stackoverflow.com/questions/1937622/convert-date-to-datetime-in-python
    t = datetime.datetime.combine(datetime.date.today(), datetime.time())

    for features in FeatureListener(lambda x: [abs(x).mean()], 1024, 10):
        now = datetime.datetime.now()

        loud = any(features > args.threshold)

        if loud:
            time_loud += (now - last_check)
        else:
            time_quiet += (now - last_check)

        if args.debug:
            print('dbg:', now-last_check, features)

        if now > next_info:
            # WHY doesn't timedelta have __format__?
            # because of that I do crazy shit like getting todays date as datetime
            # via `datetime.combine` - and then adding timedeltas to that to get a datetime,
            # hich then handles formatting
            print(
                '{:%H:%M:%S} (volume: {:.3f}) total: {:%M:%S}, LOUD: {:%M:%S}, quiet: {:%M:%S} {}'.format(
                    now, max(features), t+(now-start), t+time_loud, t+time_quiet, 'LOUD' if loud else 'quiet'
                )
            )
            next_info = now + refresh

        last_check = now


if args.listener:
    for chunk in Listener(frames_per_buffer=1024, rate=44100):
        print(chunk.shape, 'Current volume:', abs(chunk).mean(), 'span:', chunk.min(), chunk.max())
elif args.feature:
    for features in FeatureListener(lambda x: [abs(x).mean()], 1024, 20):
        print(features.shape, 'Past 20 volumes:', features)
elif args.window:
    for window in WindowListener(1024 * 10, 1024):
        print(window.shape, 'Volume of last 10 chunks:', abs(window).mean())
elif args.timers:
    show_timers(args)
else:
    # inspired by:
    # https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
    count = 0
    output = None
    try:
        if args.output:
            output = open(args.output, 'w')
        for chunk in Listener(frames_per_buffer=512, rate=24100):
            vol = int(abs(chunk).mean() * 1000)
            if args.sqrt:
                vol = int(math.sqrt(vol))
            print(datetime.datetime.now(), '{:3d}'.format(vol), '*' * vol)
            count += 1
            if count == args.limit:
                break
            if output:
                output.write('{}\n'.format(vol))
    finally:
        if output:
            output.close()
