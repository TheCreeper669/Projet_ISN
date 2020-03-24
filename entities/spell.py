import pygamepp as pgp
from vars import *
import entities.base as entities

class IceSpell(entities.Entity):
	def __init__(self, owner):
		entities.Entity.__init__(self, owner.game, owner.submap, owner.pos)
		self.game.groups["spells"].add(self)
		self.owner = owner
		self.motion_orientation = vec(self.owner.weapon_orientation)
		self.submap.add_sprite(self)
		self.image = entities.Image(
			pgp.pg.transform.rotate(
				pgp.pg.transform.scale(
					pgp.pg.image.load(DIR_IMAGE_ENTITIES + "ice_spell.png"),
					(self.game.tile_size, self.game.tile_size)
				),
				-self.motion_orientation.as_polar()[1]
			)
		)
		self.hitbox = entities.Hitbox(self, (1 / 2, 1 / 2), (2 / 7, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 256
		self.force_coef = self.game.tile_size * 512
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.vel.x = self.owner.vel.x * abs(self.motion_orientation.x)
		self.vel.y = self.owner.vel.y * abs(self.motion_orientation.y)
		self.forces += self.motion_orientation * self.force_coef
		self.minvel = 256
		self.cooldown = self.game.framerate // 4
		self.owner.weapon_cooldown = self.cooldown

	def update(self):
		entities.Entity.update(self)
		if self.vel.length() <= self.minvel:
			self.kill()

	def collide(self, other):
		entities.Entity.collide(self, other)
		if other is not self.owner and ((not hasattr(other, "owner")) or self.owner is not other.owner):
			self.attack(other)
			self.kill()

