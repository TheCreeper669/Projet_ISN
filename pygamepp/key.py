import pygame as pg
import json_handler as json

# permet de chager certaines touches
# n'est pas utile si pygame reconnais correctement le clavier
# permet également de choisir sois même ses touche si on le veut

# créer un dictionnaire pygame key -> pygame key
# sera changé dans pygamepp.key.load
def Keyboard():
	k = { pg.__dict__[e]: pg.__dict__[e] for e in pg.__dict__ if e[:2] == "K_" }
	return k

# change une key pour une autre
def change(keyboard, o, n):
	keyboard[pg.__dict__["K_" + o]] = pg.__dict__["K_" + n]

# load un fichier .json de keyboard
def load(filename):
	keyboard = Keyboard()
	for e in json.load(filename).items():
		change(keyboard, *e)
	return keyboard

# dump un fichier .json de keyboard
def dump(keyboard, filename):
	json.dump(filename, keyboard)
