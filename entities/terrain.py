import pygamepp as pgp
from vars import *
import entities.base as entities



class FakeWall(entities.Sprite):
	def __init__(self, game, pos= vec(0), submap= None):
		entities.Sprite.__init__(self, game, pos, submap)
		self.game.groups["fakewalls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_SPRITES + "fakewall.png"), (TILE_SIZE, TILE_SIZE)))



class Stationary(entities.Entity):
	def __init__(self, game, submap, pos= vec(0)):
		entities.Entity.__init__(self, game, submap, pos)
		self.game.groups["stationaries"].add(self)
		self.movable = False

class Wall(Stationary):
	def __init__(self, game, submap, pos= vec(0)):
		Stationary.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall.png"), (TILE_SIZE, TILE_SIZE)))
		self.hitbox = entities.Hitbox(self, color= BLUE)

class BigWall(Stationary):
	def __init__(self, game, submap, pos= vec(0), size= vec(1, 1)):
		Stationary.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall.png"), (TILE_SIZE, TILE_SIZE)))
		self.image.stack(size)
		self.hitbox = entities.Hitbox(self, color= BLUE)


