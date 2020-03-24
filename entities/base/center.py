import pygamepp as pgp
from vars import *

from entities.base.image import Image
from entities.base.sprite import Sprite

class Center(Sprite):
	def __init__(self, sprite, color= RED):
		Sprite.__init__(self, sprite.game)
		self.sprite = sprite
		self.game.groups["centers"].add(self)
		width = 4
		self.image = Image(pgp.pg.Surface(vec(width)))
		self.image.surface.fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(1), vec(width - 2))).fill(color)

	def update(self):
		self.image.center = self.sprite.pos
