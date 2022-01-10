import math, random, pygame, numpy as np
from . import settings as s

def area(a, b):
    """
    :param a: object mid point
    :param b: scale
    :return:
    """
    if b < a:
        max = a + 0.5 * b
        min = a - 0.5 * b
    else:
        max = a + 0.25 * b
        min = a - 0.25 * b
    return min, max

def dist(a, b):
    """
    return the distance between two vectors
    :param a: np.array
    :param b: np.array
    :return:
    """
    return norm(a - b)

def image_with_rect(filename, scale):
    _image = pygame.image.load(filename)
    _image = pygame.transform.scale(_image, (scale[0], scale[1]))
    return _image, _image.get_rect()

def randrange(a, b):
    """
    Random number between a and b.
    """
    return a + np.random.random() * (b - a)

def plusminus():
    return 1 if (random.random() > 0.5) else -1

def rotate(vector):
    new_vector = np.zeros(2)
    theta = np.deg2rad(random.randint(135, 225))
    cs = np.cos(theta)
    sn = np.sin(theta)
    new_vector[0] = vector[0] * cs - vector[1] * sn
    new_vector[1] = vector[0] * sn + vector[1] * cs
    return new_vector

def normalize(vector):
    """
    Function to normalize a vector
    ----------
    param vector : np.array
    return: unit vector
    """
    n = norm(vector)
    return np.zeros(2) if n < 1e-13 else np.array(vector) / n

def truncate(vector, max_length, min_lenght = None):
    """
    Truncate the length of a vector to a maximum/minimum value.
    """
    n = norm(vector)
    if n > max_length:
        return normalize(vector) * max_length
    elif min_lenght != None and n < min_lenght:
        return normalize(vector) * min_lenght
    else:
        return vector

def norm(vector):
    """
    Compute the norm of a vector.
    """
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def speedvector(max_speed):
    return [random.randrange(1, max_speed * 2 + 1) * plusminus(), random.randrange(1, max_speed * 2 + 1) * plusminus()]

def relative(u, v):
    return [int(u[i]) - int(v[i]) for i in range(len(u))]

def load_images():
    """
    Loads the sprites of the world objects into a dict.
    """
    block = pygame.image.load("simulation/utils/assets/block.png").convert_alpha()
    tree = pygame.image.load("simulation/utils/assets/tree.png").convert_alpha()
    return {"block": block, "tree": tree}

def cart_to_iso(x, y):
    """
    Cartesian coordinates to isometric.
    """
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y

def pos_to_grid(world, x, y, scroll):
    """
    Removes the camera scroll influence on the location and returns the grid location.
    """
    world_x = x - scroll.x - world.grass_tiles.get_width() / 2
    world_y = y - scroll.y
    cart_y = (2 * world_y - world_x) / 2
    cart_x = cart_y + world_x
    grid_x = int(cart_x // s.TILE_SIZE)
    grid_y = int(cart_y // s.TILE_SIZE)
    return grid_x, grid_y

def spawn():
    """
    Helperfunction to retrieve the chance and position for food and enemies.
    """
    chance = 1
    upper_bound = s.ISO_X * (s.TILE_SIZE / 10)
    pos_x = random.randint(-1, upper_bound) * 16
    pos_y = random.randint(-1, upper_bound) * 16

    return chance, pos_x, pos_y

def get_count(sprite):
    return len(sprite.agents)

def get_health(sprite):
    avg_health = 0
    if len(sprite.agents) > 0:
        total_health = 0
        for agent in sprite.agents:
            total_health += agent.health
        avg_health = total_health / len(sprite.agents)
    return avg_health

def update_info(sprite):
    count = get_count(sprite)
    avg_health = get_health(sprite)
    return count, avg_health

def get_base(environment, camera):
    """
    Get coordinates for a base, that is inside the isometric world, and not on a tile with an obstacle.
    """
    coordinates = None
    _, pos_x, pos_y = spawn()
    for x in range(5, environment.grid_length_x - 5):
        for y in range(5, environment.grid_length_y - 5):
            render_pos = environment.world[x][y]["render_pos"]
            collision = environment.world[x][y]['collision']
            if not bool(collision):
                if render_pos[0] == pos_x and int(render_pos[1]) == pos_y:
                    environment.world[x][y]["base"] = True
                    x_coordinate = render_pos[0] + environment.grass_tiles.get_width()/2 + camera.scroll.x + s.TILE_SIZE * 2
                    y_coordinate = render_pos[1] - (s.BOUNDS - camera.scroll.y - s.TILE_SIZE)
                    coordinates = [x_coordinate, y_coordinate]
                    original_coordinates = (pos_x, pos_y)
                    return coordinates, original_coordinates

def initialize(self):
    while self.base == None:
            try:
                self.base, original = get_base(self.environment, self.camera)
            except Exception:
                pass
    self.home.add_home(file = s.BASE_IMAGE, pos = [original[0] + self.environment.grass_tiles.get_width() / 2 + self.camera.scroll.x + s.TILE_SIZE * 2,
                                        original[1] - (s.BOUNDS - self.camera.scroll.y -  s.TILE_SIZE)], 
                                        scale = s.FOOD_SCALE )

def update_base(self):
    for base in self.home.home:
        self.base_location = base.pos
        self.base_center = base.rect.center