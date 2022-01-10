# =========================================

# from former enemy.py

# import pygame, sys, random, time, numpy as np
# from .utils import displayfunctions, helperfunctions, settings as s

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, pos=None, v=None):
#         super(Enemy, self).__init__()
#         self.image_file = s.SNAKE_IMAGE
#         self.width, self.height = s.SNAKE_WIDTH, s.SNAKE_HEIGHT
#         self.base_image, self.rect = helperfunctions.image_with_rect(self.image_file, [self.width, self.height])
#         self.image = self.base_image
#         self.mask = pygame.mask.from_surface(self.image)
#         self.mask = self.mask.scale((self.width, self.height))

#         self.mass = s.SNAKE_MASS
#         self.max_speed = s.MAX_SPEED
#         self.min_speed = s.MIN_SPEED
#         self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi)

#         self.steering = np.zeros(2)
#         self.pos = np.zeros(2) if pos is None else pos
#         self.v = self.set_velocity() if v is None else v
#         self.dT = s.dT

#         self.max_health, self.health, self.min_health = s.MAX_HEALTH, s.MAX_HEALTH, s.MIN_HEALTH
#         self.energy, self.min_energy = s.MAX_ENERGY, s.MIN_ENERGY
#         self.health_bar_length, self.energy_bar_length = self.width * 2, self.width * 2
#         self.health_ratio, self.energy_ratio = s.MAX_HEALTH / self.health_bar_length, s.MAX_ENERGY / self.energy_bar_length
    
#     @property
#     def pos(self):
#         return self._pos

#     @pos.setter
#     def pos(self, pos):
#         self._pos = pos
#         self.rect.center = tuple(pos)

#     @property
#     def v(self):
#         return self._v

#     @v.setter
#     def v(self, v):
#         self._v = v

#     def set_velocity(self):
#         angle = np.pi * (2 * np.random.rand() - 1)
#         velocity = [random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus(),
#                     random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus()]
#         velocity *= np.array([np.cos(angle), np.sin(angle)])
#         return velocity

#     def wander(self, wander_dist, wander_radius, wander_angle):
#         """
#         Function to make the agents to perform random movement
#         """
#         rands = 2 * np.random.rand() - 1
#         cos = np.cos(self.wandering_angle)
#         sin = np.sin(self.wandering_angle)
#         n_v = helperfunctions.normalize(self.v)
#         circle_center = n_v * wander_dist
#         displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * wander_radius)
#         wander_force = circle_center + displacement
#         self.wandering_angle += wander_angle * rands
#         return wander_force

#     def avoid_obstacle(self):
#         """
#         Function to avoid obstacles
#         """
#         self.v = (helperfunctions.rotate(helperfunctions.normalize(self.v)) * helperfunctions.norm(self.v))
#         self.v *= s.AVOIDANCE_VELOCITY
#         self.pos += self.v

#     def find_nearest_agent(self, players):
#         for sprite in players:
#             if (len(sprite.agents)) > 0:
#                 pos = pygame.math.Vector2(self.pos[0], self.pos[1])
#                 player = min([a for a in sprite.agents], key=lambda a: pos.distance_to(pygame.math.Vector2(a.pos[0], a.pos[1])))
#                 player_pos = pygame.math.Vector2(player.pos[0], player.pos[1])
#                 dist = pos.distance_to(player_pos)
#                 dx, dy = (player_pos[0] - self.pos[0], player_pos[1] - self.pos[1])
#                 stepx, stepy = (dx*4 / dist, dy*4 / dist)
#                 self.pos += (stepx, stepy)
#                 return dist
#         return np.Inf

#     def forage_food(self, simulation, player_dist):
#         if len(simulation.food.mushrooms) > 0:
#             pos = pygame.math.Vector2(self.pos[0], self.pos[1])
#             mushroom = min([e for e in simulation.food.mushrooms], key=lambda e: pos.distance_to(pygame.math.Vector2(e.pos[0], e.pos[1])))
#             food_pos = pygame.math.Vector2(mushroom.rect.center[0], mushroom.rect.center[1])
#             dist = pos.distance_to(food_pos)
#             if dist < player_dist:
#                 dx, dy = (food_pos[0] - self.pos[0], food_pos[1] - self.pos[1])
#                 stepx, stepy = (dx*4 / dist, dy*4 / dist)
#                 self.pos += (stepx, stepy)
#                 collide = pygame.sprite.collide_mask(self, mushroom)
#                 if bool(collide) or (abs(self.rect.center[0] - mushroom.rect.center[0])) < 30 and (abs(self.rect.center[1] - mushroom.rect.center[1])) < 30:
#                     simulation.food.mushrooms.remove(mushroom)
#                     self.mushroom_effect()

