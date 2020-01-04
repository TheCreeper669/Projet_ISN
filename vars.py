import pygame

# Colors
WHITE = (0xff, 0xff, 0xff)
BLACK = (0x00, 0x00, 0x00)
RED = (0xff, 0x00, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE = (0x00, 0x00, 0xff)
YELLOW = (0xff, 0xff, 0x00)
MAGENTA = (0xff, 0X00, 0xff)
CYAN = (0x00, 0xff, 0xff)

# Keyboard
K_MOTION_UP = pygame.K_UP
K_MOTION_DOWN = pygame.K_DOWN
K_MOTION_LEFT = pygame.K_LEFT
K_MOTION_RIGHT = pygame.K_RIGHT
K_MOTION = (K_MOTION_UP, K_MOTION_DOWN, K_MOTION_LEFT, K_MOTION_RIGHT)

K_WEAPON_UP = pygame.K_w
K_WEAPON_DOWN = pygame.K_s
K_WEAPON_LEFT = pygame.K_a
K_WEAPON_RIGHT = pygame.K_d
K_WEAPON = (K_WEAPON_UP, K_WEAPON_DOWN, K_WEAPON_LEFT, K_WEAPON_RIGHT)

# Dir
DIR_PLAYERS = "./data/players/"
DIR_WEAPONS = "./data/weapons/"