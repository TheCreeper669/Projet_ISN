import pygamepp as pgp
from vars import *

import entities.base as entities

# regroupes les objets statiques comme les mur et les portails

# un faux mur
# n'a que l'apparence d'un mur
# ne fait pas de collisions (réduit le temps d'éxecution)
class FakeWall(entities.Sprite):
	def __init__(self, game, pos, submap):
		entities.Sprite.__init__(self, game, pos, submap)
		self.game.groups["fakewalls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_SPRITES + "fakewall" + EXT_IMG), (self.game.tile_size, self.game.tile_size)))



# empèche le joueur de passer
# si il y a un Wall adjacent dans sa sous carte les deux Wall fusionnent en BigWall
class Wall(entities.Obstacle):
	def __init__(self, game, submap, pos):
		entities.Obstacle.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall" + EXT_IMG), (self.game.tile_size, self.game.tile_size)))
		self.hitbox = entities.Hitbox(self, color= BLUE)
		self.update()

		# tentative de fusion
		for other in self.submap.obstacles:
			if other.pos.x == self.pos.x:
				if type(other) is Wall and self.pos.y == other.pos.y + self.game.tile_size:
					new_wall = BigWall(self.game, self.submap, other.pos + vec(0, self.game.tile_size / 2), (1, 2))
					new_wall.image.topleft = other.image.topleft
					new_wall.pos = vec(new_wall.image.center)
					self.submap.add_sprite(new_wall)
					other.kill()
					self.kill()
					return
				elif type(other) is BigWall and other.size.y == int((self.pos.y - (other.pos.y - (other.size.y // 2) * self.game.tile_size)) / self.game.tile_size) and other.size.x == 1:
					new_wall = BigWall(self.game, self.submap, other.pos + vec(0, other.size.y * self.game.tile_size / 2), (1, other.size.y + 1))
					new_wall.image.topleft = other.image.topleft
					new_wall.pos = vec(new_wall.image.center)
					self.submap.add_sprite(new_wall)
					other.kill()
					self.kill()
					return
			elif other.pos.y == self.pos.y:
				if type(other) is Wall and self.pos.x == other.pos.x + self.game.tile_size:
					new_wall = BigWall(self.game, self.submap, other.pos + vec(self.game.tile_size / 2, 0), (2, 1))
					new_wall.image.topleft = other.image.topleft
					new_wall.pos = vec(new_wall.image.center)
					self.submap.add_sprite(new_wall)
					other.kill()
					self.kill()
					return
				elif type(other) is BigWall and other.size.x == int((self.pos.x - (other.pos.x - (other.size.x // 2) * self.game.tile_size)) / self.game.tile_size) and other.size.y == 1:
					new_wall = BigWall(self.game, self.submap, other.pos, (other.size.x + 1, 1))
					new_wall.image.topleft = other.image.topleft
					new_wall.pos = vec(new_wall.image.center)
					self.submap.add_sprite(new_wall)
					other.kill()
					self.kill()
					return




# fusion de plusieurs mur adjacents
# permet de réduire le temps d'éxecution mais augment le temps de chargement de la carte
class BigWall(entities.Obstacle):
	def __init__(self, game, submap, pos, size= vec(1, 1)):
		entities.Obstacle.__init__(self, game, submap, pos)
		self.game.groups["walls"].add(self)
		self.size = vec(size)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_ENTITIES + "wall" + EXT_IMG), (self.game.tile_size, self.game.tile_size)))
		self.image.stack(size)
		self.hitbox = entities.Hitbox(self, color= BLUE)
		self.update()
		#print("{} | {} | {}".format(self.pos.elementwise() / self.game.tile_size, self.submap.submap_pos.elementwise() * self.game.submap_size, self.submap.submap_pos.elementwise() * self.game.submap_size + vec(self.game.submap_size)))



# portails de sortie de niveaux
# n'est visible que si le joueur à tué tous les mob
# si le joueur le touche il passe au prochain niveau
class Portal(entities.Sprite):
	def __init__(self, game, pos, submap= None):
		entities.Sprite.__init__(self, game, pos, submap)
		self.game.groups["portals"].add(self)
		self.image = entities.Image(pgp.pg.transform.scale(pgp.pg.image.load(DIR_IMAGE_SPRITES + "portal" + EXT_IMG), (self.game.tile_size, self.game.tile_size)))
		self.sound_win_level = pgp.pg.mixer.Sound(DIR_SOUNDS + "win_level.wav")
		self.sound_win_level.set_volume(self.game.volume * 1 / 3)
		self.won_level = False

	# test si il touche un joueur
	def colliding_with_player(self):
		for player in self.game.groups["players"]:
			if entities.util.collide(self, player):
				return True
		return False

	# test si il est visible et touche un joueur
	# alors il lance le prochain niveau
	# si il est visible et mais ne touche pas un joueur
	# alors il met la musique calme et joue un son de victoire pour signaler au joueur qu'il a finis
	def update(self):
		entities.Sprite.update(self)
		if len(self.game.groups["mobs"]) == 0:
			if not self.won_level:
				self.won_level = True
				if self.game.music != MUSIC_THEME:
					self.game.change_music(MUSIC_THEME)
				self.sound_win_level.play()
			if self.colliding_with_player():
				self.game.win_level()

	# draw uniquement si il n'y a plus de mob
	def draw(self, surface, rpos= vec(0)):
		if len(self.game.groups["mobs"]) == 0:
			self.image.draw(surface, rpos)


