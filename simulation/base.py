import pygame, sys, random, time, numpy as np
from .utils import helperfunctions, settings as s

class Base(pygame.sprite.Sprite):
    def __init__(self):
        super(Base, self).__init__()
        self.home = pygame.sprite.Group()
    
    def add_home(self, file, pos, scale):
        self.home.add(Home(filename = file, pos = np.array(pos), scale = scale))

class Home(pygame.sprite.Sprite):
    def __init__(self, filename = None, pos=None, scale=None):
        super(Home, self).__init__()
        self.image, self.rect = helperfunctions.image_with_rect(filename, scale)
        self.pos = pos if pos is not None else np.zeros(2)
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def display(self, screen):
        screen.blit(self.image, self.rect)