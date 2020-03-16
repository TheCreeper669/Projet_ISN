import pygame as pg

import json_handler as json

def Keyboard():
	k = { pg.__dict__[e]: pg.__dict__[e] for e in pg.__dict__ if e[:2] == "K_" }
	return k

def change(keyboard, o, n):
	keyboard[pg.__dict__["K_" + o]] = pg.__dict__["K_" + n]

def load(filename):
	keyboard = Keyboard()
	for e in json.load(filename):
		change(keyboard, *e)
	return keyboard

def dump(keyboard, filename):
	json.dump(filename, keyboard)


