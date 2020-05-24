import pygamepp as pgp
from vars import *

from entities.base.sprite import Sprite

# permet de créer un obstacle comme un mur
# class virtuelle
# la hitbox et l'image doivent être définies dans la class fille

class Obstacle(Sprite):
	def __init__(self, game, submap, pos):
		Sprite.__init__(self, game, pos, submap)
		self.game.groups["obstacles"].add(self)
		self.movable = False

	# update l'image et la hitbox
	def update(self):
		self.image.center = self.pos + self.hitbox.rcenter
		self.hitbox.update()

	# draw l'image et la hitbox si demandé par le jeu
	def draw(self, surface, rpos= vec(0)):
		Sprite.draw(self, surface, rpos)
		if self.game.draw_hitbox:
			self.hitbox.draw(surface, rpos)

	# implémente la collison pour que le joueur puisse rentrer en collision avec
	# toutefois cette fonction est vide car les obstacles ne subbisent pas les collision
	def collide(self, other):
		pass
