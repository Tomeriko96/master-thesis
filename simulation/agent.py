import pygame, sys, random, time, copy, numpy as np
from .utils import displayfunctions, helperfunctions, settings as s

class Agent(pygame.sprite.Sprite):
    def __init__(self, pos=None, v=None):
        super(Agent, self).__init__()
        self.image_file = s.AGENT_IMAGE
        self.width, self.height = s.WIDTH, s.HEIGHT
        self.base_image, self.rect = helperfunctions.image_with_rect(self.image_file, [self.width, self.height])
        self.image = self.base_image
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = self.mask.scale((self.width, self.height))

        self.mass = s.MASS
        self.max_speed = s.MAX_SPEED
        self.min_speed = s.MIN_SPEED
        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi)

        self.steering = np.zeros(2)
        self.pos = np.zeros(2) if pos is None else pos
        self.v = self.set_velocity() if v is None else v
        self.dT = s.dT

        self.health, self.min_health, self.max_health = s.MAX_HEALTH, s.MIN_HEALTH, s.MAX_HEALTH
        self.health_bar_length = self.width * 2
        self.health_ratio = s.MAX_HEALTH / self.health_bar_length
        self.food_delivery = False

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.rect.center = tuple(pos)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v

    def set_velocity(self):
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity = [random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus(),
                    random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus()]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity

    def wander(self, wander_dist, wander_radius, wander_angle):
        """
        Function to make the agents to perform random movement
        """
        rands = 2 * np.random.rand() - 1
        cos = np.cos(self.wandering_angle)
        sin = np.sin(self.wandering_angle)
        n_v = helperfunctions.normalize(self.v)
        circle_center = n_v * wander_dist
        displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * wander_radius)
        wander_force = circle_center + displacement
        self.wandering_angle += wander_angle * rands
        return wander_force

    def avoid_obstacle(self):
        """
        Function to avoid obstacles
        """
        self.v = (helperfunctions.rotate(helperfunctions.normalize(self.v)) * helperfunctions.norm(self.v))
        self.v *= s.AVOIDANCE_VELOCITY
        self.pos += self.v
        
    def return_to_base(self, simulation):
        pos = pygame.math.Vector2(self.pos[0], self.pos[1])
        base_pos = pygame.math.Vector2(simulation.base_location[0], simulation.base_location[1])
        dist = pos.distance_to(base_pos)
        dx, dy = (base_pos[0] - self.pos[0], base_pos[1] - self.pos[1])
        stepx, stepy = (dx*4 / dist, dy*4 / dist)
        self.pos += (stepx, stepy)
        if (abs(self.rect.center[0] - simulation.base_center[0])) < s.TILE_SIZE and (abs(self.rect.center[1] - simulation.base_center[1])) < s.TILE_SIZE:
            if self.food_delivery:
                simulation.storage += 1
                simulation.transit -= 1
                self.food_delivery = False
            # if simulation.storage > 0:
            #     simulation.storage -= 1
            #     self.health = 100

    def protect_base(self, simulation):
        pos = pygame.math.Vector2(self.pos[0], self.pos[1])
        base_pos = pygame.math.Vector2(simulation.base_location[0], simulation.base_location[1])
        dist = pos.distance_to(base_pos)
        if dist > s.TILE_SIZE * s.ISO_X / 20:
            dx, dy = (base_pos[0] - self.pos[0], base_pos[1] - self.pos[1])
            stepx, stepy = (dx*2 / dist, dy*2 / dist)
            self.pos += (stepx, stepy)
            # if simulation.storage > 0:
            #     simulation.storage -= 1
            #     self.health = 100

    def forage_food(self, simulation):
        if len(simulation.food.mushrooms) > 0:
            pos = pygame.math.Vector2(self.pos[0], self.pos[1])
            mushroom = min([e for e in simulation.food.mushrooms], key=lambda e: pos.distance_to(pygame.math.Vector2(e.pos[0], e.pos[1])))
            food_pos = pygame.math.Vector2(mushroom.rect.center[0], mushroom.rect.center[1])
            dist = pos.distance_to(food_pos)
            if dist < 4*s.TILE_SIZE:
                self.min_speed = s.MAX_SPEED
                dx, dy = (food_pos[0] - self.pos[0], food_pos[1] - self.pos[1])
                stepx, stepy = (dx*4 / dist, dy*4 / dist)
                self.pos += (stepx, stepy)
                collide = pygame.sprite.collide_mask(self, mushroom)
                if bool(collide) or (abs(self.rect.center[0] - mushroom.rect.center[0])) < 30 and (abs(self.rect.center[1] - mushroom.rect.center[1])) < 30:
                    simulation.food.mushrooms.remove(mushroom)
                    if s.EXPERIMENT == "selfish":
                        self.health = 100
                    elif s.EXPERIMENT == "ternary":
                        chance = random.randint(1, 10) / 10
                        # if chance <= s.CHANCE:
                        if chance <= simulation.selfish_chance:
                            self.health = 100
                        else:
                            simulation.transit += 1
                            self.food_delivery = True
                            
                    elif s.EXPERIMENT == "group":
                        chance = random.randint(1, 10) / 10
                        if chance <= simulation.selfish_chance:
                            self.health = 100
                        else:
                            neighbors = self.population.find_neighbors(self, s.RADIUS_VIEW)
                            for agent in self.population.agents:
                                for neighbor in neighbors:
                                    if agent.identifier == neighbor:
                                        agent.health += (500/len(neighbors)+1)
                                        self.health += (500/len(neighbors)+1)

                    elif s.EXPERIMENT == "swarm":
                        chance = random.randint(1, 10) / 10
                        if chance <= simulation.selfish_chance:
                            self.health = 100
                        else:
                            neighbors = self.population.find_neighbors(self, s.RADIUS_VIEW)
                            for agent in self.population.agents:
                                for neighbor in neighbors:
                                    if agent.identifier == neighbor:
                                        agent.health += (500/len(neighbors)+1)
                                        self.health += (500/len(neighbors)+1)

                    elif s.EXPERIMENT == "supershare":
                        chance = random.randint(1, 10) / 10
                        if chance <= simulation.selfish_chance:
                            self.health = 100
                        else:
                            simulation.transit += 1
                            self.food_delivery = True
                            for agent in self.population.agents:
                                agent.food_delivery = True
                            for agent in self.population.agents:
                                agent.health += (500/len(self.population.agents))
                                


                    else:
                        simulation.transit += 1
                        self.food_delivery = True

    def update(self):
        self.v = helperfunctions.truncate(self.v + self.steering, self.max_speed, self.min_speed)
        self.pos += self.v * self.dT
        self.health -= (100 / (s.RUNTIME))
        self.health = self.min_health if self.health < self.min_health else self.health
        self.health = self.max_health if self.health > self.max_health else self.health
        if self.health < 1:
            self.population.remove_agent(self)

    def display(self, screen, camera):
        self.pos += (camera.dx, camera.dy)
        self.rect.center = tuple(self.pos)
        screen.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            displayfunctions.display_health_bar(self, screen)

    def reset_frame(self):
        self.steering = np.zeros(2)