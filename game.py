import sys
import pygame
import json

from vars import *
from sprites import *

class Game:
	def __init__(self):
		# load settings
		self.settings = {}
		with open("./settings.json", mode= "r", encoding= "utf-8") as file:
			self.settings = json.loads(file.read())
		self.width = self.settings["window"]["width"]
		self.height = self.settings["window"]["height"]
		self.title = self.settings["window"]["title"]
		self.icon = self.settings["window"]["icon"]
		self.framerate = self.settings["window"]["framerate"]

		# setup pygame stuff
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.title)
		pygame.display.set_icon(pygame.image.load(self.icon))
		self.clock = pygame.time.Clock()

		# setup sprites
		self.sprites = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()

		self.player = Player(self)

		# run main loop
		self.stop = False
		while not self.stop:
			self.loop()

	def save(self):
		# save settings
		with open("./settings.json", mode= "w", encoding= "utf-8") as file:
			file.write(json.dumps(self.settings, sort_keys= True, indent= 4))

	def loop(self):
		self.clock.tick(self.framerate)
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
		self.screen.fill(BLACK)
		for sprite in self.sprites:
			sprite.update_image()
		self.bullets.draw(self.screen)
		self.player.draw()
		pygame.display.flip()
