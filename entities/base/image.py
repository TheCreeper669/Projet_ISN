import pygamepp as pgp
from vars import *

# gère l'image et quelques transformations d'images
# se créer à partire d'une surface et contient automatiquement le Rect de cette surface

class Image(pgp.pg.Rect):
	def __init__(self, surface):
		self.surface = surface
		pgp.pg.Rect.__init__(self, self.surface.get_rect())
		self.rpos_rect = pgp.pg.Rect(self.center, self.size)
		self.reset_surface(surface)

	# change la surface de l'image
	def reset_surface(self, surface):
		self.surface = surface
		self.size = self.surface.get_rect().size
		self.rpos_rect.size = self.size

	# resize l'image
	def scale(self, w, h):
		self.reset_surface(pgp.pg.transform.scale(self.surface, (w, h)))

	# resize la largeur
	def set_width(self, w):
		self.scale(w, self.h * w // self.w)

	# resize la hauteur
	def set_height(self, h):
		self.scale(h, self.w * h // self.h)

	# resize depuis un tuple
	def set_size(self, size):
		self.scale(*size)

	# créer un rectangle plein de x réplique de l'image en longueur et y répliques en hauteur
	def stack(self, size):
		surface = pgp.pg.Surface(vec_mul(vec(self.size), vec(size)), flags= pgp.pg.SRCALPHA)
		rect = pgp.pg.Rect(self)
		for i in range(int(size[0])):
			for j in range(int(size[1])):
				rect.topleft = i * self.size[0], j * self.size[1]
				surface.blit(self.surface, rect)
		self.reset_surface(surface)

	# créer un copie de l'image
	def copy(self):
		return type(self)(self.surface.copy())

	# draw l'image sur une surface (avec une position relative)
	def draw(self, surface, rpos= vec(0)):
		self.rpos_rect.center = vec(self.center) - rpos
		surface.blit(self.surface, self.rpos_rect)
