import json

def load(filename):
	return json.load(open(filename, mode= "r", encoding= "utf-8"))

def dump(filename, obj):
	json.dump(obj, open(filename, mode= "w", encoding= "utf-8"), sort_keys= True, indent= 4)


