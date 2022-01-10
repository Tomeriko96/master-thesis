import pygame
from . import settings as s

def update_world_clock(self):
    self.minute += 1
    if self.minute == 60:
        self.minute = 0
        self.hour += 1
    if self.hour == 24:
        self.day += 1
        self.hour = 0

def draw_text(screen, text, size, colour, pos):
    """
    Displays text in the left corner of the screen.
    """
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft = pos)
    screen.blit(text_surface, text_rect)

def display_info(screen, text_list):
    """
    Calls the draw_text function iteratively.
    """
    y_position = s.TEXT_OFFSET
    for text in text_list:
        draw_text(screen, text, size = s.TEXT_SIZE, colour = s.WHITE, pos = (s.TEXT_OFFSET, y_position))
        y_position += s.TEXT_DY

def display_health_bar(self, screen):
    """
    Displays a red health bar above the agent.
    """
    pygame.draw.rect(screen, s.RED, (self.pos[0] - s.HEALTH_X, self.pos[1] - s.HEALTH_Y, self.health / self.health_ratio, 10))
    pygame.draw.rect(screen, s.WHITE, (self.pos[0] - s.HEALTH_X, self.pos[1] - s.HEALTH_Y, self.health_bar_length, 10), 4)

def camera_correction(camera, group):
    """
    Corrects the position relative to the camera for the food and object classes.
    """
    for entity in group:
        entity.pos += (camera.dx, camera.dy)
        entity.rect = entity.image.get_rect(center = entity.pos)
        entity.mask = pygame.mask.from_surface(entity.image)