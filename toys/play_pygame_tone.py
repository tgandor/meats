import math
import time

import numpy as np

import pygame
from pygame.locals import *


def SineWave(freq=1000, volume=16000, length=1):

    num_steps = length * SAMPLE_RATE
    s = []

    for n in range(num_steps):
        value = int(math.sin(n * freq * (6.28318/SAMPLE_RATE) * length) * volume)
        s.append( [value, value] )

    return np.array(s, dtype=np.int32)


def MakeSound(arr):
    return pygame.sndarray.make_sound(arr)


def MakeSineWave(freq=1000):
    return MakeSound(SineWave(freq, volume=4000))


SAMPLE_RATE = 22050 ## This many array entries == 1 second of sound.

pygame.init()
sound = MakeSineWave(435)
sound.play()
time.sleep(1.2)
pygame.quit()
