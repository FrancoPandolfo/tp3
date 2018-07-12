import heapq
import queue
import random
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def viajante(grafo,origen):
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

def viajante_aproximado(grafo,origen):
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


def camino_minimo(grafo,origen,destino):
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



