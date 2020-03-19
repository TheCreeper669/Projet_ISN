import pygamepp as pgp
from vars import *
import entities.base as entities

class IceSpell(entities.Entity):
	def __init__(self, game, submap, pos, owner):
		entities.Entity.__init__(self, game, submap, pos)
		self.game.groups["spells"].add(self)
		self.owner = owner
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "ice_spell.png"), (self.game.tile_size / 2, self.game.tile_size / 2)))
		self.hitbox = entities.Hitbox(self, (1 / 2, 1 / 2), (2 / 7, 2 / 7), color= RED)
		self.motion_orientation = vec(0)
		self.friction_coef = -self.game.tile_size / 256
		self.force_coef = self.game.tile_size * 4
		#max_speed = abs(self.force_coef / self.friction_coef)

	def update(self):
		self.motion_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_MOTION)
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)
		self.image.update(self.motion_orientation != vec(0), self.motion_orientation)

	def collision(self, other):
		entities.Entity.collision(self, other)
		if other is not self.owner:
			other.forces += self.vel.length() * self.mass
			self.kill()

