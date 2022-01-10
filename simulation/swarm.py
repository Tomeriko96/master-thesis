import pygame, sys, random, time, copy, numpy as np
from .utils import helperfunctions, settings as s

class Swarm(pygame.sprite.Sprite):
    def __init__(self):
        super(Swarm, self).__init__()
        self.agents = pygame.sprite.Group()
        
    def add_agent(self, agent):
        self.agents.add(agent)

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def find_neighbors(self, agent, radius):
        agents = list(self.agents).copy()
        neighbors = []
        for j, neighbor in enumerate(agents):
            if agent == neighbor:
                continue
            elif helperfunctions.dist(agent.pos, neighbor.pos) < radius:
                neighbors.append(j)
        return neighbors

    def find_neighbor_velocity(self, neighbors):
        neighbor_sum_v = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_v += list(self.agents)[idx].v
        return neighbor_sum_v / len(neighbors)

    def find_neighbor_center(self, neighbors):
        neighbor_sum_pos = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_pos += list(self.agents)[idx].pos
        return neighbor_sum_pos / len(neighbors)

    def find_neighbor_separation(self, boid, neighbors):
        separate = np.zeros(2)
        for idx in neighbors:
            neighbor_pos = list(self.agents)[idx].pos
            difference = boid.pos - neighbor_pos
            difference /= helperfunctions.norm(difference)
            separate += difference
        return separate / len(neighbors)

    def update(self, simulation):
        for agent in self.agents:
            agent.update_actions(simulation)
            if simulation.storage > 0:
                count = 0
                for agent in self.agents:
                    if (abs(agent.rect.center[0] - simulation.base_center[0])) < s.TILE_SIZE*2 and (abs(agent.rect.center[1] - simulation.base_center[1])) < s.TILE_SIZE*2:
                        # agent.health += 100
                        count += 1
                for agent in self.agents:
                    if (abs(agent.rect.center[0] - simulation.base_center[0])) < s.TILE_SIZE*2 and (abs(agent.rect.center[1] - simulation.base_center[1])) < s.TILE_SIZE*2:
                        if s.EXPERIMENT == "supershare":
                            agent.health == 0
                        # agent.health += (500 / count)
                        # count += 1
                simulation.storage -= 1
            agent.update()

    def display(self, simulation):
        for agent in self.agents:
            agent.display(simulation.screen, simulation.camera)
            agent.reset_frame()