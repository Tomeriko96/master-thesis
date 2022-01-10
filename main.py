import pygame, sys, time, random, os
from argparse import ArgumentParser
from simulation.simulation import Simulation
from simulation.utils import settings as s

if not s.TEST:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--percentage-lazy",
                        dest="lazy",
                        help="The percentage of the population that does not contribute in foragin.",
                        default=0)
    parser.add_argument("-s", "--selfish-chance",
                        dest="chance",
                        help="The chance that an agent does not share the food it collects.",
                        default=0)
    parser.add_argument("-n", "--neighbors",
                        dest="neighbors",
                        help="The number of neighbors required to forage.",
                        default=0)
    options = parser.parse_args()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    demo = Simulation(screen, options)
    demo.run()


# TODO: try instead of selfish or sharing with base
# share with the neighbors 