#     def update_actions(self, simulation):
#         try:
#             grid_pos = helperfunctions.pos_to_grid(simulation.environment, self.pos[0], self.pos[1], simulation.camera.scroll)
#             collision = simulation.environment.world[grid_pos[0]][grid_pos[1]]["collision"]
#             for tile in simulation.environment.world:
#                 if bool(collision):
#                     self.max_speed = 1
#                     self.avoid_obstacle()
#                     self.health -= s.OBSTACLE_DAMAGE
#                 else:
#                     self.max_speed = s.MAX_SPEED
#         except:
#             simulation.enemies.remove(self)
#         player_dist = self.find_nearest_agent(simulation.to_display)
#         self.forage_food(simulation, player_dist)
                
#         force = self.wander(s.WANDER_DIST, s.WANDER_RADIUS, s.WANDER_ANGLE)
#         self.steering += helperfunctions.truncate(force / self.mass, s.MAX_FORCE)

#     def mushroom_effect(self):
#         self.width += 25
#         self.height += 25
#         self.base_image, self.rect = helperfunctions.image_with_rect(self.image_file, [self.width, self.height])
#         self.image = self.base_image
#         self.mask = pygame.mask.from_surface(self.image)
#         self.mask = self.mask.scale((self.width, self.height))
#         self.energy = 100
#         self.max_health += 500
#         self.health += 500
#         self.health_ratio = self.max_health / self.health_bar_length

#     def update(self):
#         self.energy -= self.max_speed * 0.01
#         self.health = self.min_health if self.health < self.min_health else self.health
#         self.energy = self.min_energy if self.energy < self.min_energy else self.energy

#     def display(self, screen, camera):
#         self.pos += (camera.dx, camera.dy)
#         self.rect.center = tuple(self.pos)
#         screen.blit(self.image, self.rect)
#         mouse_pos = pygame.mouse.get_pos()
#         if self.rect.collidepoint(mouse_pos):
#             displayfunctions.display_health_bar(self, screen)
#             displayfunctions.display_energy_bar(self, screen)

#     def reset_frame(self):
#         self.steering = np.zeros(2)


# =========================================
# from displayfunctions.py

# def display_energy_bar(self, screen):
#     """
#     Displays a blue energy bar above the agent.
#     """
#     pygame.draw.rect(screen, s.BLUE, (self.pos[0] - s.ENERGY_X, self.pos[1] - s.ENERGY_Y, self.energy / self.energy_ratio, 10))
#     pygame.draw.rect(screen, s.WHITE, (self.pos[0] - s.ENERGY_X, self.pos[1] - s.ENERGY_Y, self.energy_bar_length, 10), 4)

# =========================================
# from helperfunctions.py

# def get_energy(sprite):
#     avg_energy = 0
#     if len(sprite.agents) > 0:
#         total_energy = 0
#         for agent in sprite.agents:
#             total_energy += agent.energy
#         avg_energy = total_energy / len(sprite.agents)
#     return avg_energy

# update info
    # avg_energy = get_energy(sprite)
    # return count, avg_health, avg_energy

# def update_enemies(self):
#     if len(self.enemies) > 0:
#         for enemy in self.enemies:
#             enemy.update_actions(self)
#             enemy.update()
#             if enemy.health < 1:
#                 self.enemies.remove(enemy)

# =========================================
# from logfunctions.py

# def get_list(self, count, avg_health, avg_energy):

    # experiment_list.append(self.day)
    # experiment_list.append(self.hour)
    # experiment_list.append(self.minute)
    # experiment_list.append(s.PERCENTAGE)
    # experiment_list.append(avg_energy)

    # experiment_list.append(len(self.food.mushrooms))
    # experiment_list.append(self.transit)
    # experiment_list.append(self.storage)

    # experiment_list.append(len(self.enemies))


# =========================================
# from settings.py

# Simulation: gameplay
# RUNTIME = 720

# Energy bar
# ENERGY_X, ENERGY_Y = 25, 40

# PERLIN_SCALE = ISO_X / 2
# PERLIN_UPPER = 15
# PERLIN_LOWER = -35

# Enemy
# SNAKE_IMAGE = "simulation/utils/assets/snake.png"
# SNAKE_WIDTH = 75
# SNAKE_HEIGHT = 50

# MAX_ENERGY = 100
# MIN_ENERGY = 0
# SNAKE_MASS = 100

# =========================================
# from person.py

            
        # self.flee(simulation.enemies) if len(neighbors) < s.NEIGHBOR_THRESHOLD else self.eliminate_enemy(simulation.enemies)

        # else:

