import pygamepp as pgp
from vars import *

from entities.base.util import collide
from entities.base.sprite import Sprite
from entities.base.display import Display

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
		# bools
		self.movable = True

	def update(self):
		self.forces += self.vel * self.friction_coef * self.mass
		self.acc = self.forces / self.mass
		self.vel += self.acc * self.game.dt
		self.pos += self.vel * self.game.dt
		self.forces = vec(0)
		self.update_pos()
		self.life_display = Display(self.game, self.life, self.life_display_color, self.pos)
		if self.life <= 0:
			self.kill()

	def update_pos(self):
		self.image.center = self.pos + self.hitbox.rcenter
		self.hitbox.update()

	def draw(self, surface, rpos= vec(0)):
		Sprite.draw(self, surface, rpos)
		if self.game.draw_hitbox:
			self.hitbox.draw(surface, rpos)

	def find_submap(self):
		submaps = pgp.pg.sprite.spritecollide(self, self.game.groups["submaps"], dokill= False, collided= collide)
		if len(submaps) > 0:
			submaps[0].add_sprite(self)

	def collide(self, other):
		if other.movable:
			#print("{} collide {}".format(type(self).__name__, type(other).__name__))
			from_other = (self.pos - other.pos) * other.mass * self.game.tile_size
			#print(from_other)
			self.forces += from_other
		else:
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
				abs(posdiff.x) > abs(posdiff.y),
				abs(posdiff.y) > abs(posdiff.x)
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

	def attack(self, other):
		if other.movable:
			other.forces += self.vel * self.mass
			other.life -= 1


