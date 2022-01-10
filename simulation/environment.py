import pygame, sys, random, time, noise, numpy as np
from .utils import helperfunctions, settings as s
from .food import Food

class Environment:
    def __init__(self):
        self.grid_length_x = s.ISO_X
        self.grid_length_y = s.ISO_Y
        self.grass_tiles = pygame.Surface((s.GRASS_SURFACE)).convert_alpha()
        self.tiles = helperfunctions.load_images()
        self.world = self.create_world()
        
    def create_world(self):
        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
                if world_tile['tile'] != "":
                    world_tile['collision'] = True
                elif world_tile["tile"] == "":
                    if world_tile["grid"][0] == (s.ISO_X-1) or world_tile["grid"][1] == (s.ISO_Y-1) or world_tile["grid"][0] == 0 or world_tile["grid"][1] == 0:
                        world_tile['collision'] = True
                    
        return world

    def grid_to_world(self, grid_x, grid_y):
        rect = [
            (grid_x * s.TILE_SIZE, grid_y * s.TILE_SIZE),
            (grid_x * s.TILE_SIZE + s.TILE_SIZE, grid_y * s.TILE_SIZE),
            (grid_x * s.TILE_SIZE + s.TILE_SIZE, grid_y * s.TILE_SIZE + s.TILE_SIZE),
            (grid_x * s.TILE_SIZE, grid_y * s.TILE_SIZE + s.TILE_SIZE)
        ]

        iso_poly = [helperfunctions.cart_to_iso(x, y) for x, y in rect]
        minx, miny = min([x for x, y in iso_poly]), min([y for x, y in iso_poly])
        tile = ""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True,
            "base": False
        }

        return out

    def render_world(self, screen, camera):
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                base = self.world[x][y]["base"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - s.TILE_SIZE) + camera.scroll.y))

    def spawn_food(self, screen, camera, food):
        food_chance, food_pos_x, food_pos_y = helperfunctions.spawn()
        if food_chance == 1:
            for x in range(self.grid_length_x):
                for y in range(self.grid_length_y):
                    render_pos = self.world[x][y]["render_pos"]
                    collision = self.world[x][y]['collision']
                    base = self.world[x][y]['base']
                    if not bool(collision) and not bool(base):
                        if render_pos[0] == food_pos_x and int(render_pos[1]) == food_pos_y:
                            food.add_food(file = s.FOOD_IMAGE, pos = [render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x + s.TILE_SIZE*2,
                                            render_pos[1] - (s.BOUNDS - camera.scroll.y - s.TILE_SIZE)], 
                                            scale = s.FOOD_SCALE )


    def draw(self, simulation):
        if s.TEST:
            simulation.screen.blit(self.grass_tiles, (simulation.camera.scroll.x, simulation.camera.scroll.y))

        for sprite in simulation.to_display:
            count, avg_health = helperfunctions.update_info(sprite)
            sprite.display(simulation)

        for mushroom in simulation.food.mushrooms:
            mushroom.display(simulation.screen)
        for home in simulation.home.home:
            home.display(simulation.screen)
        if s.TEST:
            self.render_world(simulation.screen, simulation.camera)                                   
        self.spawn_food(simulation.screen, simulation.camera, simulation.food)

        return count, avg_health