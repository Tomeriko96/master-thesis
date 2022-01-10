import pygame, sys, random, time, numpy as np
from .utils import helperfunctions, settings as s
from .swarm import Swarm
from .person import Person

class Population(Swarm):
    def __init__(self):
        super(Population, self).__init__()

    def initialize(self, simulation):
        for id, agent in enumerate(range(simulation.num_agents)):
            self.add_agent(Person(pos = np.array(simulation.base) + id, v = None, population = simulation.swarm, identifier = id))