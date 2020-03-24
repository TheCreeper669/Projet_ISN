import pygamepp as pgp
from vars import *

from entities.base.image import Image
from entities.base.sprite import Sprite

class Display(Sprite):
	def __init__(self, game, content, color, pos, font= None):
		Sprite.__init__(self, game, pos)
		self.game.groups["displays"].add(self)
		self.font = font
		if self.font is None:
			self.font = self.game.font
		self.content = content
		self.color = color
		if isinstance(self.content, type(lambda: None)):
			self.image = Image(self.font.render(self.content(self.game), True, self.color))
		else:
			self.image = Image(self.font.render(str(self.content), True, self.color))
		self.image.topleft = self.pos

	def update(self, pos= None, content= None):
		if pos is not None:
			self.pos = pos
		if content is not None:
			self.content = content
		if isinstance(self.content, type(lambda: None)):
			self.image.reset_surface(self.font.render(self.content(self.game), True, self.color))
		else:
			self.image = Image(self.font.render(str(self.content), True, self.color))
		self.image.topleft = self.pos

class FixDisplay(Display):
	def __init__(self, game, content, color, pos, font= None):
		Display.__init__(self, game, content, color, pos, font)
		self.game.groups["fix_displays"].add(self)

	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface)
