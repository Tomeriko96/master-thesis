TEST = True
RUNTIME = 1440

EXPERIMENT = ""
# EXPERIMENT = "lazy"
# EXPERIMENT = "selfish"
# EXPERIMENT = "ternary"
# EXPERIMENT = "swarm"
# EXPERIMENT = "group"
# EXPERIMENT = "supershare"

# Swarm
NUM_AGENTS = 20 
AGENT_IMAGE = "simulation/utils/assets/lemmings.png"

# Health bar
HEALTH_X, HEALTH_Y = 25, 25

# Environment, alter size for experiment?
TILE_SIZE = 64
ISO_X = 20
ISO_Y = 20

GRASS_SURFACE = ISO_X * TILE_SIZE * 2, ISO_Y * TILE_SIZE + 2 * TILE_SIZE
OBSTACLE_DAMAGE = 0.005
# REST_THRESHOLD = 20
NEIGHBOR_THRESHOLD = 2
CLOCK = [1, 0, 0]

# Food
FOOD_IMAGE = "simulation/utils/assets/food.png"
FOOD_SCALE = [300, 600]

# Objects
BASE_IMAGE = "simulation/utils/assets/base.png"
BOUNDS = 73

# Agent
MAX_HEALTH = 100
MIN_HEALTH = 0
WIDTH = 20
HEIGHT = 20
dT = 0.2 

#agents mass
MASS = 50
AVOIDANCE_VELOCITY = 0.5

#agent maximum speed and 'duration'
MAX_SPEED = 4.
MIN_SPEED = 4.
MAX_FORCE = 0.6
RADIUS_VIEW = TILE_SIZE*2

#wandering definition
if EXPERIMENT == "swarm":
    WANDER_RADIUS = 3.0
    WANDER_DIST = 0.5
    WANDER_ANGLE = 2.0
else:
    WANDER_RADIUS = 3.0
    WANDER_DIST = 0.5
    WANDER_ANGLE = 2.0
# WANDER_RADIUS = 0.
# WANDER_DIST = 0
# WANDER_ANGLE = 0.

#weights for velocity forces
if EXPERIMENT == "swarm":
    COHESION_WEIGHT = 8.
    ALIGNMENT_WEIGHT = 8.
    SEPERATION_WEIGHT = 0.

elif EXPERIMENT == "supershare":
    COHESION_WEIGHT = 2.
    ALIGNMENT_WEIGHT = 2.
    SEPERATION_WEIGHT = 4.

else:
    COHESION_WEIGHT = 4.
    ALIGNMENT_WEIGHT = 3.
    SEPERATION_WEIGHT = 2.
WANDER_WEIGHT = 0.01
# WANDER_WEIGHT = 10

# Camera
CAMERA_BOUND = 0.97
CAMERA_DXDY = [0, 0]
CAMERA_SPEED = 5
CAMERA_INIT = -ISO_X / 2 * TILE_SIZE, -ISO_Y / 2 * TILE_SIZE / 2

# Colours
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# TEXT
TEXT_OFFSET = 10
TEXT_SIZE = 25
TEXT_DY = 20