import pygamepp as pgp
pg = pgp.pg

from vars import *
import json_handler as json
import entities
from map import *

class Game:
	def __init__(self):
		self.load_settings()
		if self.fullscreen:
			self.window = pgp.pg.display.set_mode((self.display_info.current_w, self.display_info.current_h), pgp.pg.FULLSCREEN | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
		else:
			self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
		self.rect = self.window.get_rect()
		pgp.pg.display.set_caption(self.title)
		pgp.pg.display.set_icon(pgp.pg.image.load(DIR_IMAGE_ICONS + self.icon))
		self.clock = pgp.time.Clock()
		self.font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 32)
		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()

		self.display_info = pgp.pg.display.Info()
		self.display_info
		
		self.dt = 0

		self.groups = [
			"all", "sprites", "entities", "submaps",
			"displays", "fix_displays", "hitboxs", "fakewalls",
			"players", "mobs", "stationaries", "walls",
			"find_submap_sprites", "find_submap_entities"
		]

		self.groups = { s: pgp.pg.sprite.Group() for s in self.groups }
		for group in self.groups: self.groups[group].name = group

		self.manual_update_order = [
			"fix_displays"
		]

		self.manual_update_order = [ self.groups[s] for s in self.manual_update_order ]

		self.manual_draw_order = [
			"fix_displays"
		]

		self.manual_draw_order = [ self.groups[s] for s in self.manual_draw_order ]

		self.draw_order = [
			"fakewalls",
			"walls",
			"players"
		]

		self.draw_order = [ self.groups[s] for s in self.draw_order ]

		self.player = None
		self.framerate_display = entities.display.FixDisplay(self, lambda game: "fps: " + str(int(game.clock.get_fps())), WHITE, (0, 0))
		self.acc_display = entities.display.FixDisplay(	self,
														lambda game: "acc: {}".format((
															round(game.player.acc.x, 2),
															round(game.player.acc.y, 2)
														) if game.player is not None else None),
														WHITE,
														(0, 32))
		self.vel_display = entities.display.FixDisplay(	self,
														lambda game: "vel: {}".format((
															round(game.player.vel.x, 2),
															round(game.player.vel.y, 2)
														) if game.player is not None else None),
														WHITE,
														(0, 32 * 2))
		self.pos_display = entities.display.FixDisplay(	self,
														lambda game: "pos: {}".format((
															round(game.player.pos.x, 2),
															round(game.player.pos.y, 2)
														) if game.player is not None else None),
														WHITE,
														(0, 32 * 3))

		self.map = Map(self, mapname= "test", biome= "test")

		# play main loop
		for i in range(4):
			self.clock.tick(self.framerate)
		self.stop = False
		while not self.stop:
			self.loop()

	def load_settings(self):
		settings = json.load(FILE_SETTINGS)
		self.res = settings["res"]
		self.on_screen = self.res.copy()
		self.fullscreen = settings["fullscreen"]
		self.title = settings["title"]
		self.icon = settings["icon"]
		self.framerate = settings["framerate"]
		keyboard = settings["keyboard"]
		if keyboard == "default":
			self.keyboard = pgp.key.Keyboard()
		else:
			self.keyboard = pgp.key.load(DIR_KEYBOARDS + keyboard + ".json")
		self.draw_submap_info = settings["draw_submap_info"]
		self.draw_hitbox = settings["draw_hitbox"]
		self.tile_size = settings["tile_size"]
		self.submap_size = settings["submap_size"]
		self.off_screen_alive = settings["off_screen_alive"]

	def loop(self):
		self.dt = self.clock.tick(self.framerate)
		self.events()
		self.update()
		self.draw()

	def set_res(self, new_res):
		self.res = new_res
		self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()
		self.on_screen = self.res.copy()
		self.window = pgp.pg.display.set_mode(self.res)
		self.rect = self.window.get_rect()

	def events(self):
		self.keys = pg.key.get_pressed()
		for event in pg.event.get():
			if event.type == pgp.pg.KEYDOWN:
				"""if event.key == pgp.pg.K_F11:
					self.fullscreen = not self.fullscreen
					if self.fullscreen:
						self.window = pgp.pg.display.set_mode((self.display_info.current_w, self.display_info.current_h), pgp.pg.FULLSCREEN | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
					else:
						self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
					self.rect = self.window.get_rect()
				el"""
				if event.key == pgp.pg.K_h:
					self.draw_hitbox = not self.draw_hitbox
				elif event.key == pgp.pg.K_j:
					self.draw_submap_info = not self.draw_submap_info
				elif event.key == pgp.pg.K_k:
					self.on_screen = list(vec(self.on_screen) * (1 / 2 if self.on_screen == self.res else 2))
					self.map.reset_followers()
					self.map.reset_submaps_groups()

			elif event.type == pgp.pg.VIDEORESIZE:
				self.set_res(list(event.size))
					
			elif event.type == pgp.pg.QUIT:
				self.stop = True

	def update(self):
		self.map.update()
		for group in self.manual_update_order:
			group.update()
		for sprite in self.groups["find_submap_sprites"]: sprite.kill()
		for entity in self.groups["find_submap_entities"]: entity.kill()

	def draw(self):
		self.window.blit(self.background_image, self.background_rect)
		self.map.draw(self.window)
		for group in self.manual_draw_order:
			for sprite in group:
				sprite.draw(self.window, self.map.rpos)
		pgp.pg.display.flip()


