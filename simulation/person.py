# from simulation.simulation import Simulation
import pygame, sys, random, time, numpy as np
from .utils import helperfunctions, settings as s
from .agent import Agent

class Person(Agent):
    def __init__(self, pos, v, population, identifier):
        super(Person, self).__init__(pos, v)
        self.population = population
        self.identifier = identifier

    def neighbor_forces(self):
        align_force, cohesion_force, separate_force = np.zeros(2), np.zeros(2), np.zeros(2)
        neighbors = self.population.find_neighbors(self, s.RADIUS_VIEW)

        if neighbors:
            align_force = self.align(self.population.find_neighbor_velocity(neighbors))
            cohesion_force = self.cohesion(self.population.find_neighbor_center(neighbors))
            separate_force = self.population.find_neighbor_separation(self, neighbors)

        return align_force, cohesion_force, separate_force

    def align(self, neighbor_force):
        """
        Function to align the agent in accordance to neighbor velocity
        :param neighbor_force: np.array(x,y)
        """
        return helperfunctions.normalize(neighbor_force - self.v)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors
        :param neighbor_rotation: np.array(x,y)
        """
        force = neighbor_center - self.pos
        return helperfunctions.normalize(force - self.v)

    def update_actions(self, simulation):
        neighbors = self.population.find_neighbors(self, s.RADIUS_VIEW)
        try:
            grid_pos = helperfunctions.pos_to_grid(simulation.environment, self.pos[0], self.pos[1], simulation.camera.scroll)
            collision = simulation.environment.world[grid_pos[0]][grid_pos[1]]["collision"]
            base = simulation.environment.world[grid_pos[0]][grid_pos[1]]["base"]
            for tile in simulation.environment.world:
                if bool(collision):
                    self.max_speed = 1
                    self.avoid_obstacle()
                    self.health -= s.OBSTACLE_DAMAGE
                else:
                    self.max_speed = s.MAX_SPEED
        except:
            self.population.remove_agent(self)

        # degrees of laziness
        if s.EXPERIMENT == "lazy":
            if self.identifier < s.PERCENTAGE * s.NUM_AGENTS:
                self.protect_base(simulation)
            else:
                if not self.food_delivery:
                    self.forage_food(simulation)
                else:
                    self.return_to_base(simulation)

        # selfish vs non-selfish
        elif s.EXPERIMENT == "selfish":
            if not self.food_delivery:
                self.forage_food(simulation)
            else:
                self.return_to_base(simulation)

        elif s.EXPERIMENT == "ternary":
            # if self.identifier < s.PERCENTAGE * s.NUM_AGENTS:
            if self.identifier < simulation.percentage_lazy * s.NUM_AGENTS:
                self.protect_base(simulation)
            else:
                if not self.food_delivery:
                    self.forage_food(simulation)
                else:
                    self.return_to_base(simulation)

        # requires a minimum number of agents in order to attempt foraging
        elif s.EXPERIMENT == "group":
            if self.identifier < simulation.percentage_lazy * s.NUM_AGENTS:
                self.protect_base(simulation)
            else:
                if not self.food_delivery:
                    if len(neighbors) > simulation.num_neighbors:
                        self.forage_food(simulation)
                else:
                    self.return_to_base(simulation)
                    
        # cohesion and alignment keep a foraging swarm glued
        elif s.EXPERIMENT == "swarm":
            if self.identifier < simulation.percentage_lazy * s.NUM_AGENTS:
                self.protect_base(simulation)
            else:
                if not self.food_delivery:
                    self.forage_food(simulation)
                else:
                    self.return_to_base(simulation)

        elif s.EXPERIMENT == "supershare":
            if self.identifier < simulation.percentage_lazy * s.NUM_AGENTS:
                self.protect_base(simulation)
            else:
                if not self.food_delivery:
                    self.forage_food(simulation)
                else:
                    self.return_to_base(simulation)

        align_force, cohesion_force, separate_force = self.neighbor_forces()
        total_force = self.wander(s.WANDER_DIST, s.WANDER_RADIUS, s.WANDER_ANGLE) * s.WANDER_WEIGHT\
                + align_force * s.ALIGNMENT_WEIGHT \
                + cohesion_force * s.COHESION_WEIGHT\
                + separate_force * s.SEPERATION_WEIGHT
                
        self.steering += helperfunctions.truncate(total_force / self.mass, s.MAX_FORCE)
        
        