import pygamepp as pgp
from vars import *
from .util import collide

# un sprite contient:
# un sprite pygame
# une position
# une image

# c'est une class virtuelle
# elle ne sert que de base pour les autres class sprites
# l'image doit être créé dans la class fille

class Sprite(pgp.pg.sprite.Sprite):
	def __init__(self, game, pos, submap= None):
		pgp.pg.sprite.Sprite.__init__(self)
		self.game = game
		self.game.groups["sprites"].add(self)
		self.submap = submap
		self.pos = vec(pos[0], pos[1])

	# update la postion de l'image par rapport à self.pos
	def update(self):
		self.image.center = self.pos

	# demande de draw à l'image
	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface, rpos)

	# retrouve une nouvelle sous carte
	def find_submap(self):
		submaps = pgp.pg.sprite.spritecollide(self, self.game.groups["submaps"], dokill= False, collided= collide)
		if len(submaps) > 0:
			submaps[0].add_sprite(self)
			#print("sprite {} added to {} | pos: {}".format(type(self).__name__, submaps[0], self.pos.elementwise() / self.game.tile_size))

	# détruit le sprite
	def kill(self):
		if self.submap is not None:
				self.submap.remove_sprite(self)
		pgp.pg.sprite.Sprite.kill(self)
