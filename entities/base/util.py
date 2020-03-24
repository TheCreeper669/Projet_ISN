from vars import *

def collide(a, b):
	if not hasattr(a, "hitbox"):
		if not hasattr(b, "hitbox"):
			return a.image.colliderect(b.image)
		else:
			return a.image.colliderect(b.hitbox.image)
	else:
		if not hasattr(b, "hitbox"):
			return a.hitbox.image.colliderect(b.image)
		else:
			return a.hitbox.image.colliderect(b.hitbox.image)

def not_collide(a, b):
	return not collide(a, b)

def get_orientation(keys, keyboard, key_up, key_down, key_left, key_right):
	orientation = vec(0)
	if keys[keyboard[key_left]]:
		orientation.x += -1
	if keys[keyboard[key_right]]:
		orientation.x += 1
	if keys[keyboard[key_up]]:
		orientation.y += -1
	if keys[keyboard[key_down]]:
		orientation.y += 1
	return orientation
