from math import sqrt

# /!\ N'EST PAS UTILISÉ /!\

class Vector:
	def __init__(self, size):
		if not isinstance(size, int) or size < 0:
			raise ValueError("vector size must be a positive integer")
		elif size == 0:
			self.arr = []
		else:
			self.arr = [0] * size

	def copy(self):
		ret = type(self)(len(self))
		ret.arr = self.arr.copy()

	def __len__(self):
		return self.size

	def __bool__(self):
		return bool(len(self))

	def __getitem__(self, index):
		return self.arr[index]

	def __setitem__(self, index, data):
		self.arr[index] = data

	def __iadd__(self, other):
		try:
			if len(other) == 0:
				pass
			elif len(other) != len(self):
				raise ValueError("cannot add two vector of different sizes")
			else:
				for i in range(len(self)):
					self[i] += other[i]
		except TypeError:
			for i in range(len(self)):
				self[i] += other
		return self

	def __add__(self, other):
		ret = self.copy()
		ret += other
		return ret

	def __isub__(self, other):
		try:
			if len(other) == 0:
				pass
			elif len(other) != len(self):
				raise ValueError("cannot sub two vector of different sizes")
			else:
				for i in range(len(self)):
					self[i] -= other[i]
		except TypeError:
			for i in range(len(self)):
				self[i] -= other
		return self

	def __sub__(self, other):
		ret = self.copy()
		ret -= other
		return ret

	def __imul__(self, other):
		try:
			if len(other) == 0:
				pass
			elif len(other) != len(self):
				raise ValueError("cannot mul two vector of different sizes")
			else:
				self0 = self[0]
				other0 = other[0]
				for i in range(len(self) - 1):
					self[i] = self[i] * other[i + 1] - self[i + 1] * other[i]
				self[-1] = self0 * other[-1] - self[-1] * other0
		except TypeError:
			for i in range(len(self)):
				self[i] *= other
		return self

	def __sub__(self, other):
		ret = self.copy()
		ret -= other
		return ret

	def __itruediv__(self, other):
		for i in range(len(self)):
			self[i] /= other
		return self

	def __truediv__(self, other):
		ret = self.copy()
		ret /= other
		return ret

	def __ifloordiv__(self, other):
		for i in range(len(self)):
			self[i] //= other
		return self

	def __floordiv__(self, other):
		ret = self.copy()
		ret //= other
		return ret

	def __imod__(self, other):
		for i in range(len(self)):
			self[i] %= other
		return self

	def __mod__(self, other):
		ret = self.copy()
		ret %= other
		return ret

	def magnitude(self):
		return sqrt(sum(e ** 2 for e in self.arr))

def Vector2():
	return Vector(2)

def Vector3():
	return Vector(3)