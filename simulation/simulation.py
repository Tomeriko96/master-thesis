import pygame, sys, random, time
from .utils import displayfunctions, events, helperfunctions, logfunctions ,settings as s
from .environment import Environment
from .utils.camera import Camera
from .population import Population
from .food import Food
from .base import Base

class Simulation:
    def __init__(self, screen, options):
        self.running = True
        self.iter = s.RUNTIME
        self.swarm = Population()
        self.num_agents = s.NUM_AGENTS
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.base = None
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.day, self.hour, self.minute = s.CLOCK
        self.food = Food()
        self.home = Base()
        self.transit, self.storage = 0, 0
        self.percentage_lazy = float(options.lazy)
        self.selfish_chance = float(options.chance)
        self.num_neighbors = float(options.neighbors)
        
    def initialize(self):
        self.camera = Camera(self)
        self.environment = Environment()
        helperfunctions.initialize(self)
        self.swarm.initialize(self)
        self.to_update = pygame.sprite.Group(self.swarm)
        self.to_display = pygame.sprite.Group(self.to_update)
        helperfunctions.update_base(self)

    def update(self):
        if s.TEST:
            self.camera.update()
            displayfunctions.camera_correction(self.camera, self.food.mushrooms)
            displayfunctions.camera_correction(self.camera, self.home.home)
            helperfunctions.update_base(self)

        self.to_update.update(self)

    def draw(self):
        self.screen.fill((0, 0, 0))
        count, avg_health = self.environment.draw(self)
        
        text_list = [
            'Day {} = {}:{}'.format(self.day, self.hour, self.minute),
            'Swarm size = {}'.format(count),
            'Swarm health = {0:10.1f}'.format(avg_health),
            'Available food = {}'.format(len(self.food.mushrooms))
            # 'Food in transit = {}'.format((self.transit)),
            # 'Food at base = {}'.format((self.storage))
        ]
        if s.TEST:
            displayfunctions.display_info(self.screen, text_list)
        pygame.display.flip()
        return count, avg_health

    def run(self):
        self.initialize()
        while self.running:
            for _ in range(self.iter):
                displayfunctions.update_world_clock(self)
                events.events(self)
                self.update()
                count, avg_health = self.draw()
                if count == 0:
                    self.running = False
                    logfunctions.get_list(self, count, avg_health)
                    pygame.quit()
                    sys.exit()
            self.running = False
            logfunctions.get_list(self, count, avg_health)
            pygame.quit()
            sys.exit()