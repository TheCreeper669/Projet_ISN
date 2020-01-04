import pygame
import json
import sys
import os
from math import sqrt

from vars import *
from func import *

class Display(pygame.sprite.Sprite):
	def __init__(self, game, func, color, pos):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.game.sprites.add(self)
		self.game.displays.add(self)
		self.func = func
		self.color = color
		self.pos = pos
		self.image = self.game.font.render(self.func(self.game), True, self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos

	def update(self):
		self.image = self.game.font.render(self.func(self.game), True, self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos

class Tile(pygame.sprite.Sprite):
	def __init__(self, game, dim, pos, color):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.game.sprites.add(self)
		self.game.tiles.add(self)
		if color == GREEN:
			self.game.obstacles.add(self)
		self.image = pygame.Surface(dim)
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.topleft = pos

	def update(self):
		pass

def get_tiles(game, dim, pos, tile_dim, space, map):
	for y in range(int(dim[1])):
		for x in range(int(dim[0])):
			if len(map) > y and len(map[y]) > x and type(map[y][x]) == type((0, 0, 0)):
				game.tiles.add(Tile(game, tile_dim, pos + vec2(tile_dim.x * x + space * x, tile_dim.y * y + space * y), map[y][x]))
			else:
				game.tiles.add(Tile(game, tile_dim, pos + vec2(tile_dim.x * x + space * x, tile_dim.y * y + space * y), BLUE))

class Player(pygame.sprite.Sprite):
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		# Set game ref
		self.game = game
		# Add to groups
		game.sprites.add(self)
		# Load json
		self.name = self.game.settings["player_name"]
		content = load_json(DIR_PLAYERS + self.name + "/info.json")
		self.def_acc = content["acc"]
		self.friction = content["friction"]
		self.weapon = Weapon(content["weapon"])
		# Motion
		self.pos = vec2(self.game.width / 2, self.game.height / 2)
		self.vel = vec2(0)
		self.acc = vec2(0)
		# Orientation
		self.motion_orientation = vec2(0)
		self.weapon_orientation = vec2(0)
		# Bool
		self.moving = False
		self.moving_x = False
		self.moving_y = False
		self.shooting = False
		self.firing = False
		# Image
		self.image = pygame.Surface((64, 64))
		self.image.fill(RED)
		self.rect = self.image.get_rect()

	def update(self):
		# Orientation
		self.motion_orientation = get_orientation(self.game.keys, *K_MOTION)
		self.weapon_orientation = get_orientation(self.game.keys, *K_WEAPON)

		# Bool
		self.moving_x = False
		if self.motion_orientation.x != 0:
			self.moving_x = True

		self.moving_y = False
		if self.motion_orientation.y != 0:
			self.moving_y = True

		self.moving = self.moving_x or self.moving_y
		
		self.shooting = False
		if self.weapon_orientation != vec2(0):
			self.shooting = True

		# Motion
		self.acc = self.motion_orientation * self.def_acc * self.game.last_tick
		self.acc += self.vel * self.friction
		self.vel += self.acc
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0
		if abs(self.vel.y) < 0.1:
			self.vel.y = 0
		self.pos += self.vel + self.acc / 2

		# Borders
		border_width = 5
		border = border_width + self.rect.height / 2
		if self.pos.y <= border:
			self.pos.y = border
			if self.vel.y < 0:
				self.vel.y = 0
		border = self.game.rect.height - border_width - self.rect.height / 2
		if self.pos.y >= border:
			self.pos.y = border
			if self.vel.y > 0:
				self.vel.y = 0
		border = border_width + self.rect.width / 2
		if self.pos.x <= border:
			self.pos.x = border
			if self.vel.x < 0:
				self.vel.x = 0
		border = self.game.rect.width - border_width - self.rect.width / 2
		if self.pos.x >= border:
			self.pos.x = border
			if self.vel.x > 0:
				self.vel.x = 0

		self.rect.center = self.pos

		obstacles_list = pygame.sprite.spritecollide(self, self.game.obstacles, False)
		for obstacle in obstacles_list:
			diff = vec2(obstacle.rect.center) - vec2(self.rect.center)
			if abs(diff.x) >= abs(diff.y):
				self.rect.x += diff.x
				if diff.x >= 0:
					self.rect.right = obstacle.rect.left
					if self.vel.x > 0:
						self.vel.x = 0
				else:
					self.rect.left = obstacle.rect.right
					if self.vel.x < 0:
						self.vel.x = 0
			else:
				if diff.y >= 0:
					self.rect.bottom = obstacle.rect.top
					if self.vel.y > 0:
						self.vel.y = 0
				else:
					self.rect.top = obstacle.rect.bottom
					if self.vel.y < 0:
						self.vel.y = 0

		self.pos = vec2(self.rect.center)

		"""
		# Weapon
		if self.weapon_cycle > 0:
			self.weapon_cycle += 1
		if self.weapon_cycle >= self.weapon.loading:
			self.weapon_cycle = 0
		if self.weapon_cycle == 0 and self.weapon_orientation != vec2(0):
			self.weapon_cycle = 1
			Bullet(self.game, self.weapon, vec2(self.pos), self.weapon_orientation)

		# Image
		if self.weapon_orientation == vec2(0):
			self.direction = get_direction(self.motion_orientation)
		else:
			self.direction = get_direction(self.weapon_orientation)

		if self.direction != self.last_direction or self.halt != self.last_halt:
			self.animation.change(self.direction, self.halt)

		self.last_direction = self.direction
		"""

	def draw(self, surface):
		surface.blit(self.image, self.rect)


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

	def draw(self):
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

		# Image
		if self.weapon.image["type"] == "rect":
			self.image = pygame.Surface(self.weapon.image["dim"])
			self.image.fill(self.weapon.image["color"])
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.game.window.blit(self.image, self.rect)