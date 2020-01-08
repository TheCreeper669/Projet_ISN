import pygame.locals as pglocals

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
K_MOTION_UP = pglocals.K_UP
K_MOTION_DOWN = pglocals.K_DOWN
K_MOTION_LEFT = pglocals.K_LEFT
K_MOTION_RIGHT = pglocals.K_RIGHT
K_MOTION = (K_MOTION_UP, K_MOTION_DOWN, K_MOTION_LEFT, K_MOTION_RIGHT)

K_WEAPON_UP = pglocals.K_w
K_WEAPON_DOWN = pglocals.K_s
K_WEAPON_LEFT = pglocals.K_a
K_WEAPON_RIGHT = pglocals.K_d
K_WEAPON = (K_WEAPON_UP, K_WEAPON_DOWN, K_WEAPON_LEFT, K_WEAPON_RIGHT)

# Dir
DIR_SETTINGS = "./data/settings.json"