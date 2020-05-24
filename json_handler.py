import json

# permet de ne pas avoir à explicitement ouvrir un fichier
# permet de simplifier la lecture du code qui utilise du JSON

# importe les données d'un fichier .json
def load(filename):
	return json.load(open(filename, mode= "r", encoding= "utf-8"))

# créer un fichier .json avec son nom et l'objet à encoder en JSON
def dump(filename, obj):
	json.dump(obj, open(filename, mode= "w", encoding= "utf-8"), sort_keys= True, indent= 4)
