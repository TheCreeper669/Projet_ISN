import pygame
import json

from vars import *

vec2 = pygame.math.Vector2

def vec2_lq(vec, limit=1):
	return abs(vec.x) <= limit and abs(vec.y) <= limit

def load_json(string):
	with open(string, mode= "r", encoding= "utf-8") as file:
		return json.loads(file.read())

def get_orientation(keys, key_up, key_down, key_left, key_right):
	orientation = vec2(0)
	if keys[key_left] and not keys[key_right]:
		orientation.x = -1
	if keys[key_right] and not keys[key_left]:
		orientation.x = 1
	if keys[key_up] and not keys[key_down]:
		orientation.y = -1
	if keys[key_down] and not keys[key_up]:
		orientation.y = 1
	return orientation

def get_direction(orientation):
	if orientation.x != 0:
		if orientation.x == 1:
			return "right"
		else:
			return "left"
	elif orientation.y != 0:
		if orientation.y == -1:
			return "up"
		else:
			return "down"

class Animation:
	def __init__(self, dirname, delay=1, reverse=False, prefix=""):
		self.dirname = dirname
		self.prefix = prefix
		self.info = load_json(self.dirname + "animation.json")
		self.length = self.json[self.prefix]
		self.current = 0
		self.delay = delay
		self.reverse = reverse
		self.way = True

	def change(self, prefix):
		self.prefix = prefix
		self.length = self.info[self.prefix]
		self.current = 0

	def get_image(self):
		if self.way:
			if self.current == self.length * self.delay - 1:
				if self.reverse:
					self.way = False
					self.current -= 1
				else:
					self.current = -1
			self.current += 1
		else:
			if self.current == 0:
				self.way = True
				self.current += 1
			self.current -= 1
		return pygame.image.load(self.dirname + self.prefix + str(self.current // self.delay) + ".bmp")

class SingleAnimation:
	def __init__(self, dirname, prefix=""):
		self.dirname = dirname
		self.prefix = prefix

	def change(self, prefix):
		self.prefix = prefix

	def get_image(self):
		return pygame.image.load(self.dirname + self.prefix + ".bmp")

class Weapon:
	def __init__(self, name):
		self.name = name
		# read file
		content = {}
		with open(DIR_WEAPONS + self.name + ".json", mode= "r", encoding= "utf-8") as file:
			content = json.loads(file.read())
		self.vel = content["vel"]
		self.friction = content["friction"]
		self.loading = content["loading"]
		self.image = content["image"]





