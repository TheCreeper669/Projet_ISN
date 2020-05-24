import pygamepp as pgp
from vars import *

from entities.base.util import collide
from entities.base.sprite import Sprite
from entities.base.display import Display

# entitées
# class virtuelles
# contient:
# un Sprite
# une nombre vies
# un display de sa vie
# une hitbox
# des verteurs de déplacement (forces, accélération, vitesse et position)
# des constantes physiques (friction, masse)

# l'image et la hitbox doivent être implémenté dans la class fille

class Entity(Sprite):
	def __init__(self, game, submap, pos, team):
		Sprite.__init__(self, game, pos, submap)
		self.game.groups["entities"].add(self)
		self.team = team
		self.team.add(self)
		self.acc = vec(0)
		self.vel = vec(0)
		self.friction_coef = 0
		self.forces = vec(0)
		self.mass = 1
		self.life = 1
		self.life_display_color = WHITE
		self.life_display = Display(self.game, self.life, self.life_display_color, self.pos)
		self.damage = 1
		# bools
		self.movable = True

	# update la possition en fonction de la vitesse et des forces qui s'appliques sur l'entitée
	# le modèle physique n'est pas strictement fidèle à la réalité ni même au équations newtoniennes
	# elles les approches de mieux en mieux si les fps sont élévés
	def update(self):
		# update position
		self.forces += self.vel * self.friction_coef * self.mass	# ajoute la force de friction
		self.acc = self.forces / self.mass							# calcule l'accelération en fonction des forces et de la masse
		self.vel += self.acc * self.game.dt							# calcule la vittesse en fonction du temps écoulé depuis la dernière frame
		self.pos += self.vel * self.game.dt							# calcule la position en fonction du temps écoulé depuis la dernière frame
		self.forces = vec(0)										# remet les forces à (0, 0)
		self.update_pos()											# actualise l'image
		# update life
		self.life_display = Display(self.game, self.life, self.life_display_color, self.pos)
		if self.life <= 0:
			self.kill()

	# remet la possition de l'image et de la hitbox par rappot à self.pos
	def update_pos(self):
		self.image.center = self.pos + self.hitbox.rcenter
		self.hitbox.update()

	# draw l'image et la hitbox si le jeu le demande
	def draw(self, surface, rpos= vec(0)):
		Sprite.draw(self, surface, rpos)
		if self.game.draw_hitbox:
			self.hitbox.draw(surface, rpos)

	# gère les collisions entre entitées et entitées ainsi qu'entre entitées et obstacles
	def collide(self, other):
		if other.movable: # entitées et entitées
			# applique une force sur les entitées pour les repouser

			#print("{} collide {}".format(type(self).__name__, type(other).__name__))
			from_other = (self.pos - other.pos) * other.mass * self.game.tile_size
			#print(from_other)
			self.forces += from_other
		else: # entitées et obstacles
			# repostitione l'entité en dehors de l'obstacle

			posdiff = other.pos - self.pos
			#print("posdiff {}".format(posdiff))
			diff = vec(0)
			if posdiff.x >= 0:
				diff.x = posdiff.x - (other.hitbox.image.size[0] + self.hitbox.image.size[0]) / 2
			else:
				diff.x = posdiff.x + (other.hitbox.image.size[0] + self.hitbox.image.size[0]) / 2
			if posdiff.y >= 0:
				diff.y = posdiff.y - (other.hitbox.image.size[1] + self.hitbox.image.size[1]) / 2
			else:
				diff.y = posdiff.y + (other.hitbox.image.size[1] + self.hitbox.image.size[1]) / 2
			#print("diff {}".format(diff))
			valid = vec(
				abs(diff.x) <= abs(diff.y),
				abs(diff.y) < abs(diff.x)
			)
			#print("valid {}".format(valid))
			if valid.x and not valid.y:
				#print("x", end= "")
				if self.vel.x * diff.x < 0:
					self.vel.x = 0
				if self.acc.x * diff.x < 0:
					self.acc.x = 0
				self.pos.x += diff.x + (posdiff.x >= 0)
			if valid.y and not valid.x:
				#print("y", end= "")
				if self.vel.y * diff.y < 0:
					self.vel.y = 0
				if self.acc.y * diff.y < 0:
					self.acc.y = 0
				self.pos.y += diff.y + (posdiff.y >= 0)
			#print()
			self.update_pos()

	# attaque une autre entitées
	# lui enlève de la vie et la pousse
	def attack(self, other):
		if other.movable:
			other.forces += self.vel * self.mass
			self.forces -= self.vel * self.mass
			other.life -= self.damage


