import pygamepp as pgp
from vars import *
import entities.base as entities

class Display(entities.Sprite):
	def __init__(self, game, content, color, pos):
		entities.Sprite.__init__(self, game, pos)
		self.game.groups["displays"].add(self)
		self.content = content
		self.color = color
		if isinstance(self.content, type(lambda: None)):
			self.image = entities.Image(self.game.font.render(self.content(self.game), True, self.color))
		else:
			self.image = entities.Image(self.game.font.render(str(self.content), True, self.color))
		self.image.topleft = self.pos

	def update(self, pos= None, content= None):
		if pos is not None:
			self.pos = pos
		if content is not None:
			self.content = content
		if isinstance(self.content, type(lambda: None)):
			self.image.reset_surface(self.game.font.render(self.content(self.game), True, self.color))
		else:
			self.image = entities.Image(self.game.font.render(str(self.content), True, self.color))
		self.image.topleft = self.pos

class FixDisplay(Display):
	def __init__(self, game, content, color, pos):
		Display.__init__(self, game, content, color, pos)
		self.game.groups["fix_displays"].add(self)

	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface)
