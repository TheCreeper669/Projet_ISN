import pygamepp as pgp
from vars import *

from entities.base.sprite import Sprite

class Obstacle(Sprite):
	def __init__(self, game, submap, pos):
		Sprite.__init__(self, game, pos, submap)
		self.game.groups["obstacles"].add(self)
		self.movable = False

	def update(self):
		self.image.center = self.pos + self.hitbox.rcenter
		self.hitbox.update()

	def draw(self, surface, rpos= vec(0)):
		Sprite.draw(self, surface, rpos)
		if self.game.draw_hitbox:
			self.hitbox.draw(surface, rpos)

	def collide(self, other):
		pass
