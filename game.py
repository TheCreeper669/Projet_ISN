import pygamepp as pgp
pygame = pgp.pg

from vars import *
import json_handler as json
import entities
from map import *

class Game:
	def __init__(self):
		self.load_settings()
		self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE)
		self.rect = self.window.get_rect()
		pgp.pg.display.set_caption(self.title)
		pgp.pg.display.set_icon(pgp.pg.image.load(DIR_IMAGE_ICONS + self.icon))
		self.clock = pgp.time.Clock()
		self.little_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 16)
		self.font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 32)
		self.game_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), self.tile_size // 2)
		self.big_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 128)
		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()

		self.display_info = pgp.pg.display.Info()

		self.groups = [
			"all", "sprites", "obstacles", "entities", "submaps",
			"displays", "fix_displays", "hitboxs", "fakewalls",
			"team_players", "team_mobs",
			"players", "mobs", "walls", "spells", "portals",
			"followers"
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
			"portals",
			"fakewalls",
			"walls",
			"mobs",
			"spells",
			"players"
		]

		self.draw_order = [ self.groups[s] for s in self.draw_order ]

		self.framerate_display = entities.FixDisplay(self, lambda game: "fps: " + str(int(game.clock.get_fps())), WHITE, (0, 0), self.font)
		"""
		self.acc_display = entities.FixDisplay(
			self,
			lambda game: "acc: {}".format((
				round(game.groups["players"].sprites()[0].acc.x / game.tile_size, 2),
				round(game.groups["players"].sprites()[0].acc.y / game.tile_size, 2)
			) if len(game.groups["players"].sprites()) > 0 else None),
			WHITE,
			(0, 32),
			self.font
		)
		self.vel_display = entities.FixDisplay(
			self,
			lambda game: "vel: {}".format((
				round(game.groups["players"].sprites()[0].vel.x / game.tile_size, 2),
				round(game.groups["players"].sprites()[0].vel.y / game.tile_size, 2)
			) if len(game.groups["players"].sprites()) > 0 else None),
			WHITE,
			(0, 32 * 2),
			self.font
		)
		self.pos_display = entities.FixDisplay(
			self,
			lambda game: "pos: {}".format((
				round(game.groups["players"].sprites()[0].pos.x / game.tile_size, 2),
				round(game.groups["players"].sprites()[0].pos.y / game.tile_size, 2)
			) if len(game.groups["players"].sprites()) > 0 else None),
			WHITE,
			(0, 32 * 3),
			self.font
		)
		"""

		self.map = Map(self, self.maps[self.map_index], self.biome)
		
		self.isgameover = False
		self.won_level = False
		self.pause = False

		self.pause_mask = pgp.pg.Surface(self.res)
		self.pause_mask.fill(BLACK)
		self.pause_mask.set_alpha(64)
		self.pause_mask_rect = self.pause_mask.get_rect()

		self.dt = 0

		self.music = None
		self.change_music(MUSIC_THEME)

		for i in range(4):
			self.clock.tick(self.framerate)
		self.stop = False
		while not self.stop:
			self.loop()

	def load_settings(self):
		settings = json.load(FILE_SETTINGS)
		self.minres = settings["minres"]
		self.res = settings["res"]
		self.on_screen = self.res.copy()
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
		self.generation_length = settings["generation_length"]
		self.maps = settings["maps"]
		self.map_index = 0
		self.biome = settings["biome"]
		self.volume = settings["volume"] / 100

	def loop(self):
		self.dt = self.clock.tick(self.framerate)
		if self.framerate != 0:
			if 1 / (2 * self.framerate) > self.dt or self.dt > 2 / self.framerate:
				print("/!\\ LAG: {}fps or {}s/t | rather than {}fps or {}s/t".format(round(1 / self.dt), round(self.dt, 3), self.framerate, round(1 / self.framerate, 3)))
				return
		if not self.pause:
			self.events()
			self.update()
			self.draw()
		else:
			self.events_pause()
			self.update_pause()
			self.draw_pause()

	def set_res(self, new_res):
		if new_res[0] < self.minres[0]:
			new_res[0] = self.minres[0]
		if new_res[1] < self.minres[1]:
			new_res[1] = self.minres[1]

		self.res = new_res

		self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE)
		self.rect = self.window.get_rect()

		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()

		self.pause_mask = pgp.pg.Surface(self.res)
		self.pause_mask.fill(BLACK)
		self.pause_mask.set_alpha(64)
		self.pause_mask_rect = self.pause_mask.get_rect()

		self.on_screen = self.res.copy()
		self.map.reset_followers()
		self.map.reset_submaps_groups()

	def events(self):
		self.keys = pgp.pg.key.get_pressed()
		for event in pgp.pg.event.get():
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
					self.on_screen = list(vec(self.on_screen) * (1 / 16 if self.on_screen == self.res else 16))
					self.map.reset_followers()
					self.map.reset_submaps_groups()
				elif event.key == pgp.pg.K_ESCAPE:
					self.pause = not self.pause

			elif event.type == pgp.pg.VIDEORESIZE:
				self.set_res([event.w, event.h])
					
			elif event.type == pgp.pg.QUIT:
				self.stop = True

	def update(self):
		self.map.update()
		for group in self.manual_update_order:
			group.update()

	def draw(self):
		self.window.blit(self.background_image, self.background_rect)
		self.map.draw(self.window)
		for group in self.manual_draw_order:
			for sprite in group:
				sprite.draw(self.window, self.map.rpos)
		pgp.pg.display.flip()

	def events_pause(self):
		self.keys = pgp.pg.key.get_pressed()
		for event in pgp.pg.event.get():
			if event.type == pgp.pg.KEYDOWN:
				if event.key == pgp.pg.K_ESCAPE and not self.isgameover:
					self.pause = not self.pause
					if self.pause:
						self.paused_surface = self.window.copy()
						self.paused_surface_rect = self.paused_surface.get_rect()

			elif event.type == pgp.pg.VIDEORESIZE:
				self.set_res(list(event.size))
					
			elif event.type == pgp.pg.QUIT:
				self.stop = True

	def update_pause(self):
		for group in self.manual_update_order:
			group.update()

	def draw_pause(self):
		self.window.blit(self.background_image, self.background_rect)
		self.map.draw(self.window)
		self.window.blit(self.pause_mask, self.pause_mask_rect)
		for group in self.manual_draw_order:
			for sprite in group:
				sprite.draw(self.window, self.map.rpos)
		pgp.pg.display.flip()

	def gameover(self):
		self.pause = True
		self.isgameover = True
		self.gameover_display = entities.FixDisplay(self, "GAME OVER", WHITE, (self.res[0] // 2, self.res[1] // 2), font= self.big_font)
		self.gameover_display.pos -= vec(self.gameover_display.image.size) / 2
		self.gameover_display.update()
		self.change_music(MUSIC_GAMEOVER, 1)

	def win_level(self):
		pgp.pg.mixer.Sound(DIR_SOUNDS + "teleport.wav").play()
		self.won_level = True
		self.map.kill()
		self.map_index += 1
		if self.map_index >= len(self.maps):
			self.win_game()
			return
		self.won_level = False
		if self.map_index == len(self.maps) - 1:
			self.change_music(MUSIC_BOSS)
		else:
			self.change_music(MUSIC_BATTLE)
		self.map = Map(self, self.maps[self.map_index], self.biome)

	def win_game(self):
		self.change_music(MUSIC_WON, 1)
		self.pause = True
		self.isgameover = True
		self.gameover_display = entities.FixDisplay(self, "YOU WON", WHITE, (self.res[0] // 2, self.res[1] // 2), font= self.big_font)
		self.gameover_display.pos -= vec(self.gameover_display.image.size) / 2
		self.gameover_display.update()

	def change_music(self, filename, repeat= -1):
		self.music = filename
		pgp.pg.mixer.music.load(self.music)
		pgp.pg.mixer.music.set_volume(self.volume)
		pgp.pg.mixer.music.play(repeat)



