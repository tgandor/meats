#!/usr/bin/env python

import pygame
import sys

fps = 75
width = 640
height = 480

pygame.init()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyGame Template")
screen = pygame.display.get_surface()

box = pygame.surface.Surface((10, 10))
box.fill((255, 0, 0))

box_rect = box.get_rect()
speed = [2, 2]
trail = False

while True:
    events = pygame.event.get()
    for event in events:
        print(event)
        if (event.type == pygame.QUIT or 
                (event.type == pygame.KEYDOWN and event.unicode == u'q')):
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            delta = [c1 - c0 for c0, c1 in zip((box_rect.left, box_rect.top), event.pos)]
            speed = [3*ci/sum(d*d for d in delta)**.5 for ci in delta]
        elif event.type == pygame.KEYDOWN and event.unicode == u' ':
            trail = not trail
        elif event.type == pygame.KEYDOWN and event.unicode == u'f':
            speed = [2*x for x in speed]
        elif event.type == pygame.KEYDOWN and event.unicode == u's':
            speed = [x/2 for x in speed]

    if not trail:
        screen.fill((0, 0, 0))
    screen.blit(box, box_rect)
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
    box_rect = box_rect.move(speed)
    if box_rect.left < 0 or box_rect.left > width - box_rect.width:
        speed[0] *= -1
    if box_rect.top < 0 or box_rect.top > height - box_rect.height:
        speed[1] *= -1
