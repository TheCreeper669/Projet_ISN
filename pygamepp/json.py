import json

def load(filename, **kw):
	with open(filename, mode= "r", encode= "utf-8") as file:
		json.loads(file, **kw)

def dump(filename, obj, **kw):
	with open(filename, mode= "w", encode= "utf-8") as file:
		json.dump(obj, file, **kw)


