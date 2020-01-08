import pygame as pg
import time

"""
Améliore la Clock de pygame pour donner le
temps avec le plus de précision possible.
(donné par time.perf_counter())
"""

class Clock():
	def __init__(self):
		self.clock = pg.time.Clock()
		self.beg = None
		self.end = None

	def tick(self, framerate= 0):
		self.beg = time.perf_counter()
		self.clock.tick(framerate)
		self.end = time.perf_counter()
		return self.get_time()

	def tick_busy_loop(self, framerate= 0):
		self.beg = time.perf_counter()
		self.clock.tick_busy_loop(framerate)
		self.end = time.perf_counter()
		return self.get_time()

	def get_time(self):
		if self.beg is not None:
			return time.perf_counter() - self.beg
		else:
			return 0

	def get_rawtime(self):
		if self.end is not None:
			return time.perf_counter() - self.end
		else:
			return 0

	def get_fps(self):
		return self.clock.get_fps()


