import pygamepp as pgp
pg = pgp.pg
from vars import *

class Game:
	def __init__(self):
		self.clock = pgp.time.Clock()
		with pgp.json.load(DIR_SETTINGS) as settings:
			self.res = settings["res"]
			self.framerate = settings["framerate"]
			self.keyboard = settings["keyboard"]

	def start(self):
		for i in range(4):
			self.clock.tick(self.framerate)
		self.stop = False
		while not self.stop:
			self.loop()

	def loop(self):
		self.last_tick = self.clock.tick(self.framerate)
		self.events()
		self.update()
		self.draw()

	def events(self):
		self.keys = pg.key.get_pressed()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				stop = True

	def update(self):
		pass

	def draw(self):
		pass


