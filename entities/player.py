import pygamepp as pgp
from vars import *
import entities.base as entities
import entities.spell as spell
import entities.display as display

class Player(entities.Entity):
	def __init__(self, game, submap, pos):
		entities.Entity.__init__(self, game, submap, pos)
		self.game.groups["players"].add(self)
		self.game.player = self
		#self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "player.png"), (self.game.tile_size * 2, self.game.tile_size * 2)))
		self.image = entities.Anim(self.game, DIR_IMAGE_ENTITIES + "player/", (self.game.tile_size * 2, self.game.tile_size * 2))
		self.hitbox = entities.Hitbox(self, (1 / 2, 5 / 7), (2 / 7, 2 / 7), color= RED)
		self.motion_orientation = vec(0)
		self.weapon_orientation = vec(0)
		self.weapon_cooldown = self.game.framerate // 4
		self.weapon_current_cooldown = 0
		self.friction_coef = -self.game.tile_size / 8
		self.force_coef = -self.friction_coef * self.game.tile_size * 4
		#max_speed = abs(self.force_coef / self.friction_coef)
		self.life = 5
		self.life_display = display.Display(self.game, self.life, GREEN, self.pos)

	def update(self):
		self.motion_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_MOTION)
		self.forces += self.motion_orientation * self.force_coef
		entities.Entity.update(self)
		self.life_display.update(self.pos, self.life)
		self.image.update(self.motion_orientation != vec(0), self.motion_orientation)
		self.weapon_orientation = entities.get_orientation(self.game.keys, self.game.keyboard, *K_WEAPON)
		if self.weapon_current_cooldown > 0:
			self.weapon_current_cooldown -= 1
		elif self.weapon_current_cooldown == 0 and self.weapon_orientation != vec(0):
			self.weapon_current_cooldown = self.weapon_cooldown
			spell.IceSpell(self)

	def draw(self, surface, rpos):
		entities.Entity.draw(self, surface, rpos)
		self.life_display.draw(surface, rpos)


