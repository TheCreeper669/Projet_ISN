import sys
import pygame
import json
import time

from vars import *
from sprites import *

class Game:
	def __init__(self):
		# load settings
		self.settings = {}
		self.settings = load_json("./settings.json")
		self.width = self.settings["window"]["width"]
		self.height = self.settings["window"]["height"]
		self.title = self.settings["window"]["title"]
		self.icon = self.settings["window"]["icon"]
		self.framerate = self.settings["window"]["framerate"]

		# setup pygame stuff
		self.window = pygame.display.set_mode((self.width, self.height))
		self.rect = self.window.get_rect()
		pygame.display.set_caption(self.title)
		pygame.display.set_icon(pygame.image.load(self.icon))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(pygame.font.get_default_font(), 32)

		# time
		self.last_tick = 1
		self.time = 1

		# setup sprites
		self.sprites = pygame.sprite.Group()
		self.tiles = pygame.sprite.Group()
		self.obstacles = pygame.sprite.Group()
		self.displays = pygame.sprite.Group()

		self.player = Player(self)
		self.framerate_display = Display(self, lambda game: "fps: " + str(int(game.clock.get_fps())), BLACK, (0, 0))
		self.acc_display = Display(self, lambda game: "acc: " + str(game.player.acc), BLACK, (0, 32))
		self.vel_display = Display(self, lambda game: "vel: " + str(game.player.vel), BLACK, (0, 32 * 2))
		self.pos_display = Display(self, lambda game: "pos: " + str(game.player.pos), BLACK, (0, 32 * 3))
		get_tiles(self, vec2(18, 10), vec2(0), vec2(77), 1, [
			[GREEN, GREEN, GREEN],
			[GREEN, None, GREEN],
			[GREEN, None, GREEN, GREEN, GREEN, GREEN, GREEN],
			[GREEN, None, None, None, None, None, GREEN],
			[GREEN, None, GREEN, GREEN, GREEN, GREEN, GREEN],
			[GREEN],
			[GREEN]
		])

		# run main loop
		self.time = time.perf_counter()
		self.clock.tick(self.framerate)
		self.stop = False
		while not self.stop:
			self.loop()

	"""
	def save(self):
		# save settings
		with open("./settings.json", mode= "w", encoding= "utf-8") as file:
			file.write(json.dumps(self.settings, sort_keys= True, indent= 4))
	"""

	def loop(self):
		self.last_tick = time.perf_counter() - self.time
		self.time = time.perf_counter()
		self.clock.tick(self.framerate)
		self.actual_fps = self.clock.get_fps()
		self.events()
		self.update()
		self.draw()

	def events(self):
		self.keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stop = True

	def update(self):
		self.sprites.update()

	def draw(self):
		self.window.fill(BLACK)
		self.tiles.draw(self.window)
		self.player.draw(self.window)
		self.displays.draw(self.window)
		pygame.display.flip()
