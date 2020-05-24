import pygamepp as pgp
from vars import *

from entities.base.image import Image
from entities.base.sprite import Sprite

# créer un Rect en plus de celui de l'image pour gérer les collisions
# on crée une Hitbox en passant:
# un sprite
# une position relative - ex (1 / 2, 2 / 3) placera le centre de la Hitbox à la moitié de l'image en longueur et à deux tiers en heuteur
# un coéficient qui détermine la heuteur et la longeur de la hitbox en multipliant les dimentions de l'image par le coef
# une couleur (affichage avec "H" pour le debug)

# la hitbox contient une image de rectange coloré que l'on peut afficher ne appuyant sur "H" dans le jeu (debug)

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

	# appeler cette methode si l'image à changé de dimension ou si l'on veux changer l'affichage de la hitbox
	def reset_image(self, color, width= 1):
		self.image.surface.fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(1), vec(self.image.size) - vec(2))).fill(color)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 1), vec(self.image.size) - vec(width + 3))).fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 2), vec(self.image.size) - vec(width + 4))).fill(TRANSPARENT)
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)

	# update la postition de la hitbox par rapport au sprite
	def update(self):
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)
