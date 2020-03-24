import pygamepp as pgp
from vars import *

from entities.base.image import Image
from entities.base.sprite import Sprite

class Hitbox(Sprite):
	def __init__(self, sprite, rpos= (1 / 2, 1 / 2), coef= (1, 1), color= RED):
		Sprite.__init__(self, sprite.game, vec(0))
		self.sprite = sprite
		self.game.groups["hitboxs"].add(self)
		self.rpos = vec(rpos)
		self.coef = vec(coef)
		self.image = Image(pgp.pg.Surface((self.sprite.image.size[0] * self.coef.x, self.sprite.image.size[1] * self.coef.y), flags= pgp.pg.SRCALPHA))
		self.reset_image(color)
		self.rcenter = vec(self.sprite.image.center) - vec(self.image.center)

	def reset_image(self, color, width= 1):
		self.image.surface.fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(1), vec(self.image.size) - vec(2))).fill(color)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 1), vec(self.image.size) - vec(width + 3))).fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 2), vec(self.image.size) - vec(width + 4))).fill(TRANSPARENT)
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)

	def update(self):
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)
