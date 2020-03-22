import pygamepp as pgp
import json_handler as json
from vars import *

class Image(pgp.pg.Rect):
	def __init__(self, surface):
		self.surface = surface
		pgp.pg.Rect.__init__(self, self.surface.get_rect())
		self.rpos_rect = pgp.pg.Rect(self.center, self.size)
		self.reset_surface(surface)

	def reset_surface(self, surface):
		self.surface = surface
		self.size = self.surface.get_rect().size
		self.rpos_rect.size = self.size

	def scale(self, w, h):
		self.reset_surface(pgp.pg.transform.scale(self.surface, (w, h)))

	def set_width(self, w):
		self.scale(w, self.h * w // self.w)

	def set_height(self, h):
		self.scale(h, self.w * h // self.h)

	def set_size(self, size):
		self.scale(*size)

	def stack(self, size):
		surface = pgp.pg.Surface(vec_mul(vec(self.size), vec(size)))
		rect = rect(self)
		for i in range(size[0]):
			for j in range(size[1]):
				rect.topleft = i * self.size, j * self.size
				surface.blit(self.surface, rect)
		self.reset_surface(surface)

	def copy(self):
		return type(self)(self.surface.copy())

	def draw(self, surface, rpos= vec(0)):
		self.rpos_rect.center = vec(self.center) - rpos
		surface.blit(self.surface, self.rpos_rect)



class Anim(Image):
	frames = {}
	default_frames = {}

	def __init__(self, game, folder, size):
		Image.__init__(self, pgp.pg.Surface((1, 1)))
		self.game = game
		self.folder = folder
		self.size = size
		self.load_info()
		self.current_value = None
		self.current_anim = self.default_anim
		self.counter = 0
		self.load_frames()
		self.change_anim([0, 0])
		self.update(anim= False)

	def load_info(self):
		self.info = json.load(self.folder + "info.json")
		if self.game.framerate != 0:
			self.step = int(self.info["step"] * self.game.framerate)
		else:
			self.step = int(self.info["step"] * 60)
		self.names = self.info["names"]
		self.anims = self.info["anims"]
		self.values = self.info["values"]
		self.default_frame = self.info["default_frame"]
		self.no_change_value = self.info["no_change_value"]
		self.default_anim = self.info["default_anim"]

	def load_frames(self):
		if self.folder not in self.frames:
			self.frames[self.folder] = self.anims.copy()
			self.anims = self.frames[self.folder]
			for anim in self.anims:
				for frame in range(len(self.anims[anim])):
					self.anims[anim][frame] = pgp.pg.transform.scale(pgp.pg.image.load(self.folder + anim + "/" + self.anims[anim][frame] + ".png"), self.size)
			self.default_anim = self.anims[self.default_anim]
			self.default_frames[self.folder] = { anim: pgp.pg.transform.scale(pgp.pg.image.load(self.folder + anim + "/" + self.default_frame[anim] + ".png"), self.size) for anim in self.anims }
			self.default_frame = self.default_frames[self.folder]
		else:
			self.anims = self.frames[self.folder]
			self.default_anim = self.anims[self.default_anim]
			self.default_frame = self.default_frames[self.folder]

	def get_anim_by_value(self, value):
		for anim in self.values:
			if value in self.values[anim]:
				return anim

	def change_anim(self, value):
		if value == self.current_value or value in self.no_change_value: return
		self.current_value = value
		self.current_anim = self.get_anim_by_value(self.current_value)
		self.counter = len(self.anims[self.current_anim]) * self.step

	def update(self, anim= True, value= None):
		if value is not None:
			self.change_anim(value)
		if anim:
			if self.counter <= 0:
				self.counter = len(self.anims[self.current_anim])
				self.counter *= self.step - 1
			else:
				self.counter -= 1
			self.reset_surface(self.anims[self.current_anim][self.counter // self.step])
		else:
			self.reset_surface(self.default_frame[self.current_anim])





class Sprite(pgp.pg.sprite.Sprite):
	def __init__(self, game, pos, submap= None):
		pgp.pg.sprite.Sprite.__init__(self)
		self.game = game
		self.game.groups["sprites"].add(self)
		self.submap = submap
		self.pos = vec(pos[0], pos[1])

	def update(self):
		self.image.center = self.pos

	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface, rpos)

	def find_submap(self):
		submaps = pgp.pg.sprite.spritecollide(self, self.game.groups["submaps"], dokill= False, collided= collide)
		if len(submaps) > 0:
			submaps[0].add_sprite(self)
			print("sprite {} added to {}".format(self, submaps[0]))



def collide(a, b):
	if not hasattr(a, "hitbox"):
		if not hasattr(b, "hitbox"):
			return a.image.colliderect(b.image)
		else:
			return a.image.colliderect(b.hitbox.image)
	else:
		if not hasattr(b, "hitbox"):
			return a.hitbox.image.colliderect(b.image)
		else:
			return a.hitbox.image.colliderect(b.hitbox.image)

def not_collide(a, b):
	return not collide(a, b)


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

	def reset_image(self, color, width= 1):
		self.image.surface.fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(1), vec(self.image.size) - vec(2))).fill(color)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 1), vec(self.image.size) - vec(width + 3))).fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(width + 2), vec(self.image.size) - vec(width + 4))).fill(TRANSPARENT)
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)

	def update(self):
		self.image.center = vec(self.sprite.image.topleft) + (self.sprite.image.size[0] * self.rpos.x, self.sprite.image.size[1] * self.rpos.y)

"""
class Center(Sprite):
	def __init__(self, sprite, color= RED):
		Sprite.__init__(self, sprite.game)
		self.sprite = sprite
		self.game.groups["centers"].add(self)
		width = 4
		self.image = Image(pgp.pg.Surface(vec(width)))
		self.image.surface.fill(BLACK)
		self.image.surface.subsurface(pgp.pg.Rect(vec(1), vec(width - 2))).fill(color)

	def update(self):
		self.image.center = self.sprite.pos
"""

def get_orientation(keys, keyboard, key_up, key_down, key_left, key_right):
	orientation = vec(0)
	if keys[keyboard[key_left]]:
		orientation.x += -1
	if keys[keyboard[key_right]]:
		orientation.x += 1
	if keys[keyboard[key_up]]:
		orientation.y += -1
	if keys[keyboard[key_down]]:
		orientation.y += 1
	return orientation

class Entity(Sprite):
	def __init__(self, game, submap, pos):
		Sprite.__init__(self, game, pos, submap)
		self.game.groups["entities"].add(self)
		self.acc = vec(0)
		self.vel = vec(0)
		self.friction_coef = 0
		self.forces = vec(0)
		self.mass = 1
		self.life = 1
		# bools
		self.movable = True

	def update(self):
		if self.movable:
			self.forces += self.vel * self.friction_coef * self.mass
			self.acc = self.forces / self.mass
			self.vel += self.acc * self.game.dt
			self.pos += self.vel * self.game.dt
			self.forces = vec(0)
		self.update_pos()
		if self.life <= 0 and self.submap is not None:
			self.submap.remove_entity(self)

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
			submaps[0].add_entity(self)

	def collide(self, other):
		if self.movable:
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

