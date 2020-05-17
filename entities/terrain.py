import pygamepp as pgp
from vars import *

import entities.base as entities



class FakeWall(entities.Sprite):
	def __init__(self, game, pos, submap):
		entities.Sprite.__init__(self, game, pos, submap)
		self.game.groups["fakewalls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_SPRITES + "fakewall.png"), (self.game.tile_size, self.game.tile_size)))



class Wall(entities.Obstacle):
	def __init__(self, game, submap, pos):
		entities.Obstacle.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall.png"), (self.game.tile_size, self.game.tile_size)))
		self.hitbox = entities.Hitbox(self, color= BLUE)

		for obstacle in self.submap.obstacles:
			if obstacle.pos.x == self.pos.x:
				pass
			elif obstacle.pos.y == self.pos.y:
				pass

class BigWall(entities.Obstacle):
	def __init__(self, game, submap, pos, size= vec(1, 1)):
		entities.Obstacle.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall.png"), (self.game.tile_size, self.game.tile_size)))
		self.image.stack(size)
		self.hitbox = entities.Hitbox(self, color= BLUE)


