from vars import *
import entities

from math import ceil
import os

import pygamepp as pgp
import json_handler as json

class Tile(entities.Sprite):
	def __init__(self, game, submap, image, x, y):
		entities.Sprite.__init__(self, game)
		self.submap = submap
		self.image = image
		self.image.topleft = x, y



class VirtualTile:
	def __init__(self, m_map, name):
		self.map = m_map
		self.game = self.map.game
		self.name = name
		self.image = entities.Image(pgp.pg.image.load(DIR_IMAGE_TILES + [ file for file in os.listdir(DIR_IMAGE_TILES) if file.startswith(self.name + ".") ][0]))
		self.image.set_size((TILE_SIZE, TILE_SIZE))
	def summon(self, submap, x, y):
		return Tile(self.game, submap, self.image.copy(), x, y)



class VirtualSprite:
	def __init__(self, m_map, name):
		self.map = m_map
		self.game = self.map.game
		self.name = name
		self.constructor = entities
		for name in self.name:
			self.constructor = self.constructor.__dict__[name]
	def summon(self, submap, x, y):
		return self.constructor(self.game, vec(x, y), submap)



class VirtualEntity:
	def __init__(self, m_map, name):
		self.map = m_map
		self.game = self.map.game
		self.name = name
		self.constructor = entities
		for name in self.name:
			self.constructor = self.constructor.__dict__[name]
	def summon(self, submap, x, y):
		return self.constructor(self.game, submap, vec(x, y))



