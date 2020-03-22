import pygamepp as pgp
from vars import *
import entities.base as entities

class IceSpell(entities.Entity):
	def __init__(self, owner):
		entities.Entity.__init__(self, owner.game, owner.submap, owner.pos)
		self.game.groups["spells"].add(self)
		self.owner = owner
		self.motion_orientation = vec(self.owner.weapon_orientation)
		self.submap.add_entity(self)
		self.image = entities.Image(
			pgp.pg.transform.rotate(
				pgp.pg.transform.scale(
					pgp.pg.image.load(DIR_IMAGE_ENTITIES + "ice_spell.png"),
					(self.game.tile_size * 2 // 3, self.game.tile_size * 2 // 3)
				),
				self.motion_orientation.as_polar()[1]
			)
		)
		self.hitbox = entities.Hitbox(self, (1 / 2, 1 / 2), (2 / 7, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 256
		self.force_coef = self.game.tile_size * 16
		#max_speed = abs(self.force_coef / self.friction_coef)

	def update(self):
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)

	def collide(self, other):
		entities.Entity.collide(self, other)
		if other is not self.owner:
			self.attack(other)
			if self.submap is not None:
				self.submap.remove_entity(self)