# =========================================
# from agent.py

        # self.energy, self.min_energy = s.MAX_ENERGY, s.MIN_ENERGY
        # self.health_bar_length, self.energy_bar_length = self.width * 2, self.width * 2
        # self.health_ratio, self.energy_ratio = s.MAX_HEALTH / self.health_bar_length, s.MAX_ENERGY / self.energy_bar_length

        # self.health -= 0.01

                # self.energy -= self.max_speed * 0.005
        # if self.energy < 30:
        #     self.health -= .005
                # self.energy = self.min_energy if self.energy < self.min_energy else self.energy


# display()
            # displayfunctions.display_energy_bar(self, screen)

    # def flee(self, enemies):
    #     if len(enemies) > 0:
    #         pos = pygame.math.Vector2(self.pos[0], self.pos[1])
    #         enemy = min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.pos[0], e.pos[1])))
    #         enemy_pos = pygame.math.Vector2(enemy.pos[0], enemy.pos[1])
    #         dist = pos.distance_to(enemy_pos)
    #         if dist < s.TILE_SIZE * s.ISO_X/5:
    #             dx, dy = (enemy_pos[0] - self.pos[0], enemy_pos[1] - self.pos[1])
    #             stepx, stepy = (dx*4 / dist, dy*4 / dist)
    #             self.pos -= (stepx, stepy)
    #             if (abs(self.rect.center[0] - enemy.rect.center[0])) < 20 and (abs(self.rect.center[1] - enemy.rect.center[1])) < 20:
    #                 enemy.health -= 1
    #                 self.health -= 5
    #                 self.energy -= 20

    # def eliminate_enemy(self, enemies):
    #     if len(enemies) > 0:
    #         pos = pygame.math.Vector2(self.pos[0], self.pos[1])
    #         enemy = min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.pos[0], e.pos[1])))
    #         enemy_pos = pygame.math.Vector2(enemy.pos[0], enemy.pos[1])
    #         dist = pos.distance_to(enemy_pos)
    #         if dist < s.TILE_SIZE * s.ISO_X/5:
    #             dx, dy = (enemy_pos[0] - self.pos[0], enemy_pos[1] - self.pos[1])
    #             stepx, stepy = (dx*4 / dist, dy*4 / dist)
    #             self.pos += (stepx, stepy)
    #             if (abs(self.rect.center[0] - enemy.rect.center[0])) < 20 and (abs(self.rect.center[1] - enemy.rect.center[1])) < 20:
    #                 enemy.health -= 5
    #                 self.health -= 2
    #                 self.energy -= 5



# =========================================
# from environment.py

        # self.perlin_scale = s.PERLIN_SCALE


        # perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)
        # tile = "tree" if (perlin >= s.PERLIN_UPPER) or (perlin <= s.PERLIN_LOWER) else ""

    # def spawn_enemy(self, screen, camera, enemies):
    #     enemy_chance, enemy_pos_x, enemy_pos_y = helperfunctions.spawn()
    #     if enemy_chance == 1:
    #         for x in range(self.grid_length_x):
    #             for y in range(self.grid_length_y):
    #                 render_pos = self.world[x][y]["render_pos"]
    #                 collision = self.world[x][y]['collision']
    #                 base = self.world[x][y]['base']
    #                 if not bool(collision) and not bool(base):
    #                     if render_pos[0] == enemy_pos_x and int(render_pos[1]) == enemy_pos_y:
    #                         enemies.add(Enemy(pos = np.array([render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x + s.TILE_SIZE*2,
    #                                         render_pos[1] - (s.BOUNDS - camera.scroll.y - s.TILE_SIZE)]), v=None))


            # count, avg_health, avg_energy = helperfunctions.update_info(sprite)

        # for mushroom in simulation.food.mushrooms:
        #     mushroom.display(simulation.screen)

        # for enemy in simulation.enemies:
        #     enemy.display(simulation.screen, simulation.camera)
            
        # for home in simulation.home.home:
        #     home.display(simulation.screen)

        # self.spawn_enemy(simulation.screen, simulation.camera, simulation.enemies)

        # return count, avg_health, avg_energy

# =========================================
# from simulation.py

        # self.enemies = pygame.sprite.Group()
        # helperfunctions.update_enemies(self)
        # count, avg_health, avg_energy = self.environment.draw(self)
            # 'Number of enemies = {}'.format(len(self.enemies))
            # 'Swarm energy = {0:10.1f}'.format(avg_energy),
        # return count, avg_health, avg_energy
                # count, avg_health, avg_energy = self.draw()
                    # logfunctions.get_list(self, count, avg_health, avg_energy)
            # logfunctions.get_list(self, count, avg_health, avg_energy)

# =========================================
# from swarm.py
