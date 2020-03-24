import pygamepp as pgp
from vars import *

class Sprite(pgp.pg.sprite.Sprite):
	def __init__(self, game, pos, submap= None):
		pgp.pg.sprite.Sprite.__init__(self)
		self.game = game
		self.game.groups["sprites"].add(self)
		self.submap = submap
		self.pos = vec(pos[0], pos[1])

	def update(self):
		self.image.center = self.pos

	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface, rpos)

	def find_submap(self):
		submaps = pgp.pg.sprite.spritecollide(self, self.game.groups["submaps"], dokill= False, collided= collide)
		if len(submaps) > 0:
			submaps[0].add_sprite(self)
			print("sprite {} added to {}".format(self, submaps[0]))

	def kill(self):
		if self.submap is not None:
				self.submap.remove_sprite(self)
		pgp.pg.sprite.Sprite.kill(self)
