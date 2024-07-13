import pygame

# App
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Constants
SPEED = 400
ACCELERATION = 10
PLAYER_DAMAGE = 20
HEALTH = 100

MAP_X = 2500
MAP_Y = 2500
HOUSES = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

vector = pygame.math.Vector2
MOVEMENT_KEYS = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1)
        }