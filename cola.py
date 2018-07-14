class cola:
	def __init__(self):
		self.items = []

	def encolar(self, x):
		self.items.append(x)

	def desencolar(self):
		if self.esta_vacia():
			return None
		return self.items.pop(0)

	def esta_vacia(self):
		return len(self.items) == 0