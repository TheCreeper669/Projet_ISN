# custom libs
from vars import *
import entities
import pygamepp as pgp
import json_handler as json

# python libs
from math import ceil
from os import listdir

# objet "tuile de jeu"
# utilisé par les sous-map pour créer leur image
class Tile(entities.Sprite):
	def __init__(self, game, submap, image, x, y):
		entities.Sprite.__init__(self, game, vec(0))
		self.submap = submap
		self.image = image
		self.image.topleft = x, y


# permet de créer des tuiles de jeu
class VirtualTile:
	# enrigistre les paramètres et load l'image
	def __init__(self, m_map, name):
		self.map = m_map
		self.game = self.map.game
		self.name = name
		self.image = entities.Image(pgp.pg.image.load(DIR_IMAGE_TILES + [ file for file in listdir(DIR_IMAGE_TILES) if file.startswith(self.name + ".") ][0]))
		self.image.set_size((self.map.game.tile_size, self.map.game.tile_size))

	# créé une nouvelle tuile de jeu
	def summon(self, submap, x, y):
		return Tile(self.game, submap, self.image.copy(), x, y)


# permet de créer des sprites (et entitées)
class VirtualSprite:
	# enrigistre les paramètres et load l'image
	def __init__(self, m_map, name):
		self.map = m_map
		self.game = self.map.game
		self.name = name
		self.constructor = entities
		for name in self.name:
			self.constructor = self.constructor.__dict__[name]

	# créé un nouveau sprite
	def summon(self, submap, x, y):
		return self.constructor(game= self.game, pos= vec(x, y), submap= submap)



