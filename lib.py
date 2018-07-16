import heapq
import queue
import random
import math
import itertools
from collections import OrderedDict
from grafoPeso import grafoPeso
from grafoDir import grafoDir

def buscar_pos(dic,vertice):
	cont = 0
	for v in dic:
		if v == vertice:
			break
		cont += 1
	return cont

def buscar_vertice(dic,pos):
	cont = 0
	for v in dic:
		if cont == pos:
			return v
		cont += 1

def viajante_floyd(grafo,origen):
	w, h = len(grafo.dic), len(grafo.dic);
	dist = [[math.inf for x in range(w)] for y in range(h)]
	for i in range(0,h):
		dist[i][i] = 0
	posV = 0
	for v in grafo.dic:
		for w in grafo.dic[v]:
			posW = buscar_pos(grafo.dic,w)
			dist[posV][posW] = grafo.VerPeso(v,w)
		posV += 1
	for k in range(0,h):
		for i in range(0,h):
			for j in range(0,h):
				if dist[i][j] > dist[i][k] + dist[k][j]:
					dist[i][j] = dist[i][k] + dist[k][j]
	return dist


def encontrar_minimo(grafo,camino,costoMinimo):
	for i in range(0,len(camino)):
		if i+1 < len(camino):
			actual = camino[i]
			siguiente = camino[i+1]
			costoMinimo += grafo.VerPeso(actual,siguiente)
		else:
			continue
	return costoMinimo

def encontrar_caminos_aux(origen,vertices, inicio, caminos):  #helper method
	if inicio >= len(vertices):
		insertar = vertices.copy()
		insertar.insert(0,origen)
		insertar.append(origen)
		caminos.append(insertar[:])
	else:
		for i in range(inicio, len(vertices)):
			vertices[i], vertices[inicio] = vertices[inicio], vertices[i]
			encontrar_caminos_aux(origen,vertices, inicio +1, caminos)
			vertices[inicio], vertices[i] = vertices[i], vertices[inicio]

def encontrar_caminos(origen, vertices,caminos):
	encontrar_caminos_aux(origen, vertices, 0, caminos)
	return caminos


def distancias(grafo,caminos,costos):
	for i in range(0,len(caminos)):
		actual = caminos[i][0]
		for j in range(1,len(caminos[i])):
			siguiente = caminos[i][j]
			costos[i] += grafo.VerPeso(actual,siguiente)
			actual = siguiente
	return costos

def menor_camino(caminos,costos,camino,costo):
	costo = costos[0]
	costo_actual = 0
	pos = 0
	for i in range(1,len(costos)):
		costo_actual = costos[i]
		if costo_actual < costo:
			costo = costo_actual
			pos = i
	camino = caminos[i]
	return camino, costo


def viajante(grafo,origen):
	dic = grafo.dic.copy()
	del dic[origen]
	vertices = list(dic.keys())
	vertice = vertices[1]
	camino = []
	visitado = []
	visitado.append(origen)
	costo = 0
	caminos = []
	caminos = encontrar_caminos(origen, vertices,caminos)
	costos = [0] * len(caminos)
	costos = distancias(grafo,caminos,costos)
	camino, costo = menor_camino(caminos,costos,camino,costo)
	return camino, costo

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
	vertice = list(padre.keys())[-1]
	viaje.append(origen)
	peso_total = dist[vertice] + grafo.VerPeso(vertice,origen)
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

def orden_topologico(grafo,lista):
	grado = {}
	for u in grafo.dic:
		grado[u] = 0
	'''for m in grafo.dic:
		for w in grafo.VerVecinos(m):
			grado[w] += 1'''
	aux = []
	g = 0
	for x in lista:
		aux.append(x[0])
	aux = OrderedDict((x, True) for x in aux).keys()
	for y in aux:
		g += 1
		grado[y] += g
	for tupla in lista:
		if grado[tupla[1]] <= grado[tupla[0]]:
			grado[tupla[1]] = grado[tupla[0]] + 1
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
	if len(resul) != len(grafo.dic):
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

