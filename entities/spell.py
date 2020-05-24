import pygamepp as pgp
from vars import *
import entities.base as entities

# regroupe tous les entitées qui sont lancées comme les sorts ou le flèches

# les sorts se disposent dans le terrain par eux même
# il ne faut leur donne qu'une référance au tireur
class IceSpell(entities.Entity):
	def __init__(self, owner):
		entities.Entity.__init__(self, owner.game, owner.submap, owner.pos, owner.team)
		self.game.groups["spells"].add(self)
		self.owner = owner
		# ajoute au sprite de l'owner
		self.submap.add_sprite(self)
		# met son orientation à celle de l'owner
		self.motion_orientation = vec(self.owner.weapon_orientation)
		# tourne l'image en fonction de self.owner.weapon_orientation
		self.image = entities.Image(
			pgp.pg.transform.rotate(
				pgp.pg.transform.scale(
					pgp.pg.image.load(DIR_IMAGE_ENTITIES + "ice_spell" + EXT_IMG),
					(self.game.tile_size, self.game.tile_size)
				),
				-self.motion_orientation.as_polar()[1]
			)
		)
		self.hitbox = entities.Hitbox(self, (1 / 2, 1 / 2), (2 / 7, 2 / 7), color= RED)
		self.friction_coef = -self.game.tile_size / 256
		self.force_coef = self.game.tile_size * 512
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.vel.x = self.owner.vel.x * abs(self.motion_orientation.x)
		self.vel.y = self.owner.vel.y * abs(self.motion_orientation.y)
		self.forces += self.motion_orientation * self.force_coef
		self.minvel = 256 # si self.vel < self.minvel le sort est détruit
		self.cooldown = self.game.framerate // 4 # frames avant que l'arme soit réutilisable
		self.owner.weapon_cooldown = self.cooldown
		self.sound_break = pgp.pg.mixer.Sound(DIR_SOUNDS + "ice_spell_break.ogg")
		self.sound_spell = pgp.pg.mixer.Sound(DIR_SOUNDS + "ice_spell.wav")
		self.sound_spell.set_volume(self.game.volume * 2 / 3)
		self.sound_spell.play()
		self.update_pos()

	# update et détruit le sort si il a trop ralentie
	def update(self):
		entities.Entity.update(self)
		if self.vel.length() <= self.minvel:
			self.kill()

	# détruit le sort et joue un son
	def kill(self):
		self.sound_break.play()
		entities.Entity.kill(self)

	# gère les collisions
	# tue le sort et attaque l'objet de la collision si et seulement si il est dans un équipe différante de l'owner
	# (les tois équipes sont team mob ou team player ou aucune team)
	def collide(self, other):
		entities.Entity.collide(self, other)
		if other not in self.team:
			self.attack(other)
			self.kill()