# sous carte
# créé toutes les tuiles et les sprites qui lui appartiennes
# s'occupe en suite de copartimenter les updates et le draws
# pour ne pas s'occuper que ce qui est trop en dehors de l'écrant
class Submap(entities.Sprite):
	def __init__(self, m_map, x, y, empty= False):
		entities.Sprite.__init__(self, m_map.game, vec(0))
		self.game.groups["submaps"].add(self)
		# position des sous cartes les unes par rapport aux autre (soit la position en tuile de jeu au lieux d'en pixels)
		self.submap_pos = vec(x // self.game.submap_size, y // self.game.submap_size)
		# position en pixels de la sous carte
		self.pos = self.submap_pos * self.game.submap_size * self.game.tile_size
		# carte qui contient la sous carte
		self.map = m_map
		# matrice de tuiles de jeu de la sous carte
		self.tiles = [ [ None for _ in range(self.game.submap_size) ] for _ in range(self.game.submap_size) ]
		# groupes de sprites de la sous carte
		self.content = pgp.pg.sprite.Group()		# les sprites qui n'ont pas encore été update, change au cours de chaque frame
		self.sprites = pgp.pg.sprite.Group()		# tous les sprites de la sous carte
		self.obstacles = pgp.pg.sprite.Group()		# les obstacles: pas de collisons entre eux mais bien avec le reste
		self.entities = pgp.pg.sprite.Group()		# les entitées: collisions avec tous
		self.collidables = pgp.pg.sprite.Group()	# ce qui peut rentrer en collison (plus ou moins self.obstacles + self.entities)
		# load les tuiles et les sprites de la sous carte
		if not empty:
			for i in range(self.game.submap_size):
				if x + i >= len(self.map.lines): break
				for j in range(self.game.submap_size):
					if y + j >= len(self.map.lines[x + i]): break
					if self.map.lines[x + i][y + j] in self.map.virtual_sprites:
						self.tiles[i][j] = self.map.virtual_tiles[self.map.biome_default_tile].summon(self, (x + i) * self.game.tile_size, (y + j) * self.game.tile_size)
						self.add_sprite(self.map.virtual_sprites[self.map.lines[x + i][y + j]].summon(self, (x + i + .5) * self.game.tile_size, (y + j + .5) * self.game.tile_size))
					elif self.map.lines[x + i][y + j] in self.map.biome_none_tiles:
						self.tiles[i][j] = None
					else:
						self.tiles[i][j] = self.map.virtual_tiles[self.map.lines[x + i][y + j]].summon(self, (x + i + .5) * self.game.tile_size, (y + j + .5) * self.game.tile_size)
		# ajoute des sprites à self.collidables
		self.collidables.add(self.obstacles)
		self.collidables.add(self.entities)
		# créé l'image de la sous carte de puis ses tuiles
		self.create_image()
		self.image.topleft = self.pos
		# ainsi que sa hitbox pour determiner ce qui se trouve ou non à l'interieur (appuyer sur J pour voir)
		self.hitbox = entities.Hitbox(self, color= CYAN)
		# affiche les coordonés de la sous carte (appuyer sur J pour voir)
		self.display = entities.Display(self.game, self.submap_pos, CYAN, self.pos + vec(4), font= self.game.little_font)

	# met les coordonnées de la sous carte dans sa représentation en str
	def __repr__(self):
		return "<Submap ({}, {})>".format(*self.submap_pos)

	# créer l'image de la sous map depuis ses tuiles
	def create_image(self):
		# créer une surface de la bonne taille
		surface = pgp.pg.Surface((self.game.submap_size * self.game.tile_size, self.game.submap_size * self.game.tile_size))
		# itère à travers toutes les tuiles
		# et blit chaque image de tuiles sur la surface de la sous carte au bonnes coordonées
		for x in range(self.game.submap_size):
			for y in range(self.game.submap_size):
				if self.tiles[x][y] is not None:
					surface.blit(self.tiles[x][y].image.surface, (x * self.game.tile_size, y * self.game.tile_size))
		# créer une image depuis la surface
		self.image = entities.Image(surface)

	# relie la sous carte aux autres sous cartes adjacentes (si elles exites)
	def link(self):
		# accès dirrecte
		self.topleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1] - 1] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0] - 1] else None
		self.topcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1] - 1] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0]] else None
		self.topright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1] - 1] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0] + 1] else None
		self.midleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1]] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0] - 1] else None
		self.midcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1]] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0]] else None
		self.midright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1]] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0] + 1] else None
		self.bottomleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1] + 1] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0] - 1] else None
		self.bottomcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1] + 1] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0]] else None
		self.bottomright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1] + 1] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0] + 1] else None
		# accès en set
		self.links = set([
			self.topleft, self.midleft, self.bottomleft,
			self.topcenter, self.midcenter, self.bottomcenter,
			self.topright, self.midright, self.bottomright
		])
		self.links = set([ link for link in self.links if link is not None ])
		# accès en matrice
		self.links_matrix = [
			[ self.topleft, self.midleft, self.bottomleft ],
			[ self.topcenter, self.midcenter, self.bottomcenter ],
			[ self.topright, self.midright, self.bottomright ]
		]

	# ajoute un sprite à la sous carte
	def add_sprite(self, sprite):
		self.sprites.add(sprite)
		sprite.submap = self
		if sprite in self.game.groups["obstacles"]:
			self.obstacles.add(sprite)
		if sprite in self.game.groups["entities"]:
			#print("entity {} added to {}".format(entity, self.submap_pos))
			self.entities.add(sprite)

	# retire un sprite de la sous carte
	def remove_sprite(self, sprite):
		self.sprites.remove(sprite)
		sprite.submap = None
		if sprite in self.obstacles:
			self.obstacles.remove(sprite)
		if sprite in self.entities:
			#print("entity {} removed from {}".format(entity, self.submap_pos))
			self.entities.remove(sprite)

	# update les sprites de la sous carte
	def update(self):
		# update
		for sprite in self.sprites:
			sprite.update()
		# collisions
		for entity in self.entities:
			self.collidables.remove(entity)
			for submap in self.links:
				for collided in pgp.pg.sprite.spritecollide(entity, submap.collidables, dokill= False, collided= entities.collide):
					entity.collide(collided)
					collided.collide(entity)
		# is out ?
		outside_sprites = self.sprites.copy()
		inside_sprites = pgp.pg.sprite.spritecollide(self, outside_sprites, dokill= False, collided= entities.collide)
		if len(inside_sprites) > 0:
			outside_sprites.remove(*inside_sprites)
		for sprite in outside_sprites:
			diff = sprite.pos - self.image.center
			if abs(diff.x) >= self.image.size[0] / 2 or abs(diff.y) >= self.image.size[1] / 2:
				self.remove_sprite(sprite)
				sprite.find_submap()
		outside_sprites.empty()
		# update collidables
		self.collidables.add(self.obstacles)
		self.collidables.add(self.entities)

	# draw l'image de la sous carte (tuiles de jeu)
	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface, rpos)

	# draw les sprites de la sous carte
	# seul ceux du groupe donné en argument sont draw
	# de plus les sprite sont draw de haut en bas
	def draw_content(self, surface, group, rpos= vec(0)):
		# sépare les sprites que appartiennent au bon group
		group_content = pgp.pg.sprite.Group()
		for obj in self.content:
			if obj in group:
				group_content.add(obj)
				self.content.remove(obj)
		# draw ces sprite de haut en bas
		# prend le plus haut, le draw puis recommence
		while len(group_content) != 0:
			highest = None
			y = float("+inf")
			for obj in group_content:
				if obj.pos.y < y:
					y = obj.pos.y
					highest = obj
			group_content.remove(highest)
			highest.draw(surface, rpos)

	# détruit la sous carte et tous ces sprites
	def kill(self):
		for sprite in self.sprites.sprites():
			sprite.kill()
		entities.Sprite.kill(self)