def armar_archivo1(archivo,camino,coordenadas):
	file = open(archivo,'w')

	file.write("%s\n" % ('<?xml version="1.0" encoding="UTF-8"?>'))
	file.write("%s\n" % ('<kml xmlns="http://earth.google.com/kml/2.1">'))
	file.write("\t%s\n" % ('<Document>'))
	file.write("\t\t%s\n\n" % ('<name>camino</name>'))
	for i in range(0,len(camino[0])):
		x = camino[0][i]
		coord1 = coordenadas[x]
		file.write("\t\t%s\n" % ('<Placemark>'))
		file.write("\t\t\t%s%s%s\n" % ('<name>',x, '</name>'))
		file.write("\t\t\t%s\n" % ('<Point>'))
		file.write("\t\t\t\t%s%s%s%s%s\n" % (' <coordinates>',str(coord1[0]),', ', str(coord1[1]),'</coordinates>'))
		file.write("\t\t\t%s\n" % ('</Point>'))
		file.write("\t\t%s\n\n" % ('</Placemark>'))

	for i in range(0,len(camino[0])):
		x = camino[0][i]
		coord1 = coordenadas[x]
		if i < len(camino[0])-1:
			y = camino[0][i+1]
			coord2 = coordenadas[y]
			file.write("\t\t%s\n" % ('<Placemark>'))
			file.write("\t\t\t%s\n" % ('<LineString>'))
			file.write("\t\t\t\t%s%s%s%s%s%s%s%s%s\n" % ('<coordinates>',str(coord1[0]),', ', str(coord1[1]),' ',str(coord2[0]),', ', str(coord2[1]),'</coordinates>'))
			file.write("\t\t\t%s\n" % ('</LineString>'))
			file.write("\t\t%s\n\n" % ('</Placemark>'))

	file.write("\t%s\n" % ('</Document>'))
	file.write("%s\n" % ('</kml>'))			
	file.close()

def armar_archivo2(archivo,camino,coordenadas):
	file = open(archivo,'w')

	file.write("%s\n" % ('<?xml version="1.0" encoding="UTF-8"?>'))
	file.write("%s\n" % ('<kml xmlns="http://earth.google.com/kml/2.1">'))
	file.write("\t%s\n" % ('<Document>'))
	file.write("\t\t%s\n\n" % ('<name>itinerario</name>'))
	for i in range(0,len(camino)):
		x = camino[i]
		coord1 = coordenadas[x]
		file.write("\t\t%s\n" % ('<Placemark>'))
		file.write("\t\t\t%s%s%s\n" % ('<name>',x, '</name>'))
		file.write("\t\t\t%s\n" % ('<Point>'))
		file.write("\t\t\t\t%s%s%s%s%s\n" % (' <coordinates>',str(coord1[0]),', ', str(coord1[1]),'</coordinates>'))
		file.write("\t\t\t%s\n" % ('</Point>'))
		file.write("\t\t%s\n\n" % ('</Placemark>'))

	for i in range(0,len(camino)):
		x = camino[i]
		coord1 = coordenadas[x]
		if i < len(camino)-1:
			y = camino[i+1]
			coord2 = coordenadas[y]
			file.write("\t\t%s\n" % ('<Placemark>'))
			file.write("\t\t\t%s\n" % ('<LineString>'))
			file.write("\t\t\t\t%s%s%s%s%s%s%s%s%s\n" % ('<coordinates>',str(coord1[0]),', ', str(coord1[1]),' ',str(coord2[0]),', ', str(coord2[1]),'</coordinates>'))
			file.write("\t\t\t%s\n" % ('</LineString>'))
			file.write("\t\t%s\n\n" % ('</Placemark>'))

	file.write("\t%s\n" % ('</Document>'))
	file.write("%s\n" % ('</kml>'))			
	file.close()