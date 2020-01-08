import pygame as pg
from pygame.math import Vector2 as vec

class Image:
	def __init__(self, surface):
		self.surface = surface
		self.rect = self.surface.get_rect()

	def draw(surface, pos):
		self.surface.rect.center = pos
		surface.blit(self.surface, self.rect)

class Entity(pg.sprite.Sprite):
	def __init__(self, game, image, pos= vec(0), hitbox= None):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = image
		if self.hitbox is None:
			self.hitbox = self.image.rect
			self.customHitbox = True
		else:
			self.hitbox = hitbox
			self.customHitbox = False
		self.pos = pos
		self.hitbox.center = self.pos
		self.acc = vec(0)
		self.vel = vec(0)
		self.friction = 0
		self.forces = vec(0)
		self.mass = 1
		self.motion_orientation = vec(0)

	def update(self):
		self.forces = vec(0)
		# collisions
		
		self.acc = self.forces / self.mass
		self.acc += self.vel * self.friction # to verify
		self.vel += self.acc
		self.pos += (self.vel + self.acc ** 2 / 2) * self.game.last_tick
		self.hitbox.center = self.pos

	def draw(self, surface):
		self.image.draw(surface, self.pos)