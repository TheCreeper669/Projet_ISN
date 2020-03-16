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
		self.dt = 0
		self.vals = [0] * 11

	def tick(self, framerate= 0):
		self.clock.tick(framerate)
		self.vals = [time.perf_counter()] + self.vals[:-1]
		return self.get_time()

	def get_time(self):
		return self.vals[0] - self.vals[1]

	def get_fps(self):
		return self.clock.get_fps()


