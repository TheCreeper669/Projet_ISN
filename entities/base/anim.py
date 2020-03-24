import pygamepp as pgp
from vars import *
import json_handler as json

from entities.base.image import Image

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
