import pygame.locals as pglc
from pygame.math import Vector2 as vec
import os

# Colors
TRANSPARENT = pglc.Color(0x00, 0x00, 0x00, 0x00)
WHITE = pglc.Color(0xff, 0xff, 0xff)
BLACK = pglc.Color(0x00, 0x00, 0x00)
RED = pglc.Color(0xff, 0x00, 0x00)
GREEN = pglc.Color(0x00, 0xff, 0x00)
BLUE = pglc.Color(0x00, 0x00, 0xff)
YELLOW = pglc.Color(0xff, 0xff, 0x00)
MAGENTA = pglc.Color(0xff, 0X00, 0xff)
CYAN = pglc.Color(0x00, 0xff, 0xff)
def setAlpha(color, a):
	return pglc.Color(color.r, color.g, color.b, a)

# Keyboard
K_MOTION_UP = pglc.K_UP
K_MOTION_DOWN = pglc.K_DOWN
K_MOTION_LEFT = pglc.K_LEFT
K_MOTION_RIGHT = pglc.K_RIGHT
K_MOTION = (K_MOTION_UP, K_MOTION_DOWN, K_MOTION_LEFT, K_MOTION_RIGHT)

K_WEAPON_UP = pglc.K_w
K_WEAPON_DOWN = pglc.K_s
K_WEAPON_LEFT = pglc.K_a
K_WEAPON_RIGHT = pglc.K_d
K_WEAPON = (K_WEAPON_UP, K_WEAPON_DOWN, K_WEAPON_LEFT, K_WEAPON_RIGHT)

# Directories
DIR_ROOT = os.path.abspath(".") + "/"
DIR_DATA = DIR_ROOT + "data/"

DIR_KEYBOARDS = DIR_DATA + "keyborad/"
DIR_MAPS = DIR_DATA + "maps/"

DIR_IMAGES = DIR_DATA + "images/"
DIR_IMAGE_ICONS = DIR_IMAGES + "icons/"
DIR_IMAGE_TILES = DIR_IMAGES + "tiles/"
DIR_IMAGE_SPRITES = DIR_IMAGES + "sprites/"
DIR_IMAGE_ENTITIES = DIR_IMAGES + "entities/"

DIR_JSONS = DIR_DATA + "jsons/"
DIR_JSON_MAPS = DIR_JSONS + "maps/"
DIR_JSON_BIOMES = DIR_JSONS + "biomes/"

# Files
FILE_SETTINGS = DIR_DATA + "settings.json"

# Extensions
EXT_MAP = ".map"

# Funcs
def vec_mul(u, v):
	return vec(u.x * v.x, u.y * v.y)

def vec_pow(u, n):
	return vec(u.x ** n, u.y ** n)

