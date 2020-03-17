import pygamepp as pgp
from vars import *
import entities.base as entities

class Spider(entities.Entity):
	def __init__(self, game, submap, pos= vec(0)):
		entities.Entity.__init__(self, game, submap, pos)
		self.game.groups["mobs"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "spider/", (self.game.tile_size * 2, self.game.tile_size * 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 4 / 5), (2 / 5, 2 / 5), color= RED)
		self.motion_orientation = vec(0)
		self.friction_coef = -8
		self.force_coef = -self.friction_coef * 256
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.attack = False

	def update(self):
		self.motion_orientation = vec(0)
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)
		self.image.update(True, [self.motion_orientation != vec(0), self.attack])


