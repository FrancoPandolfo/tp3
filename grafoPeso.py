
class grafoPeso:
	def __init__(self,dic):
		self.dic = dic

	def AgregarVertice(self,vertice):
		if vertice not in self.dic:
			self.dic[vertice] = {}

	def AgregarArista(self,arista):
		if arista[1] not in self.dic[arista[0]]:
			self.dic[arista[0]][arista[1]] = arista[2]
		if arista[0] not in self.dic[arista[1]]:
			self.dic[arista[1]][arista[0]] = arista[2]

	def SacarVertice(self,vertice):
		del self.dic[vertice]
		l1=list(self.dic.keys())
		for v in l1:
			l2=list(self.dic[v].keys())
			for i in l2:
				if i==vertice:
					del self.dic[v][i]

	def SacarArista(self,arista):
		if arista[1] in self.dic[arista[0]]: 
			del self.dic[arista[0]][arista[1]]
		if arista[0] in self.dic[arista[1]]:
			del self.dic[arista[1]][arista[0]]

	def EstanConectados(self,v1,v2):
		if v2 in self.dic[v1]:
			return True
		else:
			return False

	def VerVecinos(self,vertice):
		lista = []
		for v in self.dic[vertice]:
			lista.append(v)
		return lista

	def VerPeso(self,v1,v2):
		if v1 in self.dic:
			if v2 in self.dic[v1]:
				return self.dic[v1][v2]
			else:
				return 0

	def CantidadAristas(self):
		contador = 0
		for v in self.dic:
			for w in self.VerVecinos(v):
				if v == w:
					continue
				contador += 1
		return contador // 2

	def PesoTotal(self):
		visitado = []
		contador = 0
		for v in self.dic:
			visitado.append(v)
			for w in self.VerVecinos(v):
				if v == w:
					continue
				if w not in visitado:
					contador += self.VerPeso(v,w)
		return contador