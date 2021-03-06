import pygame.locals as pglc
from pygame.math import Vector2 as vec
import os
from random import randint

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
K_MOTION_UP, K_MOTION_DOWN, K_MOTION_LEFT, K_MOTION_RIGHT = pglc.K_w, pglc.K_s, pglc.K_a, pglc.K_d
K_MOTION = (K_MOTION_UP, K_MOTION_DOWN, K_MOTION_LEFT, K_MOTION_RIGHT)

K_WEAPON_UP, K_WEAPON_DOWN, K_WEAPON_LEFT, K_WEAPON_RIGHT = pglc.K_UP, pglc.K_DOWN, pglc.K_LEFT, pglc.K_RIGHT
K_WEAPON = (K_WEAPON_UP, K_WEAPON_DOWN, K_WEAPON_LEFT, K_WEAPON_RIGHT)

# Directories
DIR_ROOT = os.path.abspath(".") + "/"
DIR_DATA = DIR_ROOT + "data/"

DIR_KEYBOARDS = DIR_DATA + "keyboards/"
DIR_MAPS = DIR_DATA + "maps/"
DIR_BIOMES = DIR_DATA + "biomes/"
DIR_MUSICS = DIR_DATA + "musics/"
DIR_SOUNDS = DIR_DATA + "sounds/"

DIR_IMAGES = DIR_DATA + "images/"
DIR_IMAGE_ICONS = DIR_IMAGES + "icons/"
DIR_IMAGE_TILES = DIR_IMAGES + "tiles/"
DIR_IMAGE_SPRITES = DIR_IMAGES + "sprites/"
DIR_IMAGE_ENTITIES = DIR_IMAGES + "entities/"

# Files
FILE_SETTINGS = DIR_DATA + "settings.json"

# Musics
MUSIC_THEME = DIR_MUSICS + "theme.mp3"
MUSIC_BATTLE = DIR_MUSICS + "battle.mp3"
MUSIC_BOSS = DIR_MUSICS + "boss.wav"
MUSIC_GAMEOVER = DIR_MUSICS + "gameover.wav"
MUSIC_WON = DIR_MUSICS + "won.wav"

# Extensions
EXT_IMG = ".png"
EXT_MAP = ".map"

# Funcs
def vec_mul(u, v):
	return vec(u.x * v.x, u.y * v.y)

def vec_pow(u, n):
	return vec(u.x ** n, u.y ** n)

