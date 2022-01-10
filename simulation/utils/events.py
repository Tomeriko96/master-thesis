import pygame, sys
from pygame.locals import *

def events(self):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
                pygame.quit()
                sys.exit()