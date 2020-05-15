import pygamepp as pgp
from vars import *

import entities.base as entities

class Spider(entities.Entity):
	def __init__(self, game, submap, pos):
		entities.Entity.__init__(self, game, submap, pos, game.groups["team_mobs"])
		self.game.groups["mobs"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "spider/", (self.game.tile_size * 3 / 2, self.game.tile_size * 3 / 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 3 / 5), (3 / 5, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 8
		self.force_coef = -self.friction_coef * self.game.tile_size * 2
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.follow_range = self.game.tile_size * 16
		self.attack_range = self.game.tile_size * 1.5
		self.attacking = False
		self.moving = False
		self.target = None
		self.life = 3
		self.life_display_color = RED

	def update(self):
		self.attacking = False
		self.traget = None
		to_target = vec(0)
		len_to_target = float("+inf")
		for player in self.game.groups["players"]:
			to_player = player.pos - self.pos
			len_to_player = to_player.length()
			if len_to_player <= self.attack_range:
				self.target = player
				self.attacking = True
				self.target = player
				break
			elif len_to_player <= self.follow_range and len_to_player < len_to_target and to_player != vec(0):
				self.target = player
				to_target = to_player
				len_to_target = len_to_player
		self.moving = self.target is not None and not self.attacking
		if self.moving and to_target.length() != 0:
			to_target.scale_to_length(self.force_coef)
			self.forces += to_target
		entities.Entity.update(self)
		self.life_display.update(self.pos, self.life)
		self.image.update(True, [self.moving, self.attacking])
		if self.attacking and self.image.counter == 0:
			self.attack(self.target)

	def collide(self, other):
		entities.Entity.collide(self, other)

	def attack(self, other):
		print("{} attacks {}".format(type(self).__name__, type(other).__name__))
		entities.Entity.attack(self, other)

	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)



