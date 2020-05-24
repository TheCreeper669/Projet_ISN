
"""
ProjectEternalMagic

Le projet est sous Creative Commons Attribution-ShareAlike 4.0 International License.

le jeu est découpé en plusieurs parties:
 * "launcher/": partie complètement à part du reste du projet, sous PySide2 (interface avec Qt5), pour géré un launcher
 * "data/": regroupes tous les fichier d'images de cartes et de paramètres du jeu
 * "pygamepp/": encapsule pygame et amèliore quelques fonctions
 * "entities/": gères les sprites, les images, les entitées, les hitbox, etc...
 * "json_handler.py": gère les fichier .json
 * "map.py": gère les cartes les sous cartes les tuiles et les fichiers qui leurs sont rattachés
 * "vars.py": regroupes toutes les constantes du jeu (fichiers, dossiers, touches, couleurs, extensions, etc...)
 * "game.py": créé l'objet principal du jeu qui coordone toutes ses parties
"""

from game import *

pygame.init()
Game()
pygame.quit()