class Submap(entities.Sprite):
	def __init__(self, m_map, x, y):
		entities.Sprite.__init__(self, m_map.game)
		self.game.groups["submaps"].add(self)
		self.submap_pos = vec(x // SUBMAP_SIZE, y // SUBMAP_SIZE)
		self.pos = self.submap_pos * SUBMAP_SIZE * TILE_SIZE
		self.map = m_map
		self.tiles = [ [ None for _ in range(SUBMAP_SIZE) ] for _ in range(SUBMAP_SIZE) ]
		self.content = pgp.pg.sprite.Group()
		self.sprites = pgp.pg.sprite.Group()
		self.entities = pgp.pg.sprite.Group()
		self.collidable = self.entities.copy()
		for i in range(SUBMAP_SIZE):
			if x + i >= len(self.map.lines): break
			for j in range(SUBMAP_SIZE):
				if y + j >= len(self.map.lines[x + i]): break
				if self.map.lines[x + i][y + j] in self.map.virtual_sprites:
					self.tiles[i][j] = self.map.virtual_tiles[self.map.biome_default_tile].summon(self, (x + i) * TILE_SIZE, (y + j) * TILE_SIZE)
					self.add_sprite(self.map.virtual_sprites[self.map.lines[x + i][y + j]].summon(self, (x + i + .5) * TILE_SIZE, (y + j + .5) * TILE_SIZE))
				elif self.map.lines[x + i][y + j] in self.map.virtual_entities:
					self.tiles[i][j] = self.map.virtual_tiles[self.map.biome_default_tile].summon(self, (x + i) * TILE_SIZE, (y + j) * TILE_SIZE)
					self.add_entity(self.map.virtual_entities[self.map.lines[x + i][y + j]].summon(self, (x + i + .5) * TILE_SIZE, (y + j + .5) * TILE_SIZE))
				elif self.map.lines[x + i][y + j] in self.map.biome_none_tiles:
					self.tiles[i][j] = None
				else:
					self.tiles[i][j] = self.map.virtual_tiles[self.map.lines[x + i][y + j]].summon(self, (x + i + .5) * TILE_SIZE, (y + j + .5) * TILE_SIZE)
		self.create_image()
		self.image.topleft = self.pos
		self.hitbox = entities.Hitbox(self, color= CYAN)
		self.display = entities.display.Display(self.game, self.submap_pos, CYAN, self.pos + vec(4))

	def create_image(self):
		surface = pgp.pg.Surface((SUBMAP_SIZE * TILE_SIZE, SUBMAP_SIZE * TILE_SIZE))
		for x in range(SUBMAP_SIZE):
			for y in range(SUBMAP_SIZE):
				if self.tiles[x][y] is not None:
					surface.blit(self.tiles[x][y].image.surface, (x * TILE_SIZE, y * TILE_SIZE))
		self.image = entities.Image(surface)

	def link(self):
		self.topleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1] - 1] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0] - 1] else None
		self.topcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1] - 1] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0]] else None
		self.topright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1] - 1] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] - 1 in self.map.submaps[self.submap_pos[0] + 1] else None
		self.midleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1]] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0] - 1] else None
		self.midcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1]] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0]] else None
		self.midright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1]] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] in self.map.submaps[self.submap_pos[0] + 1] else None
		self.bottomleft = self.map.submaps[self.submap_pos[0] - 1][self.submap_pos[1] + 1] if self.submap_pos[0] - 1 in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0] - 1] else None
		self.bottomcenter = self.map.submaps[self.submap_pos[0]][self.submap_pos[1] + 1] if self.submap_pos[0] in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0]] else None
		self.bottomright = self.map.submaps[self.submap_pos[0] + 1][self.submap_pos[1] + 1] if self.submap_pos[0] + 1 in self.map.submaps and self.submap_pos[1] + 1 in self.map.submaps[self.submap_pos[0] + 1] else None
		self.links = set([
			self.topleft, self.midleft, self.bottomleft,
			self.topcenter, self.midcenter, self.bottomcenter,
			self.topright, self.midright, self.bottomright
		])
		self.links = set([ link for link in self.links if link is not None ])
		self.links_matrix = [
			[ self.topleft, self.midleft, self.bottomleft ],
			[ self.topcenter, self.midcenter, self.bottomcenter ],
			[ self.topright, self.midright, self.bottomright ]
		]

	def add_sprite(self, sprite):
		self.sprites.add(sprite)
		if sprite in self.game.groups["find_submap_sprites"]:
			self.game.groups["find_submap_sprites"].remove(sprite)
		sprite.submap = self

	def remove_sprite(self, sprite):
		self.sprites.remove(sprite)
		self.game.groups["find_submap_sprites"].add(sprite)
		sprite.submap = None

	def add_entity(self, entity):
		print("entity {} added to {}".format(entity, self.submap_pos))
		self.entities.add(entity)
		if entity in self.game.groups["find_submap_entities"]:
			self.game.groups["find_submap_entities"].remove(entity)
		entity.submap = self

	def remove_entity(self, entity):
		print("entity {} removed from {}".format(entity, self.submap_pos))
		self.entities.remove(entity)
		self.game.groups["find_submap_entities"].add(entity)
		entity.submap = None

	def update(self):
		# sprites
		for sprite in self.sprites:
			sprite.update()
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
		# entities
		for entity in self.entities:
			entity.update()
		for entity in self.collidable:
			for submap in self.links:
				for collided in pgp.pg.sprite.spritecollide(entity, submap.collidable, dokill= False, collided= entities.collide):
					entity.collide(collided)
					collided.collide(entity)
		outside_entities = self.entities.copy()
		inside_entities = pgp.pg.sprite.spritecollide(self, outside_entities, dokill= False, collided= entities.collide)
		if len(inside_entities) > 0:
			outside_entities.remove(*inside_entities)
		for entity in outside_entities:
			diff = entity.pos - self.image.center
			if abs(diff.x) >= self.image.size[0] / 2 or abs(diff.y) >= self.image.size[1] / 2:
				self.remove_entity(entity)
				entity.find_submap()
		outside_entities.empty()
		self.collidable = self.entities.copy()

	def draw(self, surface, rpos= vec(0)):
		self.image.draw(surface, rpos)

	def draw_content(self, surface, group, rpos= vec(0)):
		group_content = pgp.pg.sprite.Group()
		for obj in self.content:
			if obj in group:
				group_content.add(obj)
				self.content.remove(obj)
		while len(group_content) != 0:
			highest = None
			y = float("+inf")
			for obj in group_content:
				if obj.pos.y < y:
					y = obj.pos.y
					highest = obj
			group_content.remove(highest)
			highest.draw(surface, rpos)



class Follower(entities.Sprite):
	def __init__(self, game, entity, size):
		entities.Sprite.__init__(self, game)
		self.image = entities.Image(pgp.pg.Surface(size))
		self.entity = entity
		self.image.center = self.entity.pos

	def update(self):
		self.image.center = self.entity.pos



