import pygamepp as pgp
from vars import *
import entities.base as entities

class Player(entities.Entity):
	def __init__(self, game, submap, pos= vec(0)):
		entities.Entity.__init__(self, game, submap, pos)
		self.game.groups["players"].add(self)
		self.game.player = self
		#self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "player.png"), (TILE_SIZE * 2, TILE_SIZE * 2)))
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "player/", (TILE_SIZE * 2, TILE_SIZE * 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 4 / 5), (2 / 5, 2 / 5), color= RED)
		self.motion_orientation = vec(0)
		self.friction_coef = -8
		self.force_coef = -self.friction_coef * 256
		#max_speed = abs(self.force_coef / self.friction_coef)

	def update(self):
		self.motion_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_MOTION)
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)
		self.image.update(self.motion_orientation != vec(0), self.motion_orientation)


