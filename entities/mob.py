import pygamepp as pgp
from vars import *

import entities.base as entities

# regroupe les entitées hostiles


# class virtuelle
# créer un mob qui suit le joueur (ou un autre groupe de sprites)
# va tout droit même si il fonce dans un mur
# la class fille doit implémenter une range de poursuite et une range d'attaque
class Follower(entities.Entity):
	def __init__(self, game, submap, pos):
		entities.Entity.__init__(self, game, submap, pos, game.groups["team_mobs"])
		self.game.groups["mobs"].add(self)
		self.game.groups["followers"].add(self)
		self.moving = False # les follower est dans la range de poursuite
		self.attacking = False # les follower est dans la range d'attaque
		self.target = None # le sprite que suit actuelement le follower
		self.follow_group = self.game.groups["players"] # le groupe de sprites à suivre (par défaut les joueurs)

	# suit les sprites du groupe self.follow_group
	# suit le sprite le splus proche de ce groupe si il est dans la range de poursuite
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



# mob de base
# petite arraigné à trois pattes qui suit le joueur et lui inflige des dégats au corp à corp
class Spider(Follower):
	def __init__(self, game, submap, pos):
		Follower.__init__(self, game, submap, pos)
		self.game.groups["mobs"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "spider/", (self.game.tile_size * 3 / 2, self.game.tile_size * 3 / 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 3 / 5), (3 / 5, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 8
		self.force_coef = -self.friction_coef * self.game.tile_size * 3
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.follow_range = self.game.tile_size * 16
		self.attack_range = self.game.tile_size * 1.5
		self.life = 3
		self.life_display_color = RED
		self.sound_death = pgp.pg.mixer.Sound(DIR_SOUNDS + "death_spider.wav")
		self.sound_death.set_volume(self.game.volume * 1 / 3)
		self.update_pos()

	# update image et attaque si sur la frame d'attaque
	def update(self):
		Follower.update(self)
		self.life_display.update(self.pos, self.life)
		self.image.update(True, [self.moving, self.attacking])
		if self.image.counter % self.image.step == 0:
			if self.attacking and self.image.counter // self.image.step == 2:
				self.attack(self.target)

	# draw en tant qu'Entity puis draw life display
	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)

	# détruit l'entitée, joue un son
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
		self.force_coef = -self.friction_coef * self.game.tile_size * 1.5
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.follow_range = self.game.tile_size * 32
		self.attack_range = self.game.tile_size * 3
		self.damage = 2
		self.life = 32
		self.last_life = self.life
		self.life_display_color = RED
		self.sound_hit_hard = pgp.pg.mixer.Sound(DIR_SOUNDS + "boss_hard_hit.flac")
		self.sound_hit_hard.set_volume(self.game.volume * 2 / 3)
		self.sound_hit_soft = pgp.pg.mixer.Sound(DIR_SOUNDS + "boss_soft_hit.flac")
		self.sound_hit_soft.set_volume(self.game.volume * 2 / 3)
		self.sound_death = pgp.pg.mixer.Sound(DIR_SOUNDS + "death_boss.wav")
		self.update_pos()

	# update image et attaque si sur la frame d'attaque
	# de plus fait apparaitre des spiders si sa vie est basse
	# pour chaque nombre paire en dessous de 16, le boss fait apparaitre une spidre de plus (de 1 à 16 quand il meurt)
	def update(self):
		Follower.update(self)
		if self.last_life > self.life and self.submap is not None:
			if self.life % 2 == 0:
				vec_to_spider = vec(0)
				for i in range(8 - self.life // 2):
					vec_to_spider.from_polar((3 * self.game.tile_size, 360 * i / (8 - self.life // 2)))
					self.submap.add_sprite(Spider(self.game, self.submap, self.pos + vec_to_spider))
		self.last_life = self.life
		self.life_display.update(self.pos, self.life)
		self.image.update(True, [self.moving, self.attacking])
		if self.image.counter % self.image.step == 0:
			if self.image.counter // self.image.step == 2:
				if self.attacking:
					self.attack(self.target)
				else:
					self.sound_hit_soft.play()
						
	# attaque et joue un son
	def attack(self, other):
		self.sound_hit_hard.play()
		entities.Entity.attack(self, other)

	# draw en tant qu'Entity puis draw life display
	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)

	# détruit l'entitée, joue un son et fait apparaitre 16 spriders en cercle
	def kill(self):
		self.sound_death.play()
		vec_to_spider = vec(0)
		for i in range(16):
			vec_to_spider.from_polar((3 * self.game.tile_size, 360 * i / 16))
			self.submap.add_sprite(Spider(self.game, self.submap, self.pos + vec_to_spider))
		Follower.kill(self)