class Map:
	def __init__(self, game, mapname, biome):
		self.game = game
		self.name = mapname
		self.biome = biome
		self.load_biome()
		with open(DIR_MAPS + self.name + EXT_MAP, mode= "r", encoding= "utf-8") as tilemap:
			self.lines = tilemap.read().split("\n")
		self.create_submaps()
		self.entity = self.game.player
		self.rpos = self.entity.pos - vec(self.game.res[0]) / 2
		self.on_screen_follower = Follower(self.game, self.entity, self.game.res[0])
		self.alive_follower = Follower(self.game, self.entity, (self.game.res[0][0] + TILE_SIZE * SUBMAP_SIZE * OFF_SCREEN_ALIVE_SUBMAPS_RADIUS * 2, self.game.res[0][1] + TILE_SIZE * SUBMAP_SIZE * OFF_SCREEN_ALIVE_SUBMAPS_RADIUS * 2))
		self.on_screen = pgp.pg.sprite.Group()
		self.alive = pgp.pg.sprite.Group()
		self.dead = self.game.groups["submaps"].copy()
		self.reset_submaps_groups()

	def load_biome(self):
		biome_data = json.load(DIR_JSON_BIOMES + self.biome + ".json")
		self.biome_tiles = biome_data["tiles"]
		self.biome_sprites = biome_data["sprites"]
		self.biome_default_tile = biome_data["default_tile"]
		self.biome_none_tiles = biome_data["none_tiles"]
		self.biome_entities = biome_data["entities"]
		self.virtual_tiles = { tile: VirtualTile(self, self.biome_tiles[tile]) for tile in self.biome_tiles if self.biome_tiles[tile] is not None }
		self.virtual_sprites = { sprite: VirtualSprite(self, self.biome_sprites[sprite]) for sprite in self.biome_sprites }
		self.virtual_entities = { entity: VirtualEntity(self, self.biome_entities[entity]) for entity in self.biome_entities }

	def reset_followers(self):
		self.on_screen_follower.image.size = self.game.res[0]
		self.alive_follower.image.size = self.game.res[0][0] + TILE_SIZE * SUBMAP_SIZE * OFF_SCREEN_ALIVE_SUBMAPS_RADIUS * 2, self.game.res[0][1] + TILE_SIZE * SUBMAP_SIZE * OFF_SCREEN_ALIVE_SUBMAPS_RADIUS * 2

	def reset_submaps_groups(self):
		self.dead.add(self.on_screen)
		self.dead.add(self.alive)
		self.on_screen.empty()
		self.alive.empty()
		self.on_screen.add(pgp.pg.sprite.spritecollide(self.on_screen_follower, self.dead, dokill= False, collided= entities.collide))
		self.alive.add(pgp.pg.sprite.spritecollide(self.alive_follower, self.dead, dokill= False, collided= entities.collide))

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

	def verify_submap(self, x, y):
		only_none_tiles = True
		for i in range(SUBMAP_SIZE):
			if x + i >= len(self.lines): break
			for j in range(SUBMAP_SIZE):
				if y + j >= len(self.lines[x + i]): break
				if self.lines[x + i][y + j] not in self.virtual_tiles and self.lines[x + i][y + j] not in self.biome_none_tiles and self.lines[x + i][y + j] not in self.virtual_entities and self.lines[x + i][y + j] not in self.virtual_sprites:
					raise ValueError("unknown char at line {} at pos {} in map file ('{}')".format(x + i + 1, y + j + 1, self.lines[x + i][y + j]))
				elif self.lines[x + i][y + j] not in self.biome_none_tiles:
					only_none_tiles = False
		return not only_none_tiles

	def create_submaps(self):
		self.lines = [ "".join([ self.lines[j][i] if i < len(self.lines[j]) else self.biome_none_tiles[0] for j in range(len(self.lines)) ]) for i in range(max([ len(line) for line in self.lines ])) ]
		self.submaps = {
			x // SUBMAP_SIZE: {
				y // SUBMAP_SIZE: Submap(self, x, y)
				for y in range(0, len(self.lines[x]), SUBMAP_SIZE)
				if self.verify_submap(x, y)
			}
			for x in range(0, len(self.lines), SUBMAP_SIZE)
		}
		for submap in self.game.groups["submaps"]:
			submap.link()

	def update(self):
		self.on_screen_follower.update()
		self.alive_follower.update()
		self.update_submaps_groups()
		self.on_screen.update()
		self.alive.update()

	def draw(self, surface):
		self.rpos = self.entity.pos - vec(self.game.res[0]) / 2
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



if __name__ == "__main__":
	m_map = Map(None, "test")
	print(m_map.lines)
	print(m_map.submaps)
	for x in m_map.submaps:
		for y in m_map.submaps[x]:
			print("{} {} {}".format(x, y, m_map.submaps[x][y].entities))
			for i in m_map.submaps[x][y].tiles:
				for j in i:
					print(j, end= " ")
				print()