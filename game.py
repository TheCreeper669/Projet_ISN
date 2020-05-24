# pygamepp: une librairie améliore quelques fonctionalité de pygame (contien pygame en tant que pygamepp.pg)
import pygamepp as pgp
pygame = pgp.pg
# vars: définie des constantes comme des couleurs et des chemins, dossiers, etc...
from vars import *
# json_haldler: json_haldler.load et json_haldler.dump pour écrire et lire des fichiers json
import json_handler as json
# entities: gère les entitées (le jouers, les ennemis, etc...)
import entities
# map: gère les cartes, les sous cartes, les tuiles de jeu et les fichier qui les contiennes
from map import *

# class principale qui encapsule tout le jeu
class Game:
	# initialisation du jeu (load les paramètres et créé le objets du jeu: fenètre, clock, etc...)
	def __init__(self):
		# load les paramètres depuis data/settings.json
		self.load_settings()

		# créer la fenètre
		self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE)
		self.rect = self.window.get_rect()
		pgp.pg.display.set_caption(self.title)
		pgp.pg.display.set_icon(pgp.pg.image.load(DIR_IMAGE_ICONS + self.icon))

		# clock
		self.clock = pgp.time.Clock()

		# fonts
		self.little_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 16)
		self.font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 32)
		self.game_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), self.tile_size // 2)
		self.big_font = pgp.pg.font.Font(pgp.pg.font.get_default_font(), 128)
		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()

		# load les infos de l'écran (hauteur, longueur, etc...)
		self.display_info = pgp.pg.display.Info()

		# créer tous les groupes qui contiennent les entitées
		self.groups = [
			"all", "sprites", "obstacles", "entities", "submaps",
			"displays", "fix_displays", "hitboxs", "fakewalls",
			"team_players", "team_mobs",
			"players", "mobs", "walls", "spells", "portals",
			"followers"
		]

		self.groups = { s: pgp.pg.sprite.Group() for s in self.groups }
		for group in self.groups: self.groups[group].name = group

		# groupes à update manulement (et non pas par l'intermédiaire de la map)
		self.manual_update_order = [
			"fix_displays"
		]

		self.manual_update_order = [ self.groups[s] for s in self.manual_update_order ]

		# groupes à draw manulement (et non pas par l'intermédiaire de la map)
		self.manual_draw_order = [
			"fix_displays"
		]

		self.manual_draw_order = [ self.groups[s] for s in self.manual_draw_order ]

		# ordre des groupes à draw par la map
		self.draw_order = [
			"portals",
			"fakewalls",
			"walls",
			"mobs",
			"spells",
			"players"
		]

		self.draw_order = [ self.groups[s] for s in self.draw_order ]

		# fix displays
		self.framerate_display = entities.FixDisplay(self, lambda game: str(int(game.clock.get_fps())), WHITE, (0, 0), self.font)
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

		# load la première map
		self.map = Map(self, self.maps[self.map_index], self.biome)
		
		# quelques booléens sur l'état du jeu
		self.isgameover = False
		self.won_level = False
		self.pause = False

		# setut pour faire l'écran de pause
		self.pause_mask = pgp.pg.Surface(self.res)
		self.pause_mask.fill(BLACK)
		self.pause_mask.set_alpha(64)
		self.pause_mask_rect = self.pause_mask.get_rect()

		# contient le temps écoulé depuis la dernère frame
		self.dt = 0

		# setup la musique
		self.music = None	# permet de garder en mémoire la musique actuelle
		self.change_music(MUSIC_THEME)

		# effectue quelques ticks dans le vide pour initialiser 
		for i in range(4):
			self.clock.tick(self.framerate)

		# démarre la boucle principale du jeu
		self.stop = False
		while not self.stop:
			self.loop()

	# load les paramètres depuis data/settings.json
	def load_settings(self):
		settings = json.load(FILE_SETTINGS)
		# dimension minimales de la fenètre
		self.minres = settings["minres"]
		# dimension actuelles de la fenètre
		self.res = settings["res"]
		self.on_screen = self.res.copy()
		# titre et emplacement de l'icon de la fenètre
		self.title = settings["title"]
		self.icon = settings["icon"]
		# fps cible
		self.framerate = settings["framerate"]
		# fichier keyboard si pygame ne reconnais pas le clavier correctement (sinon default laissa pygame gérer tout seul)
		keyboard = settings["keyboard"]
		if keyboard == "default":
			self.keyboard = pgp.key.Keyboard()
		else:
			self.keyboard = pgp.key.load(DIR_KEYBOARDS + keyboard + ".json")
		# équivalent à appuyer sur J, cf self.event
		self.draw_submap_info = settings["draw_submap_info"]
		# équivalent à appuyer sur H, cf self.event
		self.draw_hitbox = settings["draw_hitbox"]
		# taille en pixels de chaque tuile de jeu
		self.tile_size = settings["tile_size"]
		# taille en tuile de jeu de chaque sous cartes
		self.submap_size = settings["submap_size"]
		# nombre de sous cartes qui sont toujours update mais si pas draw
		# rectangle dans la zone non visible du joueur
		self.off_screen_alive = settings["off_screen_alive"]
		# permet de na générer qu'une partie de la carte (debug)
		self.generation_length = settings["generation_length"]
		# liste de noms des cartes
		self.maps = settings["maps"]
		self.map_index = 0
		# nom du biome
		# contient toutes les associations entre lettre et entitées pour load un carte
		self.biome = settings["biome"]
		# volume pricipal du jeu entre 0 et 100
		self.volume = settings["volume"] / 100

	# boucle principale du jeu
	def loop(self):
		# attends pour que le jeu ait les bon fps
		self.dt = self.clock.tick(self.framerate)
		# vérifie si le jeu ne lag pas
		# si les fps réels sont trop éloigés de la cible ne pas effectuer la frame et passer à la suivante
		if self.framerate != 0 and (1 / (2 * self.framerate) > self.dt or self.dt > 2 / self.framerate):
			print("/!\\ LAG: {}fps or {}s/t | rather than {}fps or {}s/t".format(round(1 / self.dt), round(self.dt, 3), self.framerate, round(1 / self.framerate, 3)))
			return
		# choisis entre la boucle de pause et la boucle "normale"
		if not self.pause:
			self.events()
			self.update()
			self.draw()
		else:
			self.events_pause()
			self.update_pause()
			self.draw_pause()

	# change les dimensions de la fenètre
	def set_res(self, new_res):
		# si la nouvelle dimension est inférieur aux dimensions minimales, les mettres au minimale
		if new_res[0] < self.minres[0]:
			new_res[0] = self.minres[0]
		if new_res[1] < self.minres[1]:
			new_res[1] = self.minres[1]

		# enregistre les nouvelles dimensions
		self.res = new_res

		# recréé une fenètre
		self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE)
		self.rect = self.window.get_rect()

		# recréé l'image de fond
		self.background_image = pgp.pg.Surface(self.res)
		self.background_image.fill(BLACK)
		self.background_rect = self.background_image.get_rect()

		# recréé l'image de pause
		self.pause_mask = pgp.pg.Surface(self.res)
		self.pause_mask.fill(BLACK)
		self.pause_mask.set_alpha(64)
		self.pause_mask_rect = self.pause_mask.get_rect()

		# recréé les paramètre de la map qui dépandes des dimensions 
		self.on_screen = self.res.copy()
		self.map.reset_followers()
		self.map.reset_submaps_groups()

	# gère tous les events (demande que quiter, touches du clavier, redimensionement, etc...)
	def events(self):
		# prend en mémoire les touches enffoncées
		self.keys = pgp.pg.key.get_pressed()
		# fait le toure de tous les event disponibles
		for event in pgp.pg.event.get():
			if event.type == pgp.pg.KEYDOWN: # keydown pour le debug et la pause
				"""if event.key == pgp.pg.K_F11:
					self.fullscreen = not self.fullscreen
					if self.fullscreen:
						self.window = pgp.pg.display.set_mode((self.display_info.current_w, self.display_info.current_h), pgp.pg.FULLSCREEN | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
					else:
						self.window = pgp.pg.display.set_mode(self.res, pgp.pg.RESIZABLE | pgp.pg.HWSURFACE | pgp.pg.DOUBLEBUF)
					self.rect = self.window.get_rect()
				el"""
				if event.key == pgp.pg.K_h: # H: affiche les hitboxs
					self.draw_hitbox = not self.draw_hitbox
				elif event.key == pgp.pg.K_j: # J: affiche les hitboxs des submaps
					self.draw_submap_info = not self.draw_submap_info
				elif event.key == pgp.pg.K_k: # K: réduit le champ de vision
					self.on_screen = list(vec(self.on_screen) * (1 / 16 if self.on_screen == self.res else 16))
					self.map.reset_followers()
					self.map.reset_submaps_groups()
				elif event.key == pgp.pg.K_ESCAPE: # échape: demande la pause
					self.pause = not self.pause
			# demande un changerment de dimensions
			elif event.type == pgp.pg.VIDEORESIZE:
				self.set_res([event.w, event.h])
			# demande de quitter
			elif event.type == pgp.pg.QUIT:
				self.stop = True

	# calcule les dégats, les courbes de déplacements, etc...
	def update(self):
		# la map s'occupe de joindre toutes les entitées pour les update
		self.map.update()
		# updates manuelles
		for group in self.manual_update_order:
			group.update()

	# calcule la nouvelle image à afficher
	def draw(self):
		# replacer l'image prècèdante par l'image de fond
		self.window.blit(self.background_image, self.background_rect)
		# la map s'occupe de joindre toutes les entitées pour les draw
		self.map.draw(self.window)
		# draw manuelles
		for group in self.manual_draw_order:
			for sprite in group:
				sprite.draw(self.window, self.map.rpos)
		# affiche l'image créée
		pgp.pg.display.flip()

	# version en pause de self.event
	def events_pause(self):
		# prend en mémoire les touches enffoncées
		self.keys = pgp.pg.key.get_pressed()
		# fait le toure de tous les event disponibles
		for event in pgp.pg.event.get():
			if event.type == pgp.pg.KEYDOWN:
				# si échape et pas gameover
				# alors enlever la pause
				if event.key == pgp.pg.K_ESCAPE and not self.isgameover:
					self.pause = not self.pause
					if self.pause:
						self.paused_surface = self.window.copy()
						self.paused_surface_rect = self.paused_surface.get_rect()
			# demande un changerment de dimensions
			elif event.type == pgp.pg.VIDEORESIZE:
				self.set_res(list(event.size))
			# demande de quitter
			elif event.type == pgp.pg.QUIT:
				self.stop = True

	# version en pause de self.update
	def update_pause(self):
		# n'update pas les sprites de la map
		# seul les updates manuelles sont éffectué
		# (fix displays: fps et debug)
		for group in self.manual_update_order:
			group.update()

	# version en pause de self.draw
	def draw_pause(self):
		# cf self.draw car simmilaire
		self.window.blit(self.background_image, self.background_rect)
		self.map.draw(self.window)
		self.window.blit(self.pause_mask, self.pause_mask_rect)
		for group in self.manual_draw_order:
			for sprite in group:
				sprite.draw(self.window, self.map.rpos)
		pgp.pg.display.flip()

	# déclache l'écran de gameover
	# met le jeu en pause pour toujours
	# affiche gameover sur l'écran et déclanche une musique
	def gameover(self):
		# met en pause pour toujours
		self.pause = True
		self.isgameover = True
		# display
		self.gameover_display = entities.FixDisplay(self, "GAME OVER", WHITE, (self.res[0] // 2, self.res[1] // 2), font= self.big_font)
		self.gameover_display.pos -= vec(self.gameover_display.image.size) / 2
		self.gameover_display.update()
		# change la musique
		self.change_music(MUSIC_GAMEOVER, 1)

	# passe au niveau suivant
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

	# déclache l'écran de vitoire
	# fonctionne comme self.gameover
	def win_game(self):
		self.change_music(MUSIC_WON, 1)
		self.pause = True
		self.isgameover = True
		self.gameover_display = entities.FixDisplay(self, "YOU WON", WHITE, (self.res[0] // 2, self.res[1] // 2), font= self.big_font)
		self.gameover_display.pos -= vec(self.gameover_display.image.size) / 2
		self.gameover_display.update()

	# permet de changer la musique
	def change_music(self, filename, repeat= -1):
		# enregistre la musique en cours
		self.music = filename
		# load, met le bon volume (settings) et joue la musique
		pgp.pg.mixer.music.load(self.music)
		pgp.pg.mixer.music.set_volume(self.volume)
		pgp.pg.mixer.music.play(repeat)



