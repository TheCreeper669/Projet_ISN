import pygamepp as pgp
from vars import *

import entities.base as entities


class Follower(entities.Entity):
	def __init__(self, game, submap, pos):
		entities.Entity.__init__(self, game, submap, pos, game.groups["team_mobs"])
		self.game.groups["mobs"].add(self)
		self.game.groups["followers"].add(self)
		self.moving = False
		self.attacking = False
		self.target = None
		self.follow_group = self.game.groups["players"]

	def update(self):
		self.attacking = False
		self.traget = None
		to_target = vec(0)
		len_to_target = float("+inf")
		for player in self.follow_group:
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


class Spider(Follower):
	def __init__(self, game, submap, pos):
		Follower.__init__(self, game, submap, pos)
		self.game.groups["mobs"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "spider/", (self.game.tile_size * 3 / 2, self.game.tile_size * 3 / 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 3 / 5), (3 / 5, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 8
		self.force_coef = -self.friction_coef * self.game.tile_size * 2
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.follow_range = self.game.tile_size * 16
		self.attack_range = self.game.tile_size * 1.5
		self.life = 3
		self.life_display_color = RED
		self.sound_death = pgp.pg.mixer.Sound(DIR_SOUNDS + "death_spider.wav")
		self.sound_death.set_volume(self.game.volume * 1 / 3)
		self.update_pos()

	def update(self):
		Follower.update(self)
		self.life_display.update(self.pos, self.life)
		self.image.update(True, [self.moving, self.attacking])
		if self.attacking and self.image.counter == 0:
			self.attack(self.target)

	def attack(self, other):
		print("{} attacks {}".format(type(self).__name__, type(other).__name__))
		entities.Entity.attack(self, other)

	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)

	def kill(self):
		self.sound_death.play()
		Follower.kill(self)



class Boss(Follower):
	def __init__(self, game, submap, pos):
		Follower.__init__(self, game, submap, pos)
		self.game.groups["mobs"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "boss/", (self.game.tile_size * 8, self.game.tile_size * 8))
		self.hitbox = entities.Hitbox(self, (1 / 2, 2 / 3), (1 / 7, 1 / 5), color= RED)
		self.friction_coef = -self.game.tile_size / 4
		self.force_coef = -self.friction_coef * self.game.tile_size
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.follow_range = self.game.tile_size * 32
		self.attack_range = self.game.tile_size * 2
		self.damage = 2
		self.life = 32
		self.life_display_color = RED
		self.sound_hit_hard = pgp.pg.mixer.Sound(DIR_SOUNDS + "boss_hard_hit.flac")
		self.sound_hit_hard.set_volume(self.game.volume * 2 / 3)
		self.sound_hit_soft = pgp.pg.mixer.Sound(DIR_SOUNDS + "boss_soft_hit.flac")
		self.sound_hit_soft.set_volume(self.game.volume * 2 / 3)
		self.sound_death = pgp.pg.mixer.Sound(DIR_SOUNDS + "death_boss.wav")
		self.update_pos()

	def update(self):
		Follower.update(self)
		self.life_display.update(self.pos, self.life)
		self.image.update(True, [self.moving, self.attacking])
		if self.image.counter % self.image.step == 0:
			if self.image.counter // self.image.step == 2:
				if self.attacking:
					self.attack(self.target)
				else:
					self.sound_hit_soft.play()

	def attack(self, other):
		self.sound_hit_hard.play()
		print("{} attacks {}".format(type(self).__name__, type(other).__name__))
		entities.Entity.attack(self, other)

	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)

	def kill(self):
		self.sound_death.play()
		for y in range(3):
			for x in range(y + 1):
				new_sipder = Spider(self.game, self.submap, self.pos + vec(x, y) * self.game.tile_size)
				self.submap.add_sprite(new_sipder)
		Follower.kill(self)


