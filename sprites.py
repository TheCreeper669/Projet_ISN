import pygame
import json
import sys
import os

from vars import *

vec2 = pygame.math.Vector2

def vec2_lq(vec, limit=1):
	return abs(vec.x) <= limit and abs(vec.y) <= limit

class Animation:
	def __init__(self, dirname, prefix="", halt=False, delay=0, reverse=False):
		self.dirname = dirname
		self.prefix = prefix
		with open(self.dirname + "animation.json", mode= "r", encoding= "utf-8") as file:
			content = json.loads(file.read())[prefix]
			self.halt_frame = content["halt"]
			self.length = content["length"]
		self.current = 0
		self.delay = delay
		self.reverse = reverse
		self.way = True
		self.halt = halt

	def change(self, prefix, halt=False):
		self.prefix = prefix
		self.current = 0
		self.halt = halt
		with open(self.dirname + "animation.json", mode= "r", encoding= "utf-8") as file:
			content = json.loads(file.read())[prefix]
			self.halt_frame = content["halt"]
			self.length = content["length"]


	def get_image(self):
		if self.halt:
			return pygame.image.load(self.dirname + self.prefix + str(self.halt_frame) + ".bmp")
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


class Player(pygame.sprite.Sprite):
	def __init__(self, game):
		# Init mother class
		pygame.sprite.Sprite.__init__(self)
		# Set game ref
		self.game = game
		# Add to groups
		game.sprites.add(self)
		# Load settings
		self.def_acc = self.game.settings["player"]["acc"]
		self.friction = self.game.settings["player"]["friction"]
		# Motion
		self.pos = vec2(self.game.width / 2, self.game.height / 2)
		self.vel = vec2(0)
		self.acc = vec2(0)
		self.motion_orientation = vec2(0)
		# Weapon
		if len(sys.argv) > 1:
			self.weapon = Weapon("./weapons/" + sys.argv[1] + ".json")
		else:
			self.weapon = Weapon("./weapons/gun.json")
		self.weapon_orientation = vec2(0)
		self.weapon_cycle = 0
		# Image
		self.halt = True
		self.last_halt = self.halt
		self.direction = "down"
		self.last_direction = self.direction
		self.animation = Animation("./img/isaac/", prefix= self.direction, halt= self.halt, delay= self.game.framerate // 2, reverse= True)
		self.update_image()

	def update(self):
		# Motion Orientation
		self.motion_orientation = vec2(0, 0)
		if self.game.keys[K_MOTION_LEFT] and not self.game.keys[K_MOTION_RIGHT]:
			self.motion_orientation.x = -1
		if self.game.keys[K_MOTION_RIGHT] and not self.game.keys[K_MOTION_LEFT]:
			self.motion_orientation.x = 1
		if self.game.keys[K_MOTION_UP] and not self.game.keys[K_MOTION_DOWN]:
			self.motion_orientation.y = -1
		if self.game.keys[K_MOTION_DOWN] and not self.game.keys[K_MOTION_UP]:
			self.motion_orientation.y = 1

		if self.motion_orientation == vec2(0, 0):
			self.halt = True
		else:
			self.halt = False

		# Motion
		self.acc = self.motion_orientation * self.def_acc 	# acc
		self.acc += self.vel * self.friction 				# friction
		self.vel += self.acc 								# vel
		self.pos += self.vel + self.acc / 2 				# pos

		# Borders
		border_width = 5
		border = border_width + self.rect.height / 2
		if self.pos.y <= border:
			self.pos.y = border
			if self.vel.y < 0:
				self.vel.y = 0
		border = self.game.height - border_width - self.rect.height / 2
		if self.pos.y >= border:
			self.pos.y = border
			if self.vel.y > 0:
				self.vel.y = 0
		border = border_width + self.rect.width / 2
		if self.pos.x <= border:
			self.pos.x = border
			if self.vel.x < 0:
				self.vel.x = 0
		border = self.game.width - border_width - self.rect.width / 2
		if self.pos.x >= border:
			self.pos.x = border
			if self.vel.x > 0:
				self.vel.x = 0

		if self.weapon_cycle > 0:
			self.weapon_cycle += 1
		if self.weapon_cycle >= self.weapon.loading:
			self.weapon_cycle = 0
		if self.weapon_cycle == 0:
			# Weapon Orientation
			self.weapon_orientation = vec2(0)
			if self.game.keys[K_WEAPON_LEFT] and not self.game.keys[K_WEAPON_RIGHT]:
				self.weapon_orientation.x = -1
			if self.game.keys[K_WEAPON_RIGHT] and not self.game.keys[K_WEAPON_LEFT]:
				self.weapon_orientation.x = 1
			if self.game.keys[K_WEAPON_UP] and not self.game.keys[K_WEAPON_DOWN]:
				self.weapon_orientation.y = -1
			if self.game.keys[K_WEAPON_DOWN] and not self.game.keys[K_WEAPON_UP]:
				self.weapon_orientation.y = 1

			# Shoot
			if self.weapon_orientation != vec2(0):
				self.weapon_cycle = 1
				Bullet(self.game, self.weapon, vec2(self.pos), self.weapon_orientation)

	def update_image(self):
		if self.motion_orientation.x != 0:
			if self.motion_orientation.x == 1:
				self.direction = "right"
			else:
				self.direction = "left"
		elif self.motion_orientation.y != 0:
			if self.motion_orientation.y == -1:
				self.direction = "up"
			else:
				self.direction = "down"

		if self.direction != self.last_direction or self.halt != self.last_halt:
			self.animation.change(self.direction, self.halt)

		self.last_halt = self.halt
		self.last_direction = self.direction

		self.image = self.animation.get_image()
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def draw(self):
		self.game.screen.blit(self.image, self.rect)

class Weapon:
	def __init__(self, filename):
		# read file
		content = {}
		with open(filename, mode= "r", encoding= "utf-8") as file:
			content = json.loads(file.read())
		self.vel = content["vel"]
		self.friction = content["friction"]
		self.loading = content["loading"]
		self.name = content["name"]
		self.image = content["image"]


class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, weapon, pos, orientation):
		# init mother class
		pygame.sprite.Sprite.__init__(self)
		# set ref to game
		self.game = game
		# Set ref to weapon
		self.weapon = weapon
		# add self to groups
		self.game.sprites.add(self)
		self.game.bullets.add(self)
		# set pos and motion
		self.pos = pos
		self.vel = self.weapon.vel * orientation
		self.acc = vec2(0)
		self.friction = self.weapon.friction
		# Image
		self.update_image()

	def update(self):
		# Motion
		self.acc = vec2(0)
		self.acc += self.vel * self.friction 	# friction
		self.vel += self.acc 					# vel
		self.pos += self.vel + self.acc / 2 	# pos

		# Borders
		border_width = 5
		border = border_width + self.rect.height / 2
		if self.pos.y <= border:
			self.kill()
		border = self.game.height - border_width - self.rect.height / 2
		if self.pos.y >= border:
			self.kill()
		border = border_width + self.rect.width / 2
		if self.pos.x <= border:
			self.kill()
		border = self.game.width - border_width - self.rect.width / 2
		if self.pos.x >= border:
			self.kill()

		# Too slow
		if vec2_lq(self.vel):
			self.kill()

	def update_image(self):
		if self.weapon.image["type"] == "rect":
			self.image = pygame.Surface(self.weapon.image["dim"])
			self.image.fill(self.weapon.image["color"])
		self.rect = self.image.get_rect()
		self.rect.center = self.pos