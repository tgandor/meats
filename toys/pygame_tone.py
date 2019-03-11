import pygame
from pygame.locals import *
import math
import numpy as np

# Updated from:
# https://stackoverflow.com/a/24891952/1338797

#----------------------------------------------------------------------
# functions
#----------------------------------------------------------------------

def SineWave(freq=1000, volume=16000, length=1):

    num_steps = length * SAMPLE_RATE
    s = []

    for n in range(num_steps):
        value = int(math.sin(n * freq * (6.28318/SAMPLE_RATE) * length) * volume)
        s.append( [value, value] )

    return np.array(s, dtype=np.int32)

def SquareWave(freq=1000, volume=100000, length=1):

    num_steps = length * SAMPLE_RATE
    s = []

    length_of_plateau = SAMPLE_RATE / (2*freq)

    counter = 0
    state = 1

    for n in range(num_steps):

        value = state * volume
        s.append( [value, value] )

        counter += 1

        if counter == length_of_plateau:
            counter = 0
            state *= -1

    return np.array(s, dtype=np.int32)

def MakeSound(arr):
    return pygame.sndarray.make_sound(arr)

def MakeSquareWave(freq=1000):
    return MakeSound(SquareWave(freq))

def MakeSineWave(freq=1000):
    return MakeSound(SineWave(freq))

#----------------------------------------------------------------------
# main program
#----------------------------------------------------------------------

pygame.init()

size = (1200, 720)
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Nibbles!')

SAMPLE_RATE = 22050 ## This many array entries == 1 second of sound.

SINE_WAVE_TYPE = 'Sine'
SQUARE_WAVE_TYPE = 'Square'

sound_types = {SINE_WAVE_TYPE:SQUARE_WAVE_TYPE, SQUARE_WAVE_TYPE:SINE_WAVE_TYPE}

current_type = SINE_WAVE_TYPE

current_played = { 'z': None, 'c': None }

_running = True
while _running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            _running = False

        # some keys don't depend on `current_type`

        elif event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                _running = False

            if event.key == K_RETURN:
                current_type = sound_types[current_type]  #Toggle
                print('new type:', current_type)

        # some keys depend on `current_type`

        if current_type == SINE_WAVE_TYPE:

            if event.type == KEYDOWN:

                #lower notes DOWN

                if event.key == K_z:
                    print(current_type, 130.81)
                    current_played['z'] = MakeSineWave(130.81)
                    current_played['z'].play()

                elif event.key == K_c:
                    print(current_type, 180.81)
                    current_played['c'] = MakeSineWave(180.81)
                    current_played['c'].play()

            elif event.type == KEYUP:

                #lower notes UP

                if event.key == K_z:
                    current_played['z'].fadeout(350)
                elif event.key == K_c:
                    current_played['c'].fadeout(350)

        elif current_type == SQUARE_WAVE_TYPE:

            if event.type == KEYDOWN:

                #lower notes DOWN

                if event.key == K_z:
                    print(current_type, 80.81)
                    current_played['z'] = MakeSineWave(80.81)
                    #current_played['z'] = MakeSquareWave(130.81)
                    current_played['z'].play()

                elif event.key == K_c:
                    print(current_type, 180.81)
                    current_played['c'] = MakeSineWave(180.81)
                    #current_played['c'] = MakeSquareWave(130.81)
                    current_played['c'].play()

            elif event.type == KEYUP:

                #lower notes UP

                if event.key == K_z:
                    current_played['z'].fadeout(350)
                elif event.key == K_c:
                    current_played['c'].fadeout(350)

pygame.quit()
