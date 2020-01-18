#!/usr/bin/env python

# https://github.com/MycroftAI/pylisten

import argparse

from pylisten import Listener, WindowListener, FeatureListener

parser = argparse.ArgumentParser()
parser.add_argument('--window', action='store_true')
parser.add_argument('--feature', action='store_true')
parser.add_argument('--listener', action='store_true')
args = parser.parse_args()

if args.listener:
    for chunk in Listener(frames_per_buffer=512, rate=24100):
        print(chunk.shape, 'Current volume:', abs(chunk).mean())
elif args.feature:
    for features in FeatureListener(lambda x: [abs(x).mean()], 1024, 20):
        print(features.shape, 'Past 20 volumes:', features)
elif args.window:
    for window in WindowListener(1024 * 10, 1024):
        print(window.shape, 'Volume of last 10 chunks:', abs(window).mean())
else:
    # inspired by:
    # https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
    for chunk in Listener(frames_per_buffer=512, rate=24100):
        vol = int(abs(chunk).mean() * 1000)
        print('*' * vol)
