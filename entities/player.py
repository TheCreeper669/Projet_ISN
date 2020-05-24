import pygamepp as pgp
from vars import *

import entities.base as entities
from entities.spell import IceSpell

# entitée que contrôle le joueur
class Player(entities.Entity):
	def __init__(self, game, submap, pos):
		entities.Entity.__init__(self, game, submap, pos, game.groups["team_players"])
		self.game.groups["players"].add(self)
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "player/", (self.game.tile_size * 2, self.game.tile_size * 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 5 / 7), (2 / 7, 2 / 7), color= RED)
		self.motion_orientation = vec(0)
		self.weapon_orientation = vec(0)
		self.weapon_cooldown = 0
		self.friction_coef = -self.game.tile_size / 8
		self.force_coef = -self.friction_coef * self.game.tile_size * 4
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.life = 3
		self.last_life = self.life
		self.life_display_color = GREEN
		self.sound_hurt = pgp.pg.mixer.Sound(DIR_SOUNDS + "player_hurt.wav")
		self.sound_death = pgp.pg.mixer.Sound(DIR_SOUNDS + "death_player.wav")

	# prend l'orientation des touches pour le déplacement et l'attaque
	# les touches de déplacements contrôlent l'accélération du joueur
	# si sa vie baisse jou un son
	# créer un IceSpell si le joueur tire
	def update(self):
		self.motion_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_MOTION)
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)
		if self.last_life > self.life and self.submap is not None:
			self.sound_hurt.play()
		self.last_life = self.life
		self.image.update(self.motion_orientation != vec(0), self.motion_orientation)
		self.weapon_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_WEAPON)
		# baisser le cooldown si il est strictement positif
		if self.weapon_cooldown > 0:
			self.weapon_cooldown -= 1
		# tirer si le cooldown est de 0 et que le verteur d'orientation d'attaque n'est pas null
		# de plus si le joueur n'est pas dans une sous carte, il ne peux pas tirer de sort
		elif self.weapon_cooldown == 0 and self.weapon_orientation != vec(0) and self.submap is not None:
			IceSpell(self)

	# draw en tant qu'Entity et draw life display
	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)

	# détruit le joueur et jou un son
	# de plus lance le gameover si il est le dernier joueur et que le joueur n'a pas gagné
	def kill(self):
		if not self.game.won_level:
			self.sound_death.play()
		entities.Entity.kill(self)
		if len(self.game.groups["players"].sprites()) == 0 and not self.game.won_level:
			self.game.gameover()


