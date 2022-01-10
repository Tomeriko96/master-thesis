import pygame
from . import settings as s

class Camera:
    def __init__(self, simulation):
        self.width, self.height = simulation.width, simulation.height
        self.scroll = pygame.Vector2(s.CAMERA_INIT)
        self.dx, self.dy = s.CAMERA_DXDY
        self.speed = s.CAMERA_SPEED

    def update(self):
        self.dx, self.dy = s.CAMERA_DXDY
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] > self.width * s.CAMERA_BOUND:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * (1 - s.CAMERA_BOUND):
            self.dx = self.speed

        if mouse_pos[1] > self.height * s.CAMERA_BOUND:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * (1 - s.CAMERA_BOUND):
            self.dy = self.speed

        self.scroll += (self.dx, self.dy)