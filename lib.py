import heapq
import queue
import random
import math
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def ArmarCamino(grafo,padre,distancia,origen):
	for v in padre:
		for w in padre:
			if v == w:
				continue
			if padre[v] == padre[w]:
				if distancia[v] < distancia[w]:
					padre[w] = v
					distancia[w] = distancia[v] + grafo.VerPeso(v, w)
				else:
					padre[v] = w
					distancia[v] = distancia[w] + grafo.VerPeso(v, w)
	return padre,distancia

def viajante(grafo,origen):
	dist = {}
	padre = {}
	for v in grafo.MostrarVertices():
		dist[v] = math.inf
	dist[origen] = 0
	padre[origen] = None
	heap = []
	heapq.heappush(heap, (0, origen))
	while len(heap) > 0:
		peso, v = heapq.heappop(heap)
		for w in grafo.VerVecinos(v):
			if dist[v] + grafo.VerPeso(v, w) < dist[w]:
				dist[w] = dist[v] + grafo.VerPeso(v, w)
				padre[w] = v
				heapq.heappush(heap, (dist[w], w))
	ArmarCamino(grafo,padre,dist,origen)
	return padre, dist

def viajante_aproximado_funcion(grafo,origen):
	visitado = []
	padre = {}
	dist = {}
	cola = queue.Queue()
	visitado.append(origen)
	heap = []
	heap2 = []
	padre[origen] = None
	dist[origen] = 0
	heapq.heappush(heap,origen)
	while len (heap) > 0:
		v = heapq.heappop(heap)
		contador = 0
		for w in grafo.VerVecinos(v):
			a = (grafo.VerPeso(v,w),v,w)
			heapq.heappush(heap2,a)
			contador += 1
		while len (heap2) > 0:
			u = heapq.heappop(heap2)
			contador -= 1
			if u[2] not in visitado:
				visitado.append(u[2])
				padre[u[2]] = v
				dist[u[2]] = dist[v] + u[0]
				heapq.heappush(heap,u[2])
				break
			else:
				continue
		for i in range(0,contador):
			heapq.heappop(heap2)
	return padre,dist

def viajante_aproximado(grafo,origen):
	padre, dist = viajante_aproximado_funcion(grafo, origen)
	viaje = []
	peso_total = 0
	for v in padre:
		viaje.append(v)
	for w in dist:
		peso_total += dist[w]
	return viaje, peso_total

"""	Devuelve una lista con el camino mínimo, y la menor distancia desde
	el origen hacia el destino	"""
def dijkstra(grafo, origen):
	dist = {}
	padre = {}
	for v in grafo.MostrarVertices():
		dist[v] = math.inf
	dist[origen] = 0
	padre[origen] = None
	heap = []
	heapq.heappush(heap, (0, origen))
	while len(heap) > 0:
		peso, v = heapq.heappop(heap)
		for w in grafo.VerVecinos(v):
			if dist[v] + grafo.VerPeso(v, w) < dist[w]:
				dist[w] = dist[v] + grafo.VerPeso(v, w)
				padre[w] = v
				heapq.heappush(heap, (dist[w], w))
	return padre, dist

def armar_camino(padre, destino):
	aux = destino
	camino = []
	while aux:
		camino.append(aux)
		aux = padre[aux]
	camino.reverse()
	return camino

def camino_minimo(grafo, origen, destino):
	padre, dist = dijkstra(grafo, origen)
	return armar_camino(padre, destino), dist[destino]

def orden_topologico(grafo):
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
	if len(resul) == 0:
		return None
	else:
		return resul

def arbol_tendido_minimo(grafo):
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