# permet d'avoir le centre de plusieur sprites
# suis ce point avec une vitesse donnée
# fait une moyenne pondéré de la postion de chaque sprite ainsi que de la dernière position
class Center(entities.Sprite):
	def __init__(self, game, group, speed= 1):
		entities.Sprite.__init__(self, game, vec(0))
		self.group = group
		self.speed = speed
		for sprite in self.group:
			self.pos += sprite.pos
		if len(self.group.sprites()) > 0:
			self.pos /= len(self.group.sprites())

	def update(self):
		self.pos *= self.speed
		for sprite in self.group:
			self.pos += sprite.pos
		self.pos /= (len(self.group.sprites()) + self.speed)



# permet de suivre un sprite
# créer en rectangle autour de celle-ci
# utilisé notament pour détermiver ce qui est dans l'écran ou non
class Follower(entities.Sprite):
	def __init__(self, game, entity, size):
		entities.Sprite.__init__(self, game, vec(0))
		self.image = entities.Image(pgp.pg.Surface(size))
		self.entity = entity
		self.image.center = self.entity.pos

	def update(self):
		self.image.center = self.entity.pos



# carte
# gère et encapsule les sous cartes
class Map:
	def __init__(self, game, mapname, biome):
		self.game = game
		self.name = mapname
		self.biome = biome
		# charge les associations lettre -> sprite et autres
		self.load_biome()
		# load la carte et sépare les lignes
		with open(DIR_MAPS + self.name + EXT_MAP, mode= "r", encoding= "utf-8") as tilemap:
			self.lines = tilemap.read().split("\n")
		# créer les sous cartes
		self.create_submaps()
		# créer un centre pour tous les sprites de joueurs
		# permet au joueur de controller plusiers sprites en même temps
		self.center = Center(self.game, self.game.groups["players"], 8)
		# position relative au centre
		self.rpos = self.center.pos - vec(self.game.res) / 2
		# créer les followers qui permettes de déterminer ce qui est sur l'écran et donc ce qui doit être draw et update
		self.on_screen_follower = Follower(self.game, self.center, vec(self.game.on_screen).elementwise() + self.game.tile_size * self.game.submap_size * 2)
		self.alive_follower = Follower(self.game, self.center, vec(self.game.on_screen).elementwise() + self.game.tile_size * self.game.submap_size * self.game.off_screen_alive * 2)
		# groupes des sous cartes
		self.on_screen = pgp.pg.sprite.Group()			# draw et update
		self.alive = pgp.pg.sprite.Group()				# seulement les updates sans les draw
		self.dead = self.game.groups["submaps"].copy()	# ni update ni draw
		# répartie les sous cartes dans les groupes ci-dessus en fonction des followers
		self.reset_submaps_groups()

	# load le biome (fichier .json)
	# contient les assciation pour lire les fichiers .map
	def load_biome(self):
		biome_data = json.load(DIR_BIOMES + self.biome + ".json")
		self.biome_tiles = biome_data["tiles"]
		self.biome_sprites = biome_data["sprites"]
		self.biome_default_tile = biome_data["default_tile"]
		self.biome_none_tiles = biome_data["none_tiles"]
		# créer des "usines" à sprites et à tuiles de jeu
		self.virtual_tiles = { tile: VirtualTile(self, self.biome_tiles[tile]) for tile in self.biome_tiles if self.biome_tiles[tile] is not None }
		self.virtual_sprites = { sprite: VirtualSprite(self, self.biome_sprites[sprite]) for sprite in self.biome_sprites }

	# recrée les followers en fonction des dimmensions de la fenètre
	def reset_followers(self):
		self.on_screen_follower.image.size = vec(self.game.on_screen).elementwise() + self.game.tile_size * self.game.submap_size * 2
		self.alive_follower.image.size = vec(self.game.on_screen).elementwise() + self.game.tile_size * self.game.submap_size * self.game.off_screen_alive * 2

	# répartie les sous cartes dans les groupes en fonction des followers
	def reset_submaps_groups(self):
		self.dead.add(self.on_screen)
		self.dead.add(self.alive)
		self.on_screen.empty()
		self.alive.empty()
		self.on_screen.add(pgp.pg.sprite.spritecollide(self.on_screen_follower, self.dead, dokill= False, collided= entities.collide))
		self.alive.add(pgp.pg.sprite.spritecollide(self.alive_follower, self.dead, dokill= False, collided= entities.collide))

	# re-répartie les sous cartes dans les groupes en fonction des followers
	def update_submaps_groups(self):
		result = pgp.pg.sprite.spritecollide(self.on_screen_follower, self.alive, dokill= False, collided= entities.collide)
		self.on_screen.add(result)
		self.alive.remove(result)
		result = pgp.pg.sprite.spritecollide(self.on_screen_follower, self.on_screen, dokill= False, collided= entities.not_collide)
		self.alive.add(result)
		self.on_screen.remove(result)
		result = pgp.pg.sprite.spritecollide(self.alive_follower, self.dead, dokill= False, collided= entities.collide)
		self.alive.add(result)
		self.dead.remove(result)
		result = pgp.pg.sprite.spritecollide(self.alive_follower, self.alive, dokill= False, collided= entities.not_collide)
		self.dead.add(result)
		self.alive.remove(result)

	# permet de férifier qu'une sous carte est bien valide, soit:
	# composée de characères valides (cf biome)
	# n'es pas vide
	def verify_submap(self, x, y):
		only_none_tiles = True
		for i in range(self.game.submap_size):
			if x + i >= len(self.lines): break
			for j in range(self.game.submap_size):
				if y + j >= len(self.lines[x + i]): break
				if self.lines[x + i][y + j] not in self.virtual_tiles and self.lines[x + i][y + j] not in self.biome_none_tiles and self.lines[x + i][y + j] not in self.virtual_sprites:
					raise ValueError("unknown char at line {} at pos {} in map file ('{}')".format(x + i + 1, y + j + 1, self.lines[x + i][y + j]))
				elif self.lines[x + i][y + j] not in self.biome_none_tiles:
					only_none_tiles = False
		return not only_none_tiles

	# créer les sous cartes depuis les lignes du fichier .map
	def create_submaps(self):
		# met toutes les lignes aux mêmes dimensions
		self.lines = [ "".join([ self.lines[j][i] if i < len(self.lines[j]) else self.biome_none_tiles[0] for j in range(len(self.lines)) ]) for i in range(max([ len(line) for line in self.lines ])) ]
		# créer un dictionaire coordonnées -> sous carte
		self.submaps = {
			x // self.game.submap_size: {
				y // self.game.submap_size: Submap(self, x, y)
				for y in range(0, len(self.lines[x]), self.game.submap_size)
				if self.verify_submap(x, y)
			}
			for x in range(0, len(self.lines), self.game.submap_size)
		}

		# retire ce qui est en dehors de la longueure de génération, cf Game.load_settings
		for x in range(-self.game.generation_length, self.game.generation_length):
			for y in range(-self.game.generation_length, self.game.generation_length):
				if x not in self.submaps:
					self.submaps[x] = {}
				if y not in self.submaps[x]:
					self.submaps[x][y] = Submap(self, x * self.game.submap_size, y * self.game.submap_size, empty= True)

		# lie chaques sous cartes entre elles, cf Submap.link
		for submap in self.game.groups["submaps"]:
			submap.link()

	# update les sous cartes
	def update(self):
		# update le centre
		self.center.update()
		# update les followers
		self.on_screen_follower.update()
		self.alive_follower.update()
		# update les sous cartes
		self.update_submaps_groups()
		self.on_screen.update()
		self.alive.update()

	def draw(self, surface):
		self.rpos = self.center.pos - vec(self.game.res) / 2
		for submap in self.on_screen:
			submap.draw(surface, self.rpos)
		for submap in self.on_screen:
			submap.content.add(submap.sprites)
			submap.content.add(submap.entities)
		for group in self.game.draw_order:
			for submap in self.on_screen:
				submap.draw_content(surface, group, self.rpos)
		for submap in self.on_screen:
			submap.content.empty()
		if self.game.draw_submap_info:
			for submap in self.on_screen:
				submap.hitbox.draw(surface, self.rpos)
				submap.display.draw(surface, self.rpos)

	# détruit la carte et toutes ses sous cartes
	def kill(self):
		# itère à traver self.game.groups["submaps"].sprites() car on modifie self.game.groups["submaps"]
		for submap in self.game.groups["submaps"].sprites():
			submap.kill()


