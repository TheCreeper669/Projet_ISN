import pygame as pg

import pygamepp.json as json

keys = { e[1]: e[1] for e in pg.__dict__ if e[0][:1] == "K_" }

def change(o, n):
	keys[pg.__dict__["K_" + o]] = pg.__dict__["K_" + n]

def load(filename):
	nkeys = json.load(filename)
	for e in nkeys:
		change(*e)

def dump(filename):
	json.dump()


