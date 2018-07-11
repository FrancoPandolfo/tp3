import heapq
import queue
import random
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def RecorridoMinimo(grafo,origen):
	dist = {}
	padre = {}
	for v in grafo.dic: 
		dist[v] = 9999
	dist[origen] = 0
	padre[origen] = None
	heap = []
	heapq.heappush(heap,origen)
	while len (heap) > 0:
		v = heapq.heappop(heap)
		for w in grafo.VerVecinos(v):
			if dist[v] + grafo.dic[v][w] < dist[w]:
				padre[w] = v
				dist[w] = dist[v] + grafo.dic[v][w]
				heapq.heappush(heap,w)
	return padre,dist

def ArmarCamino(padre,distancia,origen):
	condicion1 = False
	condicion2 = False
	for v in padre:
		for w in padre:
			if v == w:
				continue
			if padre[v] == padre[w]:
				if distancia[v] < distancia[w]:
					for x in padre:
						if padre[x] == v:
							padre[w] = None
							condicion1 = True
							break
					if condicion1 == True:
						continue
					else:
						padre[v] = None
				else:
					for y in padre:
						if padre[y] == w:
							padre[v] = None
							condicion2 = True
							break
					if condicion2 == True:
						continue
					else:
						padre[w] = None
	return padre


def CaminoMinimo(grafo,origen,destino):
	dist = {}
	padre = {}
	for v in grafo.dic: 
		dist[v] = 9999
	dist[origen] = 0
	padre[origen] = None
	heap = []
	heapq.heappush(heap,origen)
	while len (heap) > 0:
		v = heapq.heappop(heap)
		if v == destino:
			padre = ArmarCamino(padre,dist,origen)
			break
		for w in grafo.VerVecinos(v):
			if dist[v] + grafo.dic[v][w] < dist[w]:
				padre[w] = v
				dist[w] = dist[v] + grafo.dic[v][w]
				heapq.heappush(heap,w)
	return padre,dist

def OrdenTopologico(grafo):
	grado = {}
	for u in grafo.dic:
		grado[u] = 0
	for m in grafo.dic:
		for w in grafo.VerVecinos(m):
			grado[w] += 1
	resul = []
	cola = queue.Queue()
	for n in grafo.dic:
		if grado[n] == 0:
			cola.put(n)
	while not cola.empty():
		x = cola.get()
		resul.append(x)
		for v in grafo.VerVecinos(x):
			grado[v] -= 1
			if grado[v] == 0:
				cola.put(v)
	return resul

def ArbolTendidoMinimo(grafo):
	inicio = random.choice(list(grafo.dic.keys()))
	visitado = []
	visitado.append(inicio)
	heap = []
	for w in grafo.VerVecinos(inicio):
		arista1 = (grafo.VerPeso(inicio,w),inicio,w)
		heapq.heappush(heap,arista1)
	arbol = grafoPeso({})
	for x in grafo.dic:
		arbol.AgregarVertice(x)
	while len(heap) > 0:
		a = heapq.heappop(heap)
		if a[2] in visitado:
			continue
		arista2 = (a[1],a[2],a[0])
		arbol.AgregarArista(arista2)
		visitado.append(a[2])
		for u in grafo.VerVecinos(a[2]):
			arista3 = (grafo.VerPeso(a[2],u),a[2],u)
			heapq.heappush(heap,arista3)
	return arbol


graph=grafoPeso({})
graph.AgregarVertice('A')
graph.AgregarVertice('B')
graph.AgregarVertice('C')
graph.AgregarVertice('D')
graph.AgregarVertice('E')
graph.AgregarArista(('A','B',1))
graph.AgregarArista(('B','C',4))
graph.AgregarArista(('A','D',2))
graph.AgregarArista(('B','D',3))
graph.AgregarArista(('D','C',2))
graph.AgregarArista(('C','E',2))
graph.AgregarArista(('E','D',703))
graph.AgregarArista(('E','B',7))
#print(RecorridoMinimo(graph,'A'))
#print(CaminoMinimo(graph,'A','E'))
print(ArbolTendidoMinimo(graph).dic)


graph2=grafoDir({})
graph2.AgregarVertice('A')
graph2.AgregarVertice('B')
graph2.AgregarVertice('C')
graph2.AgregarVertice('D')
graph2.AgregarVertice('E')
graph2.AgregarArista(('A','B'))
graph2.AgregarArista(('B','C'))
graph2.AgregarArista(('A','D'))
graph2.AgregarArista(('B','D'))
graph2.AgregarArista(('D','C'))
graph2.AgregarArista(('C','E'))
#print(OrdenTopologico(graph2))